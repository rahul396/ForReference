from Common.aop import after, before
from Models.BaseModel import BaseModel
from Models.SmartScheduleValidator import SmartScheduleValidator
import logging


class SmartSchedule(BaseModel):
    def __init__(self, number_of_years=None, increase_amount=None, dollar_or_percent=None):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.number_of_years = number_of_years
        self.increase_amount = increase_amount
        self.dollar_or_percent = dollar_or_percent

    @before()
    @after
    def set_values(self, data):
        saving_data = getattr(data, "savingsPlan", None)
        if saving_data is not None:
            smart_data = getattr(saving_data, "smart", None)
            if smart_data is not None:
                self.number_of_years = getattr(smart_data, "savingsRateIncreasePeriod", None)
                self.increase_amount = getattr(smart_data, "savingsRateIncreaseValue", None)
        self.dollar_or_percent = getattr(data, "smartIncrementDefinition", None)

    @before()
    @after
    def set_additional_parameters(self):
        pass

    @before()
    @after
    def validate(self):
        validator = SmartScheduleValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = SmartScheduleValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid
