import logging
from Models.BaseValidator import BaseValidator
from Common import utils


class JobValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.name is not None and utils.is_string(data.name):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Job Name")

        if data.current_earnings is not None and utils.is_int_or_float(data.current_earnings):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Current Earnings")

        if data.account_array is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Account Array")

        if data.profit_sharing_amount is not None:
            pass
        else:
            data.exception_list.append(
                "%s is not valid" % "Profit Sharing Amount")

        if data.earnings_curve_id is not None and utils.is_string(data.earnings_curve_id):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Earning Curve Id")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self,data):
        return True