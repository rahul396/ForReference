import logging
from Models.BaseValidator import BaseValidator
from Common import utils


class ContributionValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.amount_or_percent is not None and utils.is_int_or_float(data.amount_or_percent):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Amount or Percent")

        if data.money_type is not None and utils.is_string(data.money_type):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Money Type")

        if data.is_percent is not None and type(data.is_percent) == bool:
            pass
        else:
            data.exception_list.append("%s is not valid" % "is_percent field")

        if data.account_name is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Account Name")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self,data):
        return True