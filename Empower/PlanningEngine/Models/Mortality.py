import numpy as np
import pandas as pd


# Calculate the mortatlity probabilities or life expectancy given an age, health_state and gender
# requries an external data sournce (currently excel), with age, health state, and gompertzmakeham factors
# IMPROVE - if a health state or gender has a higher age (e.g. one has a factor for 80 and the other for 75)
# And then an age is passed over the max age for one health state but not the other, this will error out because max age is capped at teh highest age in the file_path_and_name_with_ext
# not a different max age for each health state, make sure max age is always the same for now
class Mortality(object):
    def __init__(self, file_path_and_name_with_ext, ip_sheet_number, error_init):

        # open excel file, get first sheet and parse columns
        xlfile = pd.ExcelFile(file_path_and_name_with_ext)
        xlsheet = xlfile.parse(ip_sheet_number)
        # array has health state, gender, age, gm, gb factors
        # temp becuase in 5 year increments, adjustment below
        self.temp_gm_gb_array = np.array(xlsheet.iloc[:, 0:5])
        self.min_age = np.min(self.temp_gm_gb_array[:, 2])
        self.max_start_age = np.max(self.temp_gm_gb_array[:, 2])
        self.error_init = error_init
        # the current table is in increments of 5, use interpolattion to fill out ages between increments
        self.gm_gb_array = self.__expand_gm_gb_table()

    def __expand_gm_gb_table(self):
        expanded_gm_gb_array = np.empty(([5]))

        for row_iter in range(self.temp_gm_gb_array.shape[0] - 1):
            if (self.temp_gm_gb_array[row_iter, 0] == self.temp_gm_gb_array[row_iter + 1, 0] and self.temp_gm_gb_array[
                row_iter, 1] == self.temp_gm_gb_array[row_iter + 1, 1] and self.temp_gm_gb_array[row_iter, 2] !=
                    self.temp_gm_gb_array[row_iter + 1, 2]):
                start_age = self.temp_gm_gb_array[row_iter, 2]
                end_age = self.temp_gm_gb_array[row_iter + 1, 2]

                for age_iter in range(start_age, end_age):
                    lower_weight = (end_age - age_iter) / (end_age - start_age)
                    upper_weight = 1 - lower_weight
                    new_gm = self.temp_gm_gb_array[row_iter, 3] * lower_weight + self.temp_gm_gb_array[
                        row_iter + 1, 3] * upper_weight
                    new_gb = self.temp_gm_gb_array[row_iter, 4] * lower_weight + self.temp_gm_gb_array[
                        row_iter + 1, 4] * upper_weight
                    new_row = np.array(
                        [self.temp_gm_gb_array[row_iter, 0], self.temp_gm_gb_array[row_iter, 1], age_iter, new_gm,
                         new_gb])
                    expanded_gm_gb_array = np.vstack(
                        (expanded_gm_gb_array, new_row))

            else:
                expanded_gm_gb_array = np.vstack(
                    (expanded_gm_gb_array, self.temp_gm_gb_array[row_iter, :]))

        # add the last row to the array, have to do it here becuase of the index + 1 above
        expanded_gm_gb_array = np.vstack(
            (expanded_gm_gb_array, self.temp_gm_gb_array[-1, :]))
        # for some reason everything is a string except the last row so do this to make sure all rows are of the same type
        expanded_gm_gb_array = (np.hstack((expanded_gm_gb_array[:, 0:2], expanded_gm_gb_array[:, 2:3].astype('str'),
                                           expanded_gm_gb_array[:, 3:5].astype('float'))))

        return expanded_gm_gb_array[1:expanded_gm_gb_array.shape[0], :]

    def get_gm_gb_factors(self, health_state='all', gender='all', age='all'):
        if age != 'all' and age > self.max_start_age:
            age = self.max_start_age

        age = str(age)

        if health_state == 'all' and gender == 'all' and age == 'all':
            temp_array = self.gm_gb_array

        elif health_state == 'all' and gender == 'all':
            temp_array = self.gm_gb_array[np.where(
                self.gm_gb_array[:, 2] == age), :]

        elif health_state == 'all' and age == 'all':
            temp_array = self.gm_gb_array[np.where(
                self.gm_gb_array[:, 1] == gender), :]

        elif gender == 'all' and age == 'all':
            temp_array = self.gm_gb_array[np.where(
                self.gm_gb_array[:, 0] == health_state), :]

        elif health_state == 'all':
            temp_array = self.gm_gb_array[
                np.where((self.gm_gb_array[:, 1] == gender) & (self.gm_gb_array[:, 2] == age))]

        elif gender == 'all':
            temp_array = self.gm_gb_array[
                np.where((self.gm_gb_array[:, 0] == health_state) & (self.gm_gb_array[:, 2] == age))]

        elif age == 'all':
            temp_array = self.gm_gb_array[
                np.where((self.gm_gb_array[:, 0] == health_state) & (self.gm_gb_array[:, 1] == gender))]

        else:
            temp_array = self.gm_gb_array[np.where((self.gm_gb_array[:, 0] == health_state) &
                                                   (self.gm_gb_array[:, 1] == gender) & (
                                                   self.gm_gb_array[:, 2] == age)), 3:5][0]

            # IMPROVE Error check if value is not found something like the below
            # if temp_array.shape[0] == 0:
            # throw some error_code
        # else:
        return temp_array

    def mortality_prob_calc(self, gender, start_age, health_state='good', end_age=110):
        number_of_periods = end_age - start_age
        # if an age over the max start age is passed, use the max start age in mortality calculation
        gm_start_age = min(start_age, self.max_start_age)

        # if start age under minimum supported age is passed assume 100% chance of survival
        # start mortality weighting at min age as if that age (e.g. 30 period 0, 1, 2, ...)
        temp_underage_mortality_array = np.empty(0)
        if start_age < self.min_age:
            gm_start_age = self.min_age
            # You don't need to calc for all ages, going to append underage mortality table
            number_of_periods = end_age - self.min_age
            temp_underage_mortality_array = np.full(
                (self.min_age - start_age), 1)

        period_array = np.arange(0, number_of_periods)
        age_array = np.arange(gm_start_age, end_age)

        gm_gb_array = self.get_gm_gb_factors(
            health_state=health_state, gender=gender, age=gm_start_age)
        gm = float(gm_gb_array[:, 0][0])
        gb = float(gm_gb_array[:, 1][0])

        temp_mortality_array = self.gompertz_calc(
            gm, gb, gm_start_age, np.arange(1, number_of_periods + 1))

        return np.append(temp_underage_mortality_array, temp_mortality_array)

    def get_life_expectancy(self, gender, age, health_state="good"):
        return np.around(np.sum(self.mortality_prob_calc(gender, age, health_state)) + age, decimals=0)

    def get_unisex_mortality(self, mortality_array_one, mortality_array_two):
        temp_mortality_array = np.array(
            [mortality_array_one, mortality_array_two])
        return np.mean(temp_mortality_array, axis=0)

    # gompertz makeham mortality calculation, supports a numpy array to calulculate multiple probabilities at once
    def gompertz_calc(self, gm, gb, age, years_array):
        return np.exp(np.exp((age - gm) / gb) * (1 - np.exp(years_array / gb)))


'''
a = Mortality("C:\\Users\\bcosm\\Google Drive\\Macbook\\Documents\Monte_carlo\\setup_files\\mortality_tables.xlsx", "e")
#print(a.get_gm_gb_factors(health_state = 'good',gender = 'male'))
for age in range(20,80):
    print(age, a.get_life_expectancy('female',age, "choles"))
'''
