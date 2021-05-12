"""
Created on Jul 6, 2018

@author: anuarora
"""
from Models.BaseValidator import BaseValidator


class ProcessValidator(BaseValidator):
    def validate_social_security_input(self, socialSecurityIndividual):
        current_age = socialSecurityIndividual.current_age
        retire_age = socialSecurityIndividual.retire_age
        current_salary = socialSecurityIndividual.current_salary
        is_valid = True
        error_values = {}
        # if not current_age in range(15, 26):
        #     is_valid = False
        #     error_values.update({'current_age': current_age})
        if current_salary < 20000 or current_salary > 127200:
            is_valid = False
            error_values.update({'current_salary': current_salary})
        if retire_age not in range(62, 86):
            is_valid = False
            error_values.update({'retire_age': retire_age})

        return (is_valid, error_values)

    def validate(self, data):

        return data.is_valid

    def validate_additional_parameters(self,data):
        return True
