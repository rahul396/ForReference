import numpy as np
import pandas as pd
import Sim_Cashflow_Array_Creator as scar
import os

class Sim_Household_Cashflows(object):


    def __init__(self, household, init_params):

        self.init_params = init_params
        self.household = household
        self.column_headers =  np.hstack((['owner', 'id', 'category'], np.arange(100))).tolist()
        self.start_earnings_column = 3
        self.taxable_cashflows_numpy = np.zeros((100))
        self.include_in_annual_net_numpy = np.zeros((100))
        self.hhc_dataframe = pd.DataFrame(self.set_compensation_array(),columns = self.column_headers)
        self.hhc_dataframe = pd.concat([self.hhc_dataframe,(pd.DataFrame(self.set_retirement_need_array(),columns = self.column_headers))])
        self.hhc_dataframe = pd.concat([self.hhc_dataframe,(pd.DataFrame(self.set_ss_array(),columns = self.column_headers))])
        self.hhc_dataframe = pd.concat([self.hhc_dataframe,(pd.DataFrame(self.set_pension_array(),columns = self.column_headers))])
        if self.household.cashflow_array != []:
            self.hhc_dataframe = pd.concat([self.hhc_dataframe,(pd.DataFrame(self.set_cashflow_array(),columns = self.column_headers))])
        self.min_cashflow_period = 100


        self.output_hhc_df_to_excel()

    def set_compensation_array(self):
        temp_compensation_array = np.empty((103), dtype = float)
        for each_ind in self.household.head_of_household_array:
            for each_job in each_ind.job_array:
                temp_np = np.hstack((each_job.get_earnings_curve(each_ind.age, each_ind.retire_age), np.zeros(100 - (each_ind.retire_age - each_ind.age))))
                temp_compensation_array = np.vstack((temp_compensation_array,np.hstack((each_ind.name, each_job.name,'earnings', temp_np))))
                self.taxable_cashflows_numpy = np.vstack((self.taxable_cashflows_numpy, temp_np))

        return temp_compensation_array[1:]

    def set_cashflow_array(self):
        temp_cashflow_array = np.hstack(('houeshold','none','cashflow',np.zeros((100), dtype = float)))

        for each_cashflow in self.household.cashflow_array:
            temp_np = scar.create_cashflow_array(each_cashflow.amount, each_cashflow.start_year - 2018, each_cashflow.end_year - 2018,100,self.init_params,
            each_cashflow.inflate_to_start, each_cashflow.inflate_to_end, each_cashflow.inflation)

            temp_cashflow_array = np.vstack((temp_cashflow_array,
            np.hstack(('houeshold', each_cashflow.id,'cashflow', temp_np))))

            self.include_in_annual_net_numpy = np.vstack((self.include_in_annual_net_numpy, temp_np))
            if each_cashflow.is_taxable:
                self.taxable_cashflows_numpy = np.vstack((self.taxable_cashflows_numpy, temp_np))


        return temp_cashflow_array[1:]

    def set_retirement_need_array(self):
        temp_retire_need_array = np.empty((103), dtype = float)
        for each_ind in self.household.head_of_household_array:
            if each_ind.retirement_need_type == 'dollar':
                temp_retirement_need = each_ind.retirement_need
            else:
                temp_retirement_need = each_ind.retirement_need * self.get_earnings(each_ind.name, int(each_ind.retire_age - each_ind.age - 1 ))

            temp_np = scar.create_cashflow_array(temp_retirement_need, each_ind.retire_age- each_ind.age,
                                                each_ind.life_expectancy - each_ind.age ,100,self.init_params)*-1
            temp_retire_need_array = np.vstack((temp_retire_need_array,
             np.hstack((each_ind.name, 'retirement_need', 'retirement_need',temp_np))))

        temp_retire_need_array = temp_retire_need_array[1:]
        #print (temp_retire_need_array)

        #need to adjust reitrement need if one person dies before the other
        #sum the two needs together then apply a discount from the init parameters

        if self.household.number_of_hoh == 2:
            first_persion_death_period = int(self.household.head_of_household_array[0].life_expectancy - self.household.head_of_household_array[0].age)
            second_person_death_period = int(self.household.head_of_household_array[1].life_expectancy - self.household.head_of_household_array[1].age)


            hoh_row_to_change = 1
            hoh_period_to_change = first_persion_death_period
            if first_persion_death_period > second_person_death_period:
                hoh_row_to_change = 0
                hoh_period_to_change = second_person_death_period
            hoh_period_to_change = int(self.start_earnings_column - 1 + hoh_period_to_change )

            post_death_retire_need = ((float(temp_retire_need_array[0,int(first_persion_death_period+self.start_earnings_column-1)])
                                    + float(temp_retire_need_array[1,int(first_persion_death_period+self.start_earnings_column-1)]))
                                    * self.init_params.retirement_need_adjustment_after_death
                                    )
                                    
            #print (scar.create_cashflow_array(post_death_retire_need,0,
            #second_person_death_period - first_persion_death_period,second_person_death_period - first_persion_death_period,self.init_params)*-1)

            if second_person_death_period>first_persion_death_period:
                temp_retire_need_array[hoh_row_to_change,first_persion_death_period+self.start_earnings_column:second_person_death_period+self.start_earnings_column] = (
                                            scar.create_cashflow_array(post_death_retire_need,0,
                                            second_person_death_period - first_persion_death_period,
                                            second_person_death_period - first_persion_death_period,self.init_params)
                                            )
        #print (temp_retire_need_array)
        self.include_in_annual_net_numpy = np.vstack((self.include_in_annual_net_numpy, temp_retire_need_array[:,self.start_earnings_column:])).astype(float)


        return temp_retire_need_array

    def set_ss_array(self):
        temp_ss_array = np.empty((103), dtype = float)
        for each_ind in self.household.head_of_household_array:
            temp_np = scar.create_cashflow_array(each_ind.ss_benefit, each_ind.ss_start_age - each_ind.age, each_ind.life_expectancy - each_ind.age ,100,self.init_params)
            temp_ss_array = np.vstack((temp_ss_array,np.hstack((each_ind.name, 'social_security', 'social_security',temp_np))))

            self.include_in_annual_net_numpy = np.vstack((self.include_in_annual_net_numpy, temp_np))
            self.taxable_cashflows_numpy = np.vstack((self.taxable_cashflows_numpy, temp_np*.5))
        return temp_ss_array[1:]

    def set_pension_array(self):
        temp_pension_array = np.hstack(('none','none','pension',np.zeros((100), dtype = float)))
        for each_ind in self.household.head_of_household_array:
            for each_pension in each_ind.pension_array:
                temp_np = scar.create_cashflow_array(each_pension.amount, each_pension.start_age, each_ind.life_expectancy,100,self.init_params,
                each_pension.inflate_to_start, each_pension.inflate_to_end, each_pension.inflation)

                temp_pension_array = np.vstack((temp_pension_array,np.hstack((each_ind.name, each_pension.id,'pension', temp_np))))

                self.include_in_annual_net_numpy = np.vstack((self.include_in_annual_net_numpy, temp_np))
                if each_pension.is_taxable:
                    self.taxable_cashflows_numpy = np.vstack((self.taxable_cashflows_numpy, temp_np))

        if np.shape(temp_pension_array)[0] > 1:
            return temp_pension_array[1:]
        else:
            return temp_pension_array

    def get_earnings(self, ind_name = '', period_number ='', job_name = '' ):
        #if name isn't passed, get all earnings, used to get household earnings
        if ind_name == '':
            temp_df = (self.hhc_dataframe.loc[(self.hhc_dataframe['category'] == "earnings")])
        else:
        #if name is passed just collect earnings for that person
            temp_df = (self.hhc_dataframe.loc[(self.hhc_dataframe['category'] == "earnings")&(self.hhc_dataframe['owner'] == ind_name )])
            #if a specific job name is passed get that job
            if job_name != '':
                temp_df = (self.hhc_dataframe.loc[(self.hhc_dataframe['id'] == job_name)])

        #if  period isn't passed get all years of earnings
        if period_number == '':
            temp_df = temp_df.ix[:,self.start_earnings_column:].sum()
        else:
        #if a period is passed, just return that period, used for things like retirement need as % of last period salary
            temp_df = float(temp_df.ix[:,self.start_earnings_column + period_number].sum()*1)

        return temp_df

    def get_min_cashflow_period(self):
        #print(np.where(self.include_in_annual_net_numpy !=0))
        return 0 #np.where(self.include_in_annual_net_numpy !=0)[1]


    #outputs this object to excel, used for QA purposes
    def output_hhc_df_to_excel(self, output_path = '', output_name = ''):

        if output_name == '':
            output_name = "household cashflows.csv"
        if output_path == '':
            output_path = self.init_params.default_output_location

        self.hhc_dataframe.to_csv(os.path.join(output_path, output_name) )
