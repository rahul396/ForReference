"""
Created on Jul 11, 2018

@author: anuarora
"""

from Common import utils


def test_birth_year_validator_with_accepted_format():
    assert utils.birth_year_validator("02-08-1990") == True


def test_birth_year_validator_with_unaccepted_format():
    assert utils.birth_year_validator("02-1990-08") == False


def test_is_int():
    assert utils.is_int(45) == True


def test_is_string():
    assert utils.is_string(45) == False


def test_is_non_negative():
    assert utils.is_non_negative(-35) == False


def test_age_calculator_today():
    assert utils.age_calculator('07-12-2018') == None


def test_age_calculator():
    assert utils.age_calculator('02-08-1990') == 28
