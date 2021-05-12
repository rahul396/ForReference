import datetime

import numpy as np

from Common import utils, config
from Common.aop import after, before
from Common.config import logging
from Common.context import Context


class SocialSecurityBenefitCalculator:
    def __init__(self, social_security_dataframe):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.social_security_df = social_security_dataframe
        self.ss_table = np.array(self.social_security_df.iloc[:, 1:5])

    # ToDo: This method is currently not in use. Need to check with Brian on its usage for future
    def get_full_benefit_age(self, age):
        now = datetime.datetime.now()
        birth_year = now.year - age
        for year, retire_age in config.birthyear_retire_age_dict:
            if birth_year < year:
                return retire_age
        return config.default_retire_age

    @before(['lookup_value'])
    @after
    def __get_upper_lower_lookup(self, lookup_value, column_number, start_row=0, end_row=-1):
        """Gives the upper and lower ranges of rows for the lookup value"""
        lower_range = []
        upper_range = []

        if end_row == -1:
            end_row = np.shape(self.ss_table)[0] - 1

        # Get lookup column on the basis of column number
        lookup_column = self.ss_table[start_row:end_row + 1, column_number]

        if lookup_value in lookup_column:
            self.LOG.debug('lookup_value %s found in lookup_column' % lookup_value)
            indices = np.where(lookup_column == lookup_value)[0]
            # lower range will be [start_index,end_index]
            lower_range.append(indices[0] + start_row)
            lower_range.append(indices[-1] + start_row)
            # if the value is present then both lower and upper ranges are same
            upper_range = lower_range[:]
        else:
            self.LOG.debug(
                'lookup_value %s not present in lookup_column. Getting upper and lower range for lookup value' % lookup_value)
            lookup_set = np.unique(lookup_column)
            upper_index = 0
            # if the value is too small
            if lookup_set[upper_index] > lookup_value:
                self.LOG.debug(
                    'lookup_value %s too small. Cant find in the range of data' % lookup_value)
                return 'Value not found'
            while lookup_set[upper_index] < lookup_value:
                upper_index += 1
                # if the value is too large
                if upper_index > lookup_set.size - 1:
                    self.LOG.debug(
                        'lookup_value %s too large. Cant find in the range of data' % lookup_value)
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

    # Extract the benefit, given a benefit start age, current age and current salary####################################
    # this is the critical function#####################################################################################
    @before(['socialSecurityIndividual.current_age', 'socialSecurityIndividual.retire_age',
             'socialSecurityIndividual.current_salary'])
    @after
    def get_benefit_amount(self, socialSecurityIndividual):

        # socialSecurityValidator = SocialSecurityValidator()

        # Validate the socialSecurityIndividual. If the validation fails, it will raise an exception and exit.
        # socialSecurityValidator.validate(socialSecurityIndividual)

        # if not socialSecurityValidator.validate(socialSecurityIndividual)[0]:
        #     error_list = socialSecurityValidator.validate(socialSecurityIndividual)[1]
        #     self.LOG.error('Invalid input(s) for SocialSecurityIndividual: ' + str(error_list))
        #     raise ValueError('Invalid input(s) for SocialSecurityIndividual: ' + str(error_list))

        # get min and max index value for age four values returns, min and max for lower, min and max for upper
        age_bands_array = self.__get_upper_lower_lookup(socialSecurityIndividual.current_age, 0)
        # get min and max index value for retirement age for a given age
        fia_iter = 0
        final_index_array = np.empty((8), dtype=int)
        for age_band_row in age_bands_array:
            try:
                retire_age_bands_array = self.__get_upper_lower_lookup(
                    socialSecurityIndividual.retire_age, 1,
                    age_band_row[0],
                    age_band_row[1])
                # get min and max index value for salary given retirement age and ages
            except IndexError as e:
                self.LOG.error("Given age: {} not in the data range".format(
                    socialSecurityIndividual.current_age))
                return None

            for retire_age_band_row in retire_age_bands_array:
                try:
                    temp_final_array = np.array(
                        self.__get_upper_lower_lookup(socialSecurityIndividual.current_salary, 2,
                                                      retire_age_band_row[0],
                                                      retire_age_band_row[1]))
                except IndexError as e:
                    self.LOG.error(
                        "Given retire_age : {} not in the data range".format(
                            socialSecurityIndividual.retire_age))
                    return None
                try:
                    final_index_array[fia_iter] = temp_final_array[0, 0]
                    final_index_array[fia_iter + 1] = temp_final_array[1, 1]
                    fia_iter += 2
                except IndexError as e:
                    self.LOG.error("Given current_salary : {} not in the data range".format(
                        socialSecurityIndividual.current_salary))
                    return None

        fia_iter = 0
        salary_ss_array = np.empty((2))
        retire_ss_array = np.empty((2))

        for age_iter in range(0, 2):
            for ret_age_iter in range(0, 2):
                x_values = [self.ss_table[final_index_array[fia_iter], 2],
                            self.ss_table[final_index_array[fia_iter + 1], 2]]
                y_values = [self.ss_table[final_index_array[fia_iter], 3],
                            self.ss_table[final_index_array[fia_iter + 1], 3]]
                salary_ss_array[ret_age_iter] = utils.interpolate_calculation(
                    socialSecurityIndividual.current_salary,
                    x_values,
                    y_values)
                fia_iter += 2

            x_values = [self.ss_table[final_index_array[0], 1],
                        self.ss_table[final_index_array[2], 1]]
            y_values = salary_ss_array

            retire_ss_array[age_iter] = utils.interpolate_calculation(
                socialSecurityIndividual.retire_age, x_values,
                y_values)

        x_values = [self.ss_table[final_index_array[0], 0], self.ss_table[final_index_array[4], 0]]
        y_values = retire_ss_array

        return utils.interpolate_calculation(socialSecurityIndividual.current_age, x_values,
                                             y_values)

    # Extract the benefit for all start Social Security ages for one Head of Household (given current salary)####################################

    @before(['socialSecurityIndividual.current_age', 'socialSecurityIndividual.current_salary'])
    @after
    def get_benefit_for_all_claiming_ages(self, socialSecurityIndividual):
        start_claim_age = max(socialSecurityIndividual.current_age, config.youngest_claim_age)
        end_claim_age = max(config.oldest_claim_age, socialSecurityIndividual.current_age)

        temp_return_array = np.empty((end_claim_age - start_claim_age + 1, 2))
        return_index = 0
        self.LOG.debug(
            'Calculating benefit amount from start_claim_age: %s to end_claim_age: %s' % (
                start_claim_age, end_claim_age))
        for claim_age_iter in range(start_claim_age, end_claim_age + 1):
            socialSecurityIndividual.retire_age = claim_age_iter
            temp_return_array[return_index, 0] = claim_age_iter
            temp_return_array[return_index, 1] = self.get_benefit_amount(socialSecurityIndividual)
            return_index += 1

        return temp_return_array

    # Extract the benefit for all start Social Security ages for one Head of Household####################################

    @before(['socialSecurity.hh1.current_age', 'socialSecurity.hh1.current_salary',
             'socialSecurity.hh2.current_age',
             'socialSecurity.hh2.current_salary'])
    @after
    def get_benefit_for_all_household_claiming_ages(self, socialSecurity):
        hh1_array = self.get_benefit_for_all_claiming_ages(socialSecurity.hh1)
        hh2_array = self.get_benefit_for_all_claiming_ages(socialSecurity.hh2)
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

    def fit_model(self,social_security_individual):
        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.metrics import r2_score
        from matplotlib import pyplot as plt
        X = self.social_security_df[['VH_AGE', 'VH_RET_AGE', 'VH_ANN_SAL']].values
        y = self.social_security_df[['VH_MTHLY_SS_INCOME']].values
        lr_model = DecisionTreeRegressor(max_depth=10)
        lr_model.fit(X, y)
        y_pred = lr_model.predict(X)
        score = r2_score(y, y_pred)
        print('r2_score: ' + str(score))
        return lr_model

    def get_social_security_benefit_using_regression(self,social_security_individual,model):

        # sheet = list(zip(X.tolist(),y_pred.tolist()))
        # for row in sheet:
        #     print (row)
        # plt.figure(figsize=(10,8))
        # plt.plot(X[:,0].reshape(-1,1),y)
        # plt.plot(X[:, 1].reshape(-1, 1), y)
        # plt.plot(X[:, 2].reshape(-1, 1), y)
        # # plt.scatter(X,y_pred)
        # plt.show()
        X_to_predict = np.array([social_security_individual.current_age,
                                     social_security_individual.retire_age,
                                     social_security_individual.current_salary]).reshape(1,3)
        result = model.predict(X_to_predict)
        return result

if __name__ == '__main__':
    from SocialSecurity import SocialSecurityIndividual
    import time
    ctx = Context()
    social_security_df = ctx.social_security_df
    calculator = SocialSecurityBenefitCalculator(social_security_df)
    ss_individual = SocialSecurityIndividual(40,65,90000)
    start = time.clock()
    ss_benefit = calculator.get_benefit_amount(ss_individual)
    end = time.clock()
    utils.print_time_difference(start,end)
    print ('Creating model...')
    model = calculator.fit_model(ss_individual)
    start = time.clock()
    ss_benefit_lr = calculator.get_social_security_benefit_using_regression(ss_individual,model)
    end = time.clock()
    utils.print_time_difference(start, end)
    print (ss_benefit, ss_benefit_lr)