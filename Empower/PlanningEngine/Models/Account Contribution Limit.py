import numpy as np
from Models.BaseModel import BaseModel
import logging
from Common.aop import before, after


class Account_Contribution_Limit(BaseModel):
    def __init__(self, context=None, limit_id=None):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.context = context
        self.limit_id = limit_id

    @before
    @after
    def set_values(self, val):
        pass

    @before
    @after
    def set_additional_parameters(self):
        temp_matrix = self.context.Account_Contribution_Limit_Initalization.limit_matrix
        temp_index = np.where(temp_matrix[:, 0] == self.limit_id)
        if temp_index is None:
            self.LOG.error("error: limit_id not found - ", self.limit_id)
        else:
            self.limit_id = temp_matrix[temp_index, 0]
            self.limit_amount = temp_matrix[temp_index, 1]
            self.limit_is_percent = temp_matrix[temp_index, 2]
            self.is_ee_only_limit = temp_matrix[temp_index, 3]
            self.is_govt_limit = temp_matrix[temp_index, 4]
            self.money_type_array = temp_matrix[temp_index, 5].split(',')

    @before
    @after
    def validate(self):
        return True

    @before
    @after
    def validate_additional_parameters(self):
        return True


