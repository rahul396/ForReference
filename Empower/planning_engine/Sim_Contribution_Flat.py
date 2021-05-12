import numpy as np
import Contribution as contr

class Sim_Contribution_Flat(object):

    def __init__(self, earnings_array, years_to_retirement,  owner_name, each_account, contri_obj, smart_obj = '', match_obj =''):
        self.earnings_array = earnings_array
        self.years_to_retirement = years_to_retirement
        self.contri_obj = contri_obj
        self.account = each_account
        self.account_id  = each_account.id
        self.money_type = contri_obj.money_type
        self.owner_name = owner_name
        self.smart_obj = smart_obj
        self.match_obj = match_obj
        self.flat_contri_array = self.__set_contirbution_array()
        #if the contribution array doesn't have anything in it return an array of all zeros

    def __set_contirbution_array(self):
        if np.shape(self.contri_obj) == 0:
            return np.zeros((100))
        else:

            temp_array = np.full((self.years_to_retirement), self.contri_obj.amount_or_percent)
            if self.contri_obj.is_percent == True:
                #multipy salary (earnings) times contribution amount
                temp_array = self.earnings_array[0:self.years_to_retirement] * temp_array

            temp_array = np.hstack((temp_array, np.zeros((100 - self.years_to_retirement))))

            return temp_array

    def set_contribution_by_year(self, year_index, amount):
        self.flat_contri_array[year_index] = amount

    def get_contribution_for_year(self, year_index):
        return self.flat_contri_array[year_index]

    def print_me(self):
        print (self.owner_name, self.account_id, self.money_type)
        print (self.flat_contri_array)
