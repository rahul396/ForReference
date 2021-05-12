"""
Created on Jul 11, 2018

@author: anuarora
"""

from Common.context import Context
from SocialSecurity.SocialSecurity import SocialSecurityIndividual
from SocialSecurity.SocialSecurityBenefitCalculator import SocialSecurityBenefitCalculator

context_obj = Context()
ssb = SocialSecurityBenefitCalculator(context_obj.social_security_df)


def test_get_benefit_amount():
    socialSecurityIndividual = SocialSecurityIndividual(24, 64, 90000)
    assert int(ssb.get_benefit_amount(socialSecurityIndividual)) == 2089
