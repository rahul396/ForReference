class SocialSecurity:
    def __init__(self, current_hh1_age, current_hh1_salary, hh1_retire_age, current_hh2_age, current_hh2_salary,
                 hh2_retire_age):
        self.hh1 = SocialSecurityIndividual(current_hh1_age, hh1_retire_age, current_hh1_salary)
        self.hh2 = SocialSecurityIndividual(current_hh2_age, hh2_retire_age, current_hh2_salary)


class SocialSecurityIndividual:
    def __init__(self, current_age, retire_age, current_salary):
        self.current_age = current_age
        self.retire_age = retire_age
        self.current_salary = current_salary
