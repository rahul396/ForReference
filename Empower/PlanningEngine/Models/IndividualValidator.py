import logging
from Models.BaseValidator import BaseValidator
from Common import utils


class IndividualValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.name is not None and utils.is_string(data.name):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Name")

        if data.date_of_birth is not None and utils.birth_year_validator(data.date_of_birth):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Date of Birth")

        if data.retire_age is not None and data.retire_age in range(62, 86):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Retirement Age")

        if data.gender is not None and utils.is_string(data.gender):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Gender")

        if data.retirement_need is not None and utils.is_non_negative(data.retirement_need) and utils.is_int_or_float(data.retirement_need):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Retirement Need")

        if data.retirement_need_type is not None and utils.is_string(data.retirement_need_type):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Retirement Need Type")

        if data.age is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Age")

        if data.health_state is not None and utils.is_string(data.health_state):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Health State")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self,data):
        if data.ss_start_age < data.life_expectancy:
            pass
        else:
            data.exception_list.append("%s should start before life_expectancy" % "SS Start age")

        for pension in data.pension_array:
            if pension.start_age < data.life_expectancy - data.age:
                pass
            else:
                data.exception_list.append("%s should start before life_expectancy" % "Pension start age")

        # Glidepath should extend upto life expectancy of the account holder for each account
        for account in data.account_array:
            if account.glidepath.num_years == data.life_expectancy - data.age:
                pass
            else:
                data.exception_list.append("%s should extend only upto life_expectancy" % "Glidepath num_years")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid
