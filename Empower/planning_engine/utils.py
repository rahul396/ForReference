import time
import numpy as np
from datetime import datetime
#import tensorflow as tf
import pandas as pd
import os


def print_time_difference(start_time, end_time, term= 'ms'):
    if term =='ms':
        print(np.around((end_time - start_time)*1000, decimals = 3), "ms")
    elif term == 's':
        print(np.around((end_time - start_time), decimals = 2), "seconds")
    elif term == 'm':
        print(np.around((end_time - start_time)/60, decimals = 0), "minutes")



def calculate_date_dif(date1, date2 = datetime.now(), return_type = 'years'):
    if return_type.strip().lower() == 'years':
        return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

def interpolate_calculation(x_value, x_coords, y_coords):
    return np.interp(x_value, x_coords, y_coords)

def find_row_in_list(my_list, my_item):
    for r, c in enumerate(my_list):
        if my_item in c:
            return (r)

def output_to_excel(np_array,init_params, output_name ):

    df = pd.DataFrame(np_array)
    df.to_csv(os.path.join(init_params.default_output_location, output_name) )



def test_this():


    x = tf.Variable(5000000, name='x', dtype=tf.float32)
    x_squared = tf.square(x)

    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(x_squared)

    init = tf.global_variables_initializer()

    with tf.Session() as session:
        session.run(init)
        print("starting at", "x:", session.run(x), "log(x)^2:", session.run(x_squared))
        for step in range(10):
            print("int here")
            session.run(train)
            print("step", step, "x:", session.run(x), "log(x)^2:", session.run(x_squared))



#test_this()
