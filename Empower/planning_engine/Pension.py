#stores information on a pension
class Pension(object):

    def __init__(self, id, start_age, amount, init_params,  is_taxable = True, inflate_to_start = True, inflate_to_end = False, inflation_override_amount = ''):
        self.id = id #used for output identification purposes only
        self.start_age = start_age
        self.amount = amount
        self.is_taxable = is_taxable
        # if inflate to start is set to true, the amount passed will stay constant (e.g. grow inline with inflation or 0 real growth)
        # if set to false, the amount will decrease by infaltion or chagne by the inflation override amount
        self.inflate_to_start = inflate_to_start
        #if set to true, the pension amount will stay constant (e.g. grow inline with inflation or 0 real growth)
        self.inflate_to_end  = inflate_to_end
        #all inflation overrides should be expressed in real terms
        if inflation_override_amount == '':
            self.inflation = ''
        else:
            self.inflation = inflation_override_amount

    #start year will be ovrriden a lot when retirement age is being solved for
    def set_start_age(self, start_age):
        self.start_age = start_age

    def set_amount(self, amount):
        self.amount = amount
