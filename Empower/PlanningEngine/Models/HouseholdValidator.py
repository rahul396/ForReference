import logging
from Models.BaseValidator import BaseValidator
from Common import utils, config


class HouseholdValidator(BaseValidator):
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)

    def validate(self, data):

        data.exception_list = []

        if data.head_of_household_array is not None:
            pass
        else:
            data.exception_list.append("%s is not valid" % "HoH Array")

        if data.state_of_residence is not None and utils.is_string(data.state_of_residence):
            pass
        else:
            data.exception_list.append("%s is not valid" % "State of Residence")

        if len(data.exception_list) > 0:
            data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_additional_parameters(self, data):
        # Check for atleast one joing year of retirement
        if self.validate_joint_year_of_retirement(data.head_of_household_array):
            pass
        else:
            data.exception_list.append("%s is not valid." % "Joint year of retirement")

        # Cashflows don’t start after household life expectancy (max of two HOHs)
        for cashflow in data.cashflow_array:
            if cashflow.start_year <= config.current_year + data.max_periods_alive:
                pass
            else:
                data.exception_list.append("%s is not valid." % "Cashflow start year")

        if len(data.exception_list) > 0:
            # Don't want the process to stop
            # data.is_valid = False
            utils.exception_logger(data.exception_list, self.LOG)

        return data.is_valid

    def validate_joint_year_of_retirement(self, head_of_household_array):
        """
        Will validate that one HOH doesn't die before the other one retires.
        :param head_of_household_array: array of two Individuals
        :return: Boolean
        """
        individual_1 = head_of_household_array[0]
        individual_2 = head_of_household_array[1]

        if individual_1.life_expectancy < individual_2.life_expectancy:
            if individual_2.retire_age <= individual_1.life_expectancy:
                return True
            else:
                return False

        elif individual_2.life_expectancy < individual_1.life_expectancy:
            if individual_1.retire_age <= individual_2.life_expectancy:
                return True
            else:
                return False

        else:
            if individual_1.retire_age <= individual_2.life_expectancy or individual_2.retire_age <= individual_1.life_expectancy:
                return True
            else:
                return False
