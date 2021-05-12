import numpy as np
from Common.aop import after, before
from Models.BaseModel import BaseModel
from Models.JobValidator import JobValidator
import logging


class Job(BaseModel):
    def __init__(self, name=None, current_earnings=None, account_array=None, context=None, profit_sharing_amount=0,
                 earnings_curve_id='default'):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.current_earnings = current_earnings
        self.account_array = account_array
        self.context = context
        self.profit_sharing_amount = profit_sharing_amount
        self.earnings_curve_id = earnings_curve_id
        self.number_of_accounts = np.shape(self.account_array)[0]

    @before()
    @after
    def set_values(self, data):
        self.name = getattr(data, "jobName", None)
        self.current_earnings = getattr(data, "annualSalary", None)
        self.earnings_curve_id = getattr(data, "jobDescription", 'default')

    @before()
    @after
    def set_additional_parameters(self):
        pass

    @before()
    @after
    def validate(self):
        validator = JobValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = JobValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

    def get_total_match_possible(self):
        pass

    def get_total_match_recieved(self):
        pass

    def get_total_contribution(self):
        total_contribution = 0  # Author:Rahul
        for contribution in self.contributions:
            if contribution.is_percent is False:
                total_contribution += contribution.amount_or_percent
            else:
                total_contribution += contribution.amount_or_percent * self.current_earnings
        return total_contribution  # Author:Rahul

    def get_earnings_curve(self, age, retire_age):
        return self.context.earnings_growth_init.get_real_earnings(age, self.current_earnings, self.earnings_curve_id,
                                                                   retire_age)
