import logging
from Models.BaseValidator import BaseValidator
from Common import utils


class AccountValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.name is not None and utils.is_string(data.name):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Name")

        if data.type_of_account is not None and utils.is_string(data.type_of_account):
            pass
        else:
            data.exception_list.append("%s is not valid" % "Type of Account")

        if data.balance_array is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Balance Array")

        if data.glidepath is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Glidepath")

        if data.sim_file is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Simulation File")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self,data):
        return True
