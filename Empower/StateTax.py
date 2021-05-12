import numpy as np
import pandas as pd


def calculate_state_tax(filename,taxable_income,state):
    tax_rate = get_state_tax_rates(filename,state)
    return taxable_income*tax_rate


def get_state_tax_rates(filename,state):
    taxrate_df = pd.read_excel(filename)
    state_row = taxrate_df.loc[taxrate_df['State']==state]
    try:
        tax_rate = state_row['Average Effective Tax Rate'].values[0]
    except Exception:
        print ('Column name Average Effective Tax Rate is not valid')
        print ('getting taxrate by row and column index....')
        tax_rate = state_row.values[0,1]
    return tax_rate

if __name__ == '__main__':
    filename = 'State Tax rates.xlsx'
    state_tax = calculate_state_tax(filename,200000,'NY')
    print (state_tax)