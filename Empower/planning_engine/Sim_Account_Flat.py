import numpy as np

class Sim_Account_Flat(object):

    def __init__(self,account_id, money_type, start_balance, sim_file, penality_age,  penality_amount,
                 account_rmd_applies, default_cashflow_status, owner_age, locked_for_withdrawal_period = -1):
        self.id = account_id
        self.money_type = money_type
        self.penality_age = penality_age
        self.penality_amount = penality_amount
        self.locked_for_withdrawal_period = locked_for_withdrawal_period
        self.start_balance  = start_balance
        self.sim_file = sim_file
        self.rmd_applies = self.get_rmd_applies(account_rmd_applies)
        self.default_cashflow_status = default_cashflow_status
        self.owner_age = owner_age


    def print_properties(self):
        print(self.id, " " , self.money_type, " ", self.penality_age, " ", self.locked_for_withdrawal_period, " "
            , self.withdrawal_sequence, " ", self.default_cashflow_status, " ",self.rmd_applies)

    def get_rmd_applies(self, account_rmd_applies):
        if account_rmd_applies and self.money_type == 'pretax':
            return True
        else:
            False
