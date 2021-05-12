import datetime
import numpy as np
import pandas as pd
import utils
import FileHandlers,config


class Social_Security(object):
    def __init__(self, social_security_dataframe):
        self.social_security_df = social_security_dataframe
        self.ss_table = np.array(self.social_security_df.iloc[:, 1:5])
        self.youngest_claim_age = config.youngest_claim_age
        self.oldest_claim_age = config.oldest_claim_age

    def get_full_benefit_age(self, age):
        now = datetime.datetime.now()
        birth_year = now.year - age
        if birth_year < 1937:
            return 65
        elif birth_year < 1954:
            return 66
        else:
            return 67
        ##????????????????##############################

    def __get_upper_lower_lookup(self, lookup_value, column_number, start_row=0, end_row=-1):
        """Gives the upper and lower ranges of rows for the lookup value"""
        lower_range = []
        upper_range = []

        if end_row == -1:
            end_row = np.shape(self.ss_table)[0] - 1

        lookup_column = self.ss_table[start_row:end_row + 1, column_number]

        if lookup_value in lookup_column:
            indices = np.where(lookup_column == lookup_value)[0]
            # lower range will be [start_index,end_index]
            lower_range.append(indices[0]+start_row)
            lower_range.append(indices[-1]+start_row)
            # if the value is present then both lower and upper ranges are same
            upper_range = lower_range[:]
        else:
            lookup_set = np.unique(lookup_column)
            upper_index = 0
            # if the value is too small
            if lookup_set[upper_index] > lookup_value:
                return 'Value not found'
            while lookup_set[upper_index] < lookup_value:
                upper_index += 1
                # if the value is too large
                if upper_index > lookup_set.size - 1:
                    return 'Value not found'

            lower_index = upper_index - 1  # lower_lookup_value is just 1 index before upper_lookup_value in the unique array
            # get the upper_lookup_value e.g if lookup_value = 30000, then upper_lookup_value=40000
            upper_lookup_value = lookup_set[upper_index]
            # get the lower_lookup_value e.g if lookup_value = 30000, then lower_lookup_value=20000
            lower_lookup_value = lookup_set[lower_index]
            # now find the ranges in which these upper and lower lookup values are present in the lookup_column
            lower_lookup_index_list = np.where(lookup_column == lower_lookup_value)[0]
            upper_lookup_index_list = np.where(lookup_column == upper_lookup_value)[0]
            # append them in the arrays. A padding of start_row has been added as we have to get the row value for excelsheet
            lower_range.append(lower_lookup_index_list[0] + start_row)
            lower_range.append(lower_lookup_index_list[-1] + start_row)
            upper_range.append(upper_lookup_index_list[0] + start_row)
            upper_range.append(upper_lookup_index_list[-1] + start_row)

        return [lower_range, upper_range]

    ##Extract the benefit, given a benefit start age, current age and current salary####################################
    ##this is the critical function#####################################################################################
    def get_benefit_amount(self, current_age, retire_age, current_salary):
        #get min and max index value for age four values returns, min and max for lower, min and max for upper
        age_bands_array = self.__get_upper_lower_lookup(current_age,0)
        #get min and max index value for retirement age for a given age
        fia_iter = 0
        final_index_array = np.empty((8), dtype = int)
        for age_band_row in age_bands_array:
            try:
                retire_age_bands_array = self.__get_upper_lower_lookup(retire_age, 1, age_band_row[0], age_band_row[1])
                #get min and max index value for salary given retirement age and ages
            except IndexError as e:
                print ("Given age: {} not in the data range".format(current_age))
                return 'Unable to find the retire age ranges for calculation'

            for retire_age_band_row in retire_age_bands_array:
                try:
                    temp_final_array =  np.array(self.__get_upper_lower_lookup(current_salary, 2, retire_age_band_row[0], retire_age_band_row[1]))
                except IndexError as e:
                    print ("Given retire_age : {} not in the data range".format(retire_age))
                    return 'Unable to find the current salary ranges for calculation'
                try:
                    final_index_array[fia_iter] = temp_final_array[0,0]
                    final_index_array[fia_iter+1] = temp_final_array[1,1]
                    fia_iter +=2
                except IndexError as e:
                    print ("Given current_salary : {} not in the data range".format(current_salary))
                    return "Exiting..."

        fia_iter = 0
        salary_ss_array = np.empty((2))
        retire_ss_array = np.empty((2))

        for age_iter in range(0,2):
            for ret_age_iter in range(0,2):
                x_values = [self.ss_table[final_index_array[fia_iter],2],self.ss_table[final_index_array[fia_iter+1],2]]
                y_values = [self.ss_table[final_index_array[fia_iter],3],self.ss_table[final_index_array[fia_iter+1],3]]
                salary_ss_array[ret_age_iter] = utils.interpolate_calculation(current_salary, x_values, y_values)
                fia_iter += 2

            x_values = [self.ss_table[final_index_array[0],1],self.ss_table[final_index_array[2],1]]
            y_values = salary_ss_array
            retire_ss_array[age_iter] = utils.interpolate_calculation(retire_age, x_values, y_values)

        x_values = [self.ss_table[final_index_array[0],0],self.ss_table[final_index_array[4],0]]
        y_values = retire_ss_array
        return  utils.interpolate_calculation(current_age, x_values, y_values)


    def get_benefit_for_all_claiming_ages(self, current_age, current_salary):
        start_claim_age = max(current_age, self.youngest_claim_age)
        end_claim_age = max(self.oldest_claim_age, current_age)
        temp_return_array = np.empty((end_claim_age - start_claim_age + 1, 2))
        return_index = 0
        for claim_age_iter in range(start_claim_age, end_claim_age + 1):
            temp_return_array[return_index, 0] = claim_age_iter
            temp_return_array[return_index, 1] = self.get_benefit_amount(current_age, claim_age_iter, current_salary)
            return_index += 1

        return temp_return_array

    ##Extract the benefit for all start Social Security ages for one Head of Household####################################

    def get_benefit_for_all_household_claiming_ages(self, current_hh1_age, current_hh1_salary, current_hh2_age,
                                                    current_hh2_salary):
        hh1_array = self.get_benefit_for_all_claiming_ages(current_hh1_age, current_hh1_salary)
        hh2_array = self.get_benefit_for_all_claiming_ages(current_hh2_age, current_hh2_salary)
        temp_return_array = np.empty((hh1_array.shape[0] * hh2_array.shape[0], 4))
        temp_iter = 0
        for hh1_iter in range(hh1_array.shape[0]):
            for hh2_iter in range(hh2_array.shape[0]):
                temp_return_array[temp_iter, 0] = hh1_array[hh1_iter, 0]
                temp_return_array[temp_iter, 1] = hh1_array[hh1_iter, 1]
                temp_return_array[temp_iter, 2] = hh2_array[hh2_iter, 0]
                temp_return_array[temp_iter, 3] = hh2_array[hh2_iter, 1]
                temp_iter += 1

        return temp_return_array


my_path = config.social_security_sheet
social_security_df = FileHandlers.get_dataframe(my_path, 1)
ss = Social_Security(social_security_df)
#print(ss.get_benefit_amount(20,72, 400000))
# print(ss.get_benefit_amount(71,71,100000))
print(ss.get_benefit_for_all_household_claiming_ages(25,100000, 25,100000))
#print (ss.get_benefit_for_all_claiming_ages(15,70000))