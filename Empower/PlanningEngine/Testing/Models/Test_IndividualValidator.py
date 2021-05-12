"""
Created on Jul 6, 2018

@author: anuarora
"""

from Models.Individual import Individual

individualObj1 = Individual("Account457B", "MutualFund", "Software Engineer", "98960-01", [])
individualObj2 = Individual(123, "MutualFund", "Software Engineer", "98960-01", [])


def test_validate_validValues():
    assert individualObj1.validate() == False


def test_validate_invalidValues():
    assert individualObj2.validate() == False
