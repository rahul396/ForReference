"""
Created on Jul 10, 2018

@author: anuarora
"""

from abc import ABC
from Models.ProcessValidator import ProcessValidator


class BaseCalculator(ABC):
    process_validator = ProcessValidator()
