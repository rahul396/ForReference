import numpy as np
from Common.aop import after, before
from Models.BaseModel import BaseModel
from Models.PortfolioValidator import PortfolioValidator
import logging
import traceback


class Portfolio(BaseModel):
    def __init__(self, context, asset_class_names=None, asset_class_weights=None):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.asset_class_names = asset_class_names
        self.asset_class_weights = np.array(asset_class_weights)
        self.acp = context.asset_class_properties_init

    @before()
    @after
    def set_values(self, data):
        pass

    @before()
    @after
    def set_additional_parameters(self):
        try:
            self.expected_return = self.portfolio_er_calc()
            self.standard_deviation = self.portfolio_stdev_calc()
        except Exception as ex:
            self.LOG.exception("Error Occurred %s " % ex)
            #self.LOG.exception(traceback.format_exc())

    @before()
    @after
    def validate(self):
        validator = PortfolioValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = PortfolioValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

    def check_portfolio_integrity(self):
        is_error = False
        error_code = []

        sum_portfolio = np.sum(self.asset_class_weights)
        if sum_portfolio != 1:
            error_code.append(
                "Sum of portfolio weights <> 1: %f" % sum_portfolio)
            is_error = True

        if is_error:
            return error_code

    def portfolio_er_calc(self):
        return np.dot(self.asset_class_weights, self.acp.get_asset_class_expected_return(self.asset_class_names))

    def portfolio_stdev_calc(self):
        return np.sqrt((np.dot(self.asset_class_weights.T,
                               np.dot(self.acp.get_covariance_matrix(self.asset_class_names),
                                      self.asset_class_weights))))

    def portfolio_equity_alloc_calc(self):
        return np.dot(self.asset_class_weights, self.acp.get_asset_class_equity_indicator(self.asset_class_names))

    def get_asset_allocation(self):
        return np.vstack((self.asset_class_names, self.asset_class_weights))
