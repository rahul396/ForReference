from Common.aop import after, before
from Models.BaseModel import BaseModel
from Models.CashflowValidator import CashflowValidator
import logging
import traceback


class Cashflow(BaseModel):
    def __init__(self, name=None, start_year=None, end_year=None, amount=None, context=None, inflate_to_start=True,
                 inflate_to_end=False, inflation_override_amount='', is_taxable=True):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.start_year = start_year
        self.end_year = end_year
        self.amount = amount
        self.context = context
        self.inflate_to_start = inflate_to_start
        self.inflate_to_end = inflate_to_end
        self.inflation = inflation_override_amount

    @before()
    @after
    def set_values(self, data):
        self.name = getattr(data, "account", None)
        self.start_year = getattr(data, "startYear", None)
        self.end_year = getattr(data, "endYear", None)
        self.amount = getattr(data, "amount", None)

    @before()
    @after
    def set_additional_parameters(self):
        try:
            self.inflation = [
                self.inflation, self.context.asset_class_properties_init.inflation][self.inflation == '']
            self.is_taxable = [True, False][self.amount < 0]
        except Exception as ex:
            self.LOG.exception("Error Occurred %s " % ex)
            #self.LOG.exception(traceback.format_exc())

    @before()
    @after
    def validate(self):
        validator = CashflowValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = CashflowValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

