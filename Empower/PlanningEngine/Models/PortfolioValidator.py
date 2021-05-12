import logging
from Models.BaseValidator import BaseValidator
from Common import utils
import numpy as np


class PortfolioValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.asset_class_names is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "Asset Class Names")

        if data.asset_class_weights is not None and not (data.asset_class_weights < 0).any():
            pass
        else:
            data.exception_list.append("%s is not valid" % "asset_class_weights")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self, data):
        # asset_class_weights should add upto 100%
        if np.sum(data.asset_class_weights) == 1:
            pass
        else:
            data.exception_list.append("%s do not add up to 1" % "asset_class_weights")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid
