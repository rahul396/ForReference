import helper
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas.tools.plotting import table
from fpdf import FPDF
import os



def main():
    # Get dataframe
    df = helper.create_dataframe('state_taxes.csv')
    pdf = FPDF()
    nrows = len(df)

    # add a new pdf page and display table in this page
    pdf.add_page()
    pdf.set_font('arial', 'B', 14)
    txt = "Table on a single page"
    pdf.cell(w=150,h=10,txt=txt,border=0,ln=1,align='C')
    if nrows>=30:
        helper.create_table(df.head(20),pdf)
    else:
        helper.create_table(df,pdf)

    # add a new pdf page and display chart in this page
    pdf.add_page()
    pdf.set_font('arial', 'B', 14)
    txt = "Chart on a single page"
    pdf.cell(w=150,h=10,txt=txt,border=0,ln=1,align='C')
    # image = helper.create_fig_from_plot(df,(10,8))
    image = helper.create_plotly_image()
    pdf.image(image,w = 150, h = 100)

    # add a new pdf page. Now display both the table and
    # chart on the same page. 
    pdf.add_page()
    new_df = df.head()
    pdf.set_font('arial', 'B', 14)
    txt = "Table and chart on a single page"
    pdf.cell(w=150,h=10,txt=txt,border=0,ln=1,align='C')
    helper.create_table(new_df,pdf)
    new_image = helper.create_fig_from_plot(new_df,(10,8))
    pdf.image(new_image,w=150,h=100)
    pdf.output('output.pdf', 'F')

    # remove the png files created
    os.remove(image)
    os.remove(new_image)
        
    return {'FileCreated':'output.pdf'}





if __name__ == '__main__':
    result = main()
    print (result)