from datetime import datetime
import utils
import numpy as np


class Individual(object):

    def __init__(self, name, date_of_birth, retire_age, gender, retirement_need, retirement_need_type, init_params,
                health_state = 'good',account_array= [], job_array = [], pension_array = [],ss_start_age = '', ss_amount_override = ''):

        self.init_params = init_params
        self.name = name
        self.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
        self.retire_age = retire_age
        self.gender = gender
        self.retirement_need_type = retirement_need_type
        self.retirement_need = retirement_need
        self.age = utils.calculate_date_dif(self.date_of_birth)
        self.health_state = health_state
        self.life_expectancy = self.get_life_expectancy()
        self.account_array = account_array
        self.job_array = job_array
        self.total_comp = self.get_total_earnings()
        self.mortality_init = init_params.mortality_init
        self.set_ss_start_age(ss_start_age)
        self.ss_benefit = ss_amount_override
        if self.ss_benefit == '':
            self.ss_benefit = self.get_social_security_estimate()

        self.pension_array = pension_array

    def set_ss_start_age(self, ss_start_age, update_benefit = True):
        if ss_start_age == '':
            #self.ss_start_age = init_params.social_security_init.get_full_benefit_age(self.age)
            self.ss_start_age = max(self.retire_age, 62)
        else:
            self.ss_start_age = ss_start_age
        if update_benefit:
            self.ss_benefit = self.get_social_security_estimate()

    def get_life_expectancy(self):
        return self.init_params.mortality_init.get_life_expectancy(self.gender, self.age, self.health_state)

    def set_retire_age(self, retire_age):
        self.retire_age = retire_age
        self.get_years_to_retirement()
        self.set_ss_start_age(retire_age, True)


    def get_total_earnings(self):
        total_earnings = 0
        for job_iter in self.job_array:
            total_earnings += job_iter.current_earnings

        return total_earnings


    def get_social_security_estimate(self):
        return self.init_params.social_security_init.get_benefit_amount(self.age, self.ss_start_age, self.total_comp)*12

    def set_pension_array(self, pension_array):
        self.pension_array = pension_array

    def get_years_to_retirement(self):
        return self.retire_age - self.age

    def get_retire_year(self):
        return 2018 + self.get_years_to_retirement()
