import copy
import numpy as np
from Models.Contribution import Contribution
from Models.BaseModel import BaseModel
from Common.aop import after, before
from Models.AccountValidator import AccountValidator
import logging
import traceback


class Account(BaseModel):
    def __init__(self, name=None, type_of_account=None, balance_array=None, glidepath=None, sim_file=None, context=None,
                 contribution_array=[], start_contribution_year='', smart_schedule='', match_obj=None):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.type_of_account = type_of_account
        self.balance_array = np.array(balance_array)
        self.glidepath = glidepath
        self.sim_file = sim_file
        self.context = context
        self.contribution_array = contribution_array
        self.start_contribution_year = start_contribution_year
        self.smart_schedule = smart_schedule
        self.match_obj = match_obj
        self.default_cashflow_status = False

    @before()
    @after
    def set_values(self, data):
        self.name = getattr(data, "accountTypeName", None)
        self.type_of_account = getattr(data, "accountTypeCode", None)

    @before()
    @after
    def set_additional_parameters(self):
        try:
            if self.type_of_account is not None:
                self.type_of_account = self.type_of_account.lower()
            self.applicable_limits_array = self.context.account_type_init.get_applicable_limits(
                self.type_of_account)
            self.contributions_subject_to_fica = self.context.account_type_init.get_contributions_subject_to_fica(
                self.type_of_account)
            self.early_penality_withdrawal_age = self.context.account_type_init.get_early_penality_withdrawal_age(
                self.type_of_account)
            self.early_penality_withdrawal_percent = self.context.account_type_init.get_early_penality_withdrawal_percent(
                self.type_of_account)
            self.loan_limit = self.context.account_type_init.get_loan_limit(
                self.type_of_account)
            self.pretax_support = self.context.account_type_init.get_pretax_support(
                self.type_of_account)
            self.roth_support = self.context.account_type_init.get_roth_support(
                self.type_of_account)
            self.after_tax_support = self.context.account_type_init.get_after_tax_support(
                self.type_of_account)
            self.taxable_support = self.context.account_type_init.get_taxable_support(
                self.type_of_account)
            self.default_account_support = self.context.account_type_init.get_default_account_support(
                self.type_of_account)

            self.rmd_applies = self.context.account_type_init.get_rmd_applies(
                self.type_of_account)
            self.pair_balance_and_contributions()

        except Exception as e:
            self.LOG.exception("Error Occurred %s " % e)

    @before()
    @after
    def validate(self):
        validator = AccountValidator()
        validator.validate(self)
        return validator.is_valid

    @before
    @after
    def validate_additional_parameters(self):
        validator = AccountValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

    # there will be situations where a balance is passed with no corresponding contriubtion
    # and where contribution is passed with no correspodning balance
    # to make things easier, we want all balances to have a matching contribuiton and contribution to have a matching balance
    # put zeros in where there is a mismatch, also align them to make simulations matrix math easier
    def pair_balance_and_contributions(self):
        # check if there is a balance with no contriubtions
        for each_balance in self.balance_array:
            missing_contribution = True
            for each_contribution in self.contribution_array:
                if each_balance[0] == each_contribution.money_type:
                    missing_contribution = False
            # add the missing contriubiton at 0 dollars
            if missing_contribution:
                self.contribution_array.append(Contribution(
                    0, each_balance[0], False, self.name))

        # check if there is a contribution with no balance
        for each_contribution in self.contribution_array:
            missing_balance = True
            for each_balance in self.balance_array:
                if each_balance[0] == each_contribution.money_type:
                    missing_balance = False
            # add the missing balance at 0 dollars
            if missing_balance:
                self.balance_array = np.vstack(
                    (self.balance_array, [each_contribution.money_type, 0]))

        # order the balance and contributions to match
        balance_location = []
        for each_balance in self.balance_array:
            contri_iter = 0
            for each_contri in self.contribution_array:
                if each_balance[0] == each_contri.money_type:
                    balance_location.append(contri_iter)
                    # Improve, should add an exit here
                contri_iter += 1

        balance_iter = 0
        temp_balance = copy.deepcopy(self.balance_array)

        for each_location in balance_location:
            self.balance_array[each_location,
                               :] = temp_balance[balance_iter, :]
            balance_iter += 1

    def set_default_cashflow_status(self):
        self.default_cashflow_status = True

    def print_balance_and_contribution(self):

        for each_balance in self.balance_array:
            print(each_balance[0], self.id, "balance loop")

        for each_contri in self.contribution_array:
            print(each_contri.money_type, self.id)

    def get_total_balance(self):
        return np.sum(np.array(self.balance_array[:, 1], dtype=np.float64))

    def get_balance_by_money_type(self, money_type='all'):
        if money_type == 'all':
            return self.balance_array
        else:
            return self.balance_array[np.where(self.balance_array == money_type)[0], 1][0]

    def get_current_asset_allocation(self):
        return self.glidepath.get_asset_allocation_glidepath()[:, 0]

    def get_current_equity_allocation(self):
        return self.glidepath.get_equity_allocation_glidepath()[:, 0]

    def get_match_received(self, contribution):
        return self.match.get_employer_match_received(contribution)

    def get_match_missed(self, contribution):
        return self.match.get_match_missed(contribution)
