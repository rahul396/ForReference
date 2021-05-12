import numpy as np

class Job(object):

    def __init__ (self, job_name, current_earnings, account_array, init_params,  profit_sharing_amount= 0, earnings_curve_id = 'default'):
        self.name= job_name
        self.current_earnings  = current_earnings
        self.profit_sharing_amount = profit_sharing_amount
        self.account_array = account_array
        self.number_of_accounts = np.shape(self.account_array)[0]
        self.earnings_curve_id = earnings_curve_id
        self.init_params = init_params


    def get_total_match_possible(self):
        pass

    def get_total_match_recieved(self):
        pass

    def get_total_contribution (self):
        for contribution in self.contributions:
            if contribution.is_percent == False:
                total_contribution += contribution.amount_or_percent
            else:
                total_contribution += contribution.amount_or_percent * self.current_earnings

    def get_earnings_curve (self, age, retire_age):
        return  self.init_params.earnings_growth_init.get_real_earnings(age,self.current_earnings, self.earnings_curve_id, retire_age)
