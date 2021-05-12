import logging
from Models.BaseValidator import BaseValidator
from Common import utils


class CashflowValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.name is not None and utils.is_string(data.name):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Name")

        if data.start_year is not None and utils.is_int(data.start_year):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Start Year")

        if data.end_year is not None and utils.is_int(data.end_year) and data.end_year >= data.start_year:
            pass
        else:
            data.exception_list.append("%s is not valid" % "End Year")

        if data.amount is not None and utils.is_int_or_float(data.amount):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Amount")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self,data):
        return True