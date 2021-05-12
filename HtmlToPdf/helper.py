import pandas as pd
from matplotlib import pyplot as plt
from pandas.tools.plotting import table
import random
import plotly as py
import plotly.plotly as plty
import plotly.graph_objs as go
import ipywidgets as widgets
import numpy as np
from scipy import special



def create_dataframe(filename):
    filename = 'resources/'+filename
    df = pd.read_csv(filename)
    return df


# def create_fig_from_table(df,figsize,filename):
#     plt.figure(figsize=figsize)
#     ax = plt.subplot(111,frame_on=False)
#     col_width = (figsize[0]-2)/(10*len(df.columns))
#     ax.xaxis.set_visible(False)  # hide the x axis
#     ax.yaxis.set_visible(False)  # hide the y axis
#     t = table(ax,df,loc='center', colWidths=[col_width]*len(df.columns))
#     t.auto_set_font_size(False) # Activate set fontsize manually
#     t.set_fontsize(8) # if ++fontsize is necessary ++colWidths
#     # t.scale(1.2, 1.2) # change size table
#     plt.savefig(filename)
#     plt.close()

def create_plotly_image():
    #py.offline.init_notebook_mode(connected=True)

    x = np.linspace(-3*np.pi,3*np.pi,1000)

    layout = go.Layout(
        title='Sinusoidal function',
        yaxis=dict(
            title='sin(x)'
        ),
        xaxis=dict(
            title='x'
        )
    )

    trace1 = go.Scatter(
        x=x,
        y=np.sin(x),
        mode='lines+markers',
        name='sin(x)',
        line=dict(
            shape='spline'
        )
    )
    fig = go.Figure(data=[trace1],layout=layout)
    #fig = {'data':[trace1],'layout':layout}
    #py.offline.plot(fig,image = 'png',filename='.\images\plot_image', image_width=800, image_height=600, validate=False)
    suffix = random.randint(1,200)
    filename = 'images/output_'+str(suffix)+'.png'
    plty.image.save_as(fig,filename)
    return filename


def create_fig_from_plot(df,figsize):
    suffix = random.randint(1,200)
    filename = 'images/output_'+str(suffix)+'.png'
    plt.figure(figsize=figsize)
    # ax = plt.subplot(subplot,frame_on=False)
    df[:30].plot(kind='line')
    plt.savefig(filename)
    plt.close()
    return filename

def create_table(df,pdf):
    cell_width = 35
    cell_height = 8

    pdf.set_font('arial', 'B', 8)
    # Create header for table with Bold text
    for col in df.columns:
        pdf.cell(w=cell_width, h=10, txt=str(col),border=1, ln=0, align= 'C')
    pdf.cell(w=cell_width,h=cell_height,border=0,ln=1,align='C')

    pdf.set_font('arial', '', 7)
    # Create data rows with normal text
    for i in range(0, len(df)):
        for col in df.columns:
            pdf.cell(w=cell_width, h=10, txt=str(df[col].ix[i]),border='LRB', ln=0, align= 'C')
        pdf.cell(w=cell_width,h=cell_height,border=0,ln=1,align='C')
    
    # Add a margin for next element 
    pdf.cell(90, 10, " ", 0, 2, 'C')

