from __future__ import division
from scipy.stats import bernoulli
import numpy as np
import sympy
from sympy.abc import x, z


def sample(p_true, n=10, ):
    'simulate coin flipping'
    return bernoulli(p_true).rvs(n)  # flip it n times with probability(true) = p_true


if __name__ == '__main__':
    xs = sample(1 / 2, 20)
    print xs

    p = sympy.symbols('p', positive=True)

    L = (p ** x) * ((1 - p) ** (1 - x))
    J = np.prod([L.subs(x, i) for i in xs])  # objective function to maximize
