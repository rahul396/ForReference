import pandas as pd
import numpy as np

def get_dataframe(file_path_and_name_with_ext, ip_sheet_num):
    try:
        xlfile = pd.ExcelFile(file_path_and_name_with_ext)
    except FileNotFoundError as e:
        print ('File not found')
    xlsheet_df = xlfile.parse(ip_sheet_num)

    return xlsheet_df
