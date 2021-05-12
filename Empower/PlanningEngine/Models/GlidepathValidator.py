import logging
from Models.BaseValidator import BaseValidator

class GlidepathValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):
        return self.is_valid

    def validate_additional_parameters(self,data):
        return self.is_valid