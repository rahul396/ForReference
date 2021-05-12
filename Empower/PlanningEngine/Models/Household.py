import numpy as np
from Models.Account import Account
from Models.Portfolio import Portfolio
import Simulation.Simulation_File as sf
import Models.Glidepath_Creator as gpc
from Common.aop import after, before
from Models.BaseModel import BaseModel
from Models.HouseholdValidator import HouseholdValidator
import logging
import traceback


class Household(BaseModel):
    def __init__(self, head_of_household_array=None, state_of_residence=None, context=None, account_array=[],
                 cashflow_array=[], retire_state_of_residence="", dependents=0):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.head_of_household_array = head_of_household_array
        self.number_of_hohs = np.shape(head_of_household_array)[0]
        self.dependents = dependents
        self.state_of_residence = state_of_residence
        self.context = context
        self.retire_state_of_residence = retire_state_of_residence
        if retire_state_of_residence == "":
            self.retire_state_of_residence = self.state_of_residence
        if np.size(head_of_household_array) == 1:
            self.filing_status = 'single'
            self.number_of_hoh = 1
        else:
            self.filing_status = 'joint'
            self.number_of_hoh = 2

        self.account_array = account_array
        self.cashflow_array = cashflow_array
        self.retirment_need_adjustment_after_death = .8

    @before()
    @after
    def set_values(self, data):
        pass
        # self.state_of_residence = getattr(data,"stateCode",None)

    @before()
    @after
    def set_additional_parameters(self):
        try:
            self.max_periods_alive = self.get_max_periods_alive()
            self.create_default_account()

        except Exception as ex:
            self.LOG.exception("Error Occurred %s " % ex)
            #self.LOG.exception(traceback.format_exc())

    @before()
    @after
    def validate(self):
        validator = HouseholdValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = HouseholdValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

    def get_all_jobs(self):
        temp_job_array = []
        for each_hoh in self.head_of_household_array:
            temp_job_array.append(each_hoh.job_array)
        return temp_job_array

    def get_all_accounts(self):
        temp_account_array = []
        for each_account in self.account_array:
            temp_account_array.append(each_account)

        for each_hoh in self.head_of_household_array:
            for each_hoh_account in each_hoh.account_array:
                temp_account_array.append(each_hoh_account)
            for each_job in each_hoh.job_array:
                for each_job_account in each_job.account_array:
                    temp_account_array.append(each_job_account)

        return temp_account_array

    def get_min_rmd_period(self):
        min_rmd_period = 100
        for each_hoh in self.head_of_household_array:
            min_rmd_period = max(
                min(min_rmd_period, self.context.rmd_init.min_rmd_age - each_hoh.age), 0)

        return min_rmd_period

    def get_max_periods_alive(self):
        max_periods_alive = 0
        for each_hoh in self.head_of_household_array:
            max_periods_alive = np.maximum(
                each_hoh.life_expectancy - each_hoh.age, max_periods_alive)

        return int(max_periods_alive)

    # all households need an account where excess cashflow can go penalty free
    # if there is already a default eligable account, use the first one, if not
    # add one to the household
    def create_default_account(self):
        temp_account_array = self.get_all_accounts()
        found_default_account = False
        for each_account in temp_account_array:
            if each_account.default_account_support:
                found_default_account = True
                each_account.set_default_cashflow_status()
                break

        if not found_default_account:
            temp_weights = [1]
            temp_asset_classes = [
                self.context.asset_class_properties_init.get_lowest_risk_asset_class()]
            temp_portfolio = Portfolio(
                self.context, temp_asset_classes, temp_weights)
            temp_glidepath = gpc.static_glidepath_creator(temp_portfolio, 100)
            temp_sim_file = sf.Monte_Carlo_Returns_All_Years(
                temp_glidepath, self.context)
            temp_account = Account("Default", "Taxable", [
                ["taxable", 0]], temp_glidepath, temp_sim_file, self.context)
            temp_account.set_default_cashflow_status()
            self.account_array.append(temp_account)
