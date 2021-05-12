import logging
from Models.BaseValidator import BaseValidator
from Common import utils


class SmartScheduleValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):
        data.exception_list = []
        if (data.number_of_years is not None and utils.is_int_or_float(data.number_of_years)):
            pass
        else:
            data.exception_list.append("%s is not valid" % "number_of_years")

        if (data.increase_amount is not None and utils.is_int_or_float(data.increase_amount)):
            pass
        else:
            data.exception_list.append("%s is not valid" % "increase_amount")

        if (data.dollar_or_percent is not None and data.dollar_or_percent.lower() in ['dollar', 'percent', 'dollars']):
            pass
        else:
            data.exception_list.append("%s is not valid" % "dollar_or_percent")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self,data):
        return True
