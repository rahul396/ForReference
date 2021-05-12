"""
Created on Jul 6, 2018

@author: anuarora
"""

from Models.Holding import Holding

holdingObj1 = Holding("Fixed Identifier", 0.070000, 0.950000, "Standard")
holdingObj2 = Holding(123, "Software Engineer", "98960-01")


def test_validate_validValues():
    assert holdingObj1.validate() == True


def test_validate_invalidValues():
    assert holdingObj2.validate() == False
