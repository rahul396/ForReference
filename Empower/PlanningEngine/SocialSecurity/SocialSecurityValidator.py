import logging

from Models.BaseValidator import BaseValidator


class SocialSecurityValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, socialSecurityIndividual):
        current_age = socialSecurityIndividual.current_age
        retire_age = socialSecurityIndividual.retire_age
        current_salary = socialSecurityIndividual.current_salary
        error_values = {}
        '''Not required at this time. Will update once the criteria is known.
        
        if not current_age in range(15, 26):
            self.is_valid = False
            error_values.update({'current_age': current_age})

        '''

        if current_salary < 20000 or current_salary > 127200:
            self.is_valid = False
            error_values.update({'current_salary': current_salary})

        if retire_age not in range(62, 86):
            self.is_valid = False
            error_values.update({'retire_age': retire_age})

        if not self.is_valid:
            self.LOG.exception('Invalid input(s) for SocialSecurityIndividual: ' + str(error_values))
            raise ValueError('Invalid input(s) for SocialSecurityIndividual: ' + str(error_values))

        return self.is_valid
