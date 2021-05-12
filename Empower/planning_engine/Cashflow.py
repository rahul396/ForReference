class Cashflow(object):

    def __init__(self, id, start_year, end_year, amount, init_param, inflate_to_start = True, inflate_to_end = False, inflation_override_amount = '', is_taxable = True ):
        self.id = id
        self.start_year = start_year
        self.end_year = end_year
        self.amount = amount
        self.inflate_to_start = inflate_to_start
        self.inflate_to_end  = inflate_to_end
        if inflation_override_amount == '':
            self.inflation = init_param.acp.inflation
        else:
            self.inflation = inflation_override_amount

        if self.amount < 0:
            self.is_taxable = False
        else:
            self.is_taxable = is_taxable
