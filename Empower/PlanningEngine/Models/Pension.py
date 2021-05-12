from Common.aop import after, before
from Models.BaseModel import BaseModel
from Common import utils
from Models.PensionValidator import PensionValidator
import logging


class Pension(BaseModel):
    def __init__(self, name=None, start_age=None, amount=None, context=None, is_taxable=True, inflate_to_start=True,
                 inflate_to_end=False, inflation_override_amount=''):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.start_age = start_age
        self.amount = amount
        self.context = context
        self.is_taxable = is_taxable
        self.inflate_to_start = inflate_to_start
        self.inflate_to_end = inflate_to_end
        self.inflation = [
            '', inflation_override_amount][inflation_override_amount == '']

    @before()
    @after
    def set_values(self, data):
        birth_date = getattr(data, "birthDate", None)
        if utils.birth_year_validator(birth_date):
            current_age = utils.age_calculator(birth_date)
        retire_age = getattr(data, "retirementAge", None)
        self.start_age = retire_age - current_age
        pension_data = None
        try:
            for pension in data.participantData.userCaseType.investor.pension:
                pension_data = pension
        except Exception as ex:
            self.LOG.exception("Error Occurred %s " % ex)
        if pension_data is not None:
            self.name = getattr(pension_data, "pensionID", None)
            self.amount = getattr(pension_data, "monthlyDollarBasis", None)

    @before()
    @after
    def set_additional_parameters(self):
        pass

    @before()
    @after
    def validate(self):
        validator = PensionValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = PensionValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

    def set_start_age(self, start_age):
        self.start_age = start_age

    def set_amount(self, amount):
        self.amount = amount
