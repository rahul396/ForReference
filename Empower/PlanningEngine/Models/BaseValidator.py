"""
Created on Jul 10, 2018

@author: anuarora
"""
from abc import ABC, abstractmethod


class BaseValidator(ABC):
    exception_list = []
    is_valid = True

    @abstractmethod
    def validate(self, data):
        pass

    @abstractmethod
    def validate_additional_parameters(self,data):
        pass
