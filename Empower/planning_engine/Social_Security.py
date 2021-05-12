import datetime
import numpy as np
import pandas as pd
import os
import utils


class Social_Security(object):

    def __init__ (self, file_path_and_name_with_ext, ip_sheet_num, error_init =""):

        self.error_init = error_init

        try:
            xlfile = pd.ExcelFile(file_path_and_name_with_ext)

        except FileNotFoundError:
            error_init.add_error('critical', "Social_Security",
             "Invalid file path for social_secruity file: %s" %(file_path_and_name_with_ext))

        xlsheet = xlfile.parse(ip_sheet_num)
        #age, reitre_age, salary, estimate
        self.ss_table = np.array(xlsheet.iloc[:,1:5])
        self.youngest_claim_age = 62
        self.oldest_claim_age = 70



    def get_full_benefit_age(self,age):
        now = datetime.datetime.now()
        birth_year = now.year - age
        if birth_year < 1937:
            return 65
        elif birth_year < 1954:
            return 66
        else:
            return 67

    def __get_upper_lower_lookup(self, lookup_value, column_number, start_row = 0, end_row = -1):
        if end_row == -1:
            end_row = np.shape(self.ss_table)[0]

        upper_row_num = start_row
        lower_row_num = -1
        while lookup_value > self.ss_table[upper_row_num, column_number]:
            upper_row_num += 1
            if upper_row_num > end_row:
                #should rasise an error
                return "Value not found"


        if lookup_value == self.ss_table[upper_row_num, column_number]:
            lower_row_num = upper_row_num
            upper_lower_row_num = lower_row_num
            lower_upper_row_num = -1
        else:
            lower_upper_row_num = upper_row_num - 1
            upper_lower_row_num = upper_row_num

        while self.ss_table[upper_row_num,column_number] == self.ss_table[upper_row_num + 1,column_number]:
            upper_row_num +=1

        if lower_upper_row_num == - 1:
            lower_upper_row_num = upper_row_num

        if lower_row_num == -1:
            lower_row_num = lower_upper_row_num
            while self.ss_table[lower_row_num,column_number] == self.ss_table[lower_row_num -1,column_number]:
                lower_row_num += -1
                if lower_row_num == start_row:
                    break

        return [[lower_row_num, lower_upper_row_num], [upper_lower_row_num, upper_row_num]]


    def get_benefit_amount(self, current_age, retire_age, current_salary):
        #get min and max index value for age four values returns, min and max for lower, min and max for upper
        age_bands_array = self.__get_upper_lower_lookup(current_age,0)
        #get min and max index value for retirement age for a given age
        fia_iter = 0
        final_index_array = np.empty((8), dtype = int)
        for age_band_row in age_bands_array:
            retire_age_bands_array = self.__get_upper_lower_lookup(retire_age, 1, age_band_row[0], age_band_row[1])
            #get min and max index value for salary given retirment age and ages

            for retire_age_band_row in retire_age_bands_array:
                temp_final_array =  np.array(self.__get_upper_lower_lookup(current_salary, 2, retire_age_band_row[0], retire_age_band_row[1]))
                final_index_array[fia_iter] = temp_final_array[0,0]
                final_index_array[fia_iter+1] = temp_final_array[1,1]
                fia_iter +=2

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
        start_claim_age = max(current_age,self.youngest_claim_age)
        end_claim_age = max(self.oldest_claim_age, current_age)
        temp_return_array = np.empty((end_claim_age - start_claim_age + 1,2))
        return_index = 0
        for claim_age_iter in range(start_claim_age, end_claim_age+1):
            temp_return_array[return_index,0] = claim_age_iter
            temp_return_array[return_index,1] = self.get_benefit_amount(current_age, claim_age_iter, current_salary)
            return_index +=1

        return temp_return_array

    def get_benefit_for_all_household_claiming_ages(self, current_hh1_age, current_hh1_salary, current_hh2_age, current_hh2_salary):
        hh1_array = self.get_benefit_for_all_claiming_ages(current_hh1_age, current_hh1_salary)
        hh2_array = self.get_benefit_for_all_claiming_ages(current_hh2_age, current_hh2_salary)
        temp_return_array = np.empty((hh1_array.shape[0]* hh2_array.shape[0],4))
        temp_iter = 0
        for hh1_iter in range(hh1_array.shape[0]):
            for hh2_iter in range(hh2_array.shape[0]):
                temp_return_array[temp_iter,0] = hh1_array[hh1_iter,0]
                temp_return_array[temp_iter,1] = hh1_array[hh1_iter,1]
                temp_return_array[temp_iter,2] = hh2_array[hh2_iter,0]
                temp_return_array[temp_iter,3] = hh2_array[hh2_iter,1]
                #print (hh2_array[hh2_iter,0], temp_iter, hh2_iter)
                temp_iter += 1


        total_array= temp_return_array[:,1] + temp_return_array[:,3]
        return np.hstack((temp_return_array, total_array[:,None]))




'''
chr_dir = os.getcwd()
my_path = chr_dir + "\setup_files\Social_Security_Table.xlsm"
ss = Social_Security(my_path)
print(ss.get_benefit_amount(36,66,100000))
#print(ss.get_benefit_amount(71,71,100000))
#print(ss. get_benefit_for_all_household_claiming_ages(67,100000, 71,100000))
'''
