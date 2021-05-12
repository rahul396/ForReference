"""
Created on Jul 6, 2018

@author: anuarora
"""

from Models.Account import Account

accountObj1 = Account("Account457B", "MutualFund", "Software Engineer", "98960-01", [])
accountObj2 = Account(123, "MutualFund", "Software Engineer", "98960-01", [])


def test_validate_validValues():
    assert accountObj1.validate() == True


def test_validate_invalidValues():
    assert accountObj2.validate() == False
