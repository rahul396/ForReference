from Common.aop import after, before
from Models.BaseModel import BaseModel
from Models.ContributionValidator import ContributionValidator
import logging


class Contribution(BaseModel):
    def __init__(self, amount_or_percent=None, money_type=None, is_percent=None, account_name=None):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.amount_or_percent = amount_or_percent
        self.money_type = money_type
        self.is_percent = is_percent
        self.account_name = account_name

    @before()
    @after
    def set_values(self, data):
        self.amount_or_percent = getattr(data, "contributionValue", None)
        self.money_type = getattr(data, "plContributionTypeCode", None)
        self.is_percent = getattr(data, "contributionPercentageFlag", None)
        self.account_name = getattr(data, "accountTypeName", None)

    @before()
    @after
    def set_additional_parameters(self):
        pass

    @before()
    @after
    def validate(self):
        validator = ContributionValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = ContributionValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid
