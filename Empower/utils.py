import numpy as np


def interpolate_calculation(x_value, x_coords, y_coords):
    # print x_coords
    # print y_coords
    return np.interp(x_value, x_coords, y_coords)
