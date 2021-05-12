from Common import utils
from Models.BaseModel import BaseModel
from Common.aop import after, before
from Models.IndividualValidator import IndividualValidator
from SocialSecurity.SocialSecurityBenefitCalculator import SocialSecurityBenefitCalculator
from SocialSecurity.SocialSecurity import SocialSecurityIndividual
import logging
import traceback


class Individual(BaseModel):
    def __init__(self, name=None, date_of_birth=None, retire_age=None, gender=None, retirement_need=None,
                 retirement_need_type=None, context=None, health_state='good', account_array=[], job_array=[],
                 pension_array=[], ss_start_age='', ss_amount_override=''):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.context = context
        self.name = name
        self.date_of_birth = date_of_birth
        self.retire_age = retire_age
        self.gender = gender
        self.retirement_need_type = retirement_need_type
        self.retirement_need = retirement_need
        self.health_state = health_state
        self.account_array = account_array
        self.job_array = job_array
        self.mortality_init = context.mortality_init
        self.ss_start_age = ss_start_age
        self.ss_benefit = ss_amount_override
        self.pension_array = pension_array

    @before()
    @after
    def set_values(self, data):
        self.name = getattr(data, "firstName", None)
        self.date_of_birth = getattr(data, "birthDate", None)
        self.age = utils.age_calculator(self.date_of_birth)
        self.retire_age = getattr(data, "retirementAge", None)
        self.gender = getattr(data, "gender", None)
        retirement_need = getattr(data, 'retirementNeed', None)
        if retirement_need is not None:
            self.retirement_need = getattr(retirement_need, 'amount', None)

    @before()
    @after
    def set_additional_parameters(self):
        try:
            try:
                self.life_expectancy = self.get_life_expectancy()
            except Exception:
                self.life_expectancy = 78
            self.total_comp = self.get_total_earnings()
            self.set_ss_start_age(self.ss_start_age)
            if self.ss_benefit == '':
                self.ss_benefit = self.get_social_security_estimate()
        except Exception as e:
            self.LOG.exception("Error Occurred %s " % e)
            # self.LOG.exception(traceback.format_exc())

    @before()
    @after
    def validate(self):
        validator = IndividualValidator()
        validator.validate(self)
        return validator.is_valid

    @before()
    @after
    def validate_additional_parameters(self):
        validator = IndividualValidator()
        validator.validate_additional_parameters(self)
        return validator.is_valid

    def set_ss_start_age(self, ss_start_age, update_benefit=False):
        if ss_start_age == '':
            # self.ss_start_age = context.social_security_init.get_full_benefit_age(self.age)
            self.ss_start_age = max(self.retire_age, 62)
        else:
            self.ss_start_age = ss_start_age

        if update_benefit:
            self.ss_benefit = self.get_social_security_estimate()

    def get_life_expectancy(self):
        return self.context.mortality_init.get_life_expectancy(self.gender, self.age, self.health_state)

    def set_retire_age(self, retire_age):
        self.retire_age = retire_age
        self.get_years_to_retirement()
        self.set_ss_start_age(retire_age, True)

    def get_total_earnings(self):
        total_earnings = 0
        for job_iter in self.job_array:
            total_earnings += job_iter.current_earnings

        return total_earnings

    def get_social_security_estimate(self):
        socialSecurityIndividual = SocialSecurityIndividual(
            self.age, self.ss_start_age, self.total_comp)
        socialSecurityCalculator = SocialSecurityBenefitCalculator(
            self.context.social_security_df)
        return socialSecurityCalculator.get_benefit_amount(socialSecurityIndividual) * 12

    def set_pension_array(self, pension_array):
        self.pension_array = pension_array

    def get_years_to_retirement(self):
        return self.retire_age - self.age

    def get_retire_year(self):
        return 2018 + self.get_years_to_retirement()
