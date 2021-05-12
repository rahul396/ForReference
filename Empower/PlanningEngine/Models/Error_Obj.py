import pandas as pd


class Error_Obj(object):
    def __init__(self, output_file_location=""):
        self.output_file_location = output_file_location
        self.error_log = pd.DataFrame(
            columns=["Error Type", "Error Location", "Error Message", "Error Write Time"])

    def add_error(self, e_type, e_location, e_message):

        if e_type == 'critical':
            print("In - " + e_location +
                  " the following critical error occured  " + e_message)
            raise RuntimeError()
        if e_type == 'warning':
            print("In - ", e_location,
                  " the following warning occured  ", e_message)
