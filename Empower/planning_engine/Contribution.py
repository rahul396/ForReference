

class Contribution (object):

    def __init__(self, amount_or_percent, money_type, is_percent, account_name):
        self.amount_or_percent = amount_or_percent
        self.money_type = money_type
        self.is_percent = is_percent
        self.account_id = account_name
