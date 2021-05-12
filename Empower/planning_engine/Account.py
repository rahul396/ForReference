import numpy as np
import datetime
import Contribution as contri
import copy

class Account(object):

    def __init__(self,name_of_account, type_of_account, balance_array, glidepath, sim_file, init_params, contribution_array = [], start_contribution_year = '', smart_schedule ='',match_obj = None):
        self.id = name_of_account
        self.balance_array= np.array(balance_array)
        self.glidepath = glidepath
        self.sim_file = sim_file
        self.contribution_array  = contribution_array
        self.match = match_obj
        self.smart_schedule = smart_schedule
        self.start_contribution_year = start_contribution_year
        if self.start_contribution_year == '':
            self.start_contribution_year = datetime.datetime.now().year
        self.applicable_limits_array = init_params.account_type_init.get_applicable_limits(type_of_account)
        self.contributions_subject_to_fica = init_params.account_type_init.get_contributions_subject_to_fica(type_of_account)
        self.early_penality_withdrawal_age = init_params.account_type_init.get_early_penality_withdrawal_age(type_of_account)
        self.early_penality_withdrawal_percent = init_params.account_type_init.get_early_penality_withdrawal_percent(type_of_account)
        self.loan_limit = init_params.account_type_init.get_loan_limit(type_of_account)
        self.pretax_support = init_params.account_type_init.get_pretax_support(type_of_account)
        self.roth_support = init_params.account_type_init.get_roth_support(type_of_account)
        self.after_tax_support = init_params.account_type_init.get_after_tax_support(type_of_account)
        self.taxable_support = init_params.account_type_init.get_taxable_support(type_of_account)
        self.default_account_support = init_params.account_type_init.get_default_account_support(type_of_account)
        self.default_cashflow_status = False
        self.rmd_applies = init_params.account_type_init.get_rmd_applies(type_of_account)
        self.pair_balance_and_contribuitons()
        #self.print_balance_and_contribution()

    #there will be situations where a balance is passed with no corresponding contriubtion
    #and where contribution is passed with no correspodning balance
    #to make things easier, we want all balances to have a matching contribuiton and contribution to have a matching balance
    #put zeros in where there is a mismatch, also align them to make simulations matrix math easier
    def pair_balance_and_contribuitons(self):
        #check if there is a balance with no contriubtions
        for each_balance in self.balance_array:
            missing_contribution = True
            for each_contribution in self.contribution_array:
                if each_balance[0] == each_contribution.money_type:
                    missing_contribution = False
            #add the missing contriubiton at 0 dollars
            if missing_contribution:
                self.contribution_array.append(contri.Contribution(0,each_balance[0], False,self.id))

        #check if there is a contribution with no balance
        for each_contribution in self.contribution_array:
            missing_balance = True
            for each_balance in self.balance_array:
                if each_balance[0] == each_contribution.money_type:
                    missing_balance = False
            #add the missing balance at 0 dollars
            if missing_balance:
                self.balance_array = np.vstack((self.balance_array,[each_contribution.money_type, 0]))

        #order the balance and contributions to match
        balance_location = []
        for each_balance in self.balance_array:
            contri_iter = 0
            for each_contri in self.contribution_array:
                if each_balance[0] == each_contri.money_type:
                    balance_location.append(contri_iter)
                    #Improve, should add an exit here
                contri_iter +=1

        balance_iter = 0
        temp_balance = copy.deepcopy(self.balance_array)

        for each_location in balance_location:
            self.balance_array[each_location,:] = temp_balance[balance_iter,:]
            balance_iter +=1

    def set_default_cashflow_status(self):
        self.default_cashflow_status = True


    def print_balance_and_contribution(self):

        for each_balance in self.balance_array:
            print (each_balance[0],self.id, "balance loop")

        for each_contri in self.contribution_array:
            print (each_contri.money_type, self.id)

    def get_total_balance(self):
        return np.sum(np.array(self.balance_array[:,1],dtype=np.float64))

    def get_balance_by_money_type(self, money_type = 'all'):
        if money_type == 'all':
            return self.balance_array
        else:
            return self.balance_array[np.where(self.balance_array == money_type)[0],1][0]

    def get_current_asset_allocation(self):
        return self.glidepath.get_asset_allocation_glidepath() [:,0]

    def get_current_equity_allocation(self):
        return self.glidepath.get_equity_allocation_glidepath() [:,0]

    def get_match_received(self, contribution):
        return self.match.get_employer_match_received(contribution)

    def get_match_missed(self, contribution):
        return self.match.get_match_missed(contribution)
