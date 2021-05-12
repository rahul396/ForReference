from abc import ABC, abstractmethod


class BaseModel(ABC):
    is_valid = True
    exception_list = []

    @abstractmethod
    def set_values(self, val):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def validate_additional_parameters(self):
        pass