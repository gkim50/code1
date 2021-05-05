# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 18:34:57 2021

@author: 37092
"""

import base64
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import datetime
from datetime import datetime as dt
import io
import os
import pandas as pd
import re
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
import webbrowser
import plotly.graph_objects as go
from sklearn.cluster import KMeans

from fpdf import FPDF
import plotly.express as px
import plotly
import os


# Create instance of FPDF class
# Letter size paper, use inches as unit of measure
pdf=FPDF(format='letter', unit='in')
pdf2=FPDF(format='letter', unit='in')
pdf3=FPDF(format='letter', unit='in')
pdf4=FPDF(format='letter', unit='in')
pdf5=FPDF(format='letter', unit='in')

pdf.set_margins(0.7,0.5,1)

 
# Add new page. Without this you cannot create the document.
pdf.add_page()
pdf2.add_page()
pdf3.add_page()
pdf4.add_page()
pdf5.add_page()

# Remember to always put one of these at least once.
pdf.set_font('Times','',10.0)
pdf2.set_font('Times','',10.0) 
pdf3.set_font('Times','',10.0) 
pdf4.set_font('Times','',10.0) 
pdf5.set_font('Times','',10.0) 



# Effective page width, or just epw
epw = pdf.w - 2*pdf.l_margin
epw = pdf3.w - 2*pdf3.l_margin

# Set column width to 1/4 of effective page width to distribute content 
# evenly across table and page
col_width = epw/10


Battery_Info = pd.read_excel(r'C:\Users\cheri\OneDrive\Desktop\SRP_Software\source_data\ASUDC Metering Study Data20191103222705\Battery Info.xlsx')
Component_Info = pd.read_excel(r'C:\Users\cheri\OneDrive\Desktop\SRP_Software\source_data\ASUDC Metering Study Data20191103222705\Component Info.xlsx')\
.drop(columns=[ 'IsSystemRemoved', 'CancelledDate', 'ApplicationStatus'])
Customer_Meta_Data = pd.read_excel(r'C:\Users\cheri\OneDrive\Desktop\SRP_Software\source_data\Customer Meta Data.xlsx')
rate_plan = pd.read_csv(r'C:\Users\cheri\OneDrive\Desktop\ss\ASU Customer Rate Plans.csv')
kWh_date_info_2A = pd.read_csv(r'C:\Users\cheri\OneDrive\Desktop\ss\kWh_date_info_2A.csv')
kWh_date_info_2B = pd.read_csv(r'C:\Users\cheri\OneDrive\Desktop\ss\kWh_date_info_2B.csv')
Battery_Info.EssDerConfiguration = Battery_Info.EssDerConfiguration.astype(str)
rate_plan = rate_plan.drop_duplicates()
location_1B_info = Battery_Info[Battery_Info.EssDerConfiguration == '1B']
location_1C_info = Battery_Info[Battery_Info.EssDerConfiguration == '1C']
location_2A_info = Battery_Info[Battery_Info.EssDerConfiguration == '2A']
location_2B_info = Battery_Info[Battery_Info.EssDerConfiguration == '2B']
location_3A_info = Battery_Info[Battery_Info.EssDerConfiguration == '3A']
location_3C_info = Battery_Info[Battery_Info.EssDerConfiguration == '3C']

location_1B_info_1 = location_1B_info.merge(Customer_Meta_Data, \
                     on=['LocationNumber', 'EssDerConfiguration', 'CommissioningDate']).drop_duplicates()
Component_Info_1B = Component_Info[Component_Info.LOCATN_K.isin(location_1B_info_1.LocationNumber)]
location_1C_info_1 = location_1C_info.merge(Customer_Meta_Data, 
                     on=['LocationNumber', 'EssDerConfiguration', 'CommissioningDate']).drop_duplicates()
Component_Info_1C = Component_Info[Component_Info.LOCATN_K.isin(location_1C_info_1.LocationNumber)]
location_2A_info_1 = location_2A_info.merge(Customer_Meta_Data, \
                     on=['LocationNumber', 'EssDerConfiguration', 'CommissioningDate']).drop_duplicates()
Component_Info_2A = Component_Info[Component_Info.LOCATN_K.isin(location_2A_info_1.LocationNumber)]
location_2B_info_1 = location_2B_info.merge(Customer_Meta_Data, \
                     on=['LocationNumber', 'EssDerConfiguration', 'CommissioningDate']).drop_duplicates()
Component_Info_2B = Component_Info[Component_Info.LOCATN_K.isin(location_2B_info_1.LocationNumber)]
location_3A_info_1 = location_3A_info.merge(Customer_Meta_Data, \
                     on=['LocationNumber', 'EssDerConfiguration', 'CommissioningDate']).drop_duplicates()
Component_Info_3A = Component_Info[Component_Info.LOCATN_K.isin(location_3A_info_1.LocationNumber)]
location_3C_info_1 = location_3C_info.merge(Customer_Meta_Data, \
                     on=['LocationNumber', 'EssDerConfiguration', 'CommissioningDate']).drop_duplicates()
Component_Info_3C = Component_Info[Component_Info.LOCATN_K.isin(location_3C_info_1.LocationNumber)]

rate_plan_1B = rate_plan[rate_plan.LOCATN_K.isin(location_1B_info_1.LocationNumber)]
rate_plan_1C = rate_plan[rate_plan.LOCATN_K.isin(location_1C_info_1.LocationNumber)]
rate_plan_2A = rate_plan[rate_plan.LOCATN_K.isin(location_2A_info_1.LocationNumber)]
rate_plan_2B = rate_plan[rate_plan.LOCATN_K.isin(location_2B_info_1.LocationNumber)]
rate_plan_3A = rate_plan[rate_plan.LOCATN_K.isin(location_3A_info_1.LocationNumber)]
rate_plan_3C = rate_plan[rate_plan.LOCATN_K.isin(location_3C_info_1.LocationNumber)]

rate_info_1B = []
rate_plan_1B_Loc_N = rate_plan_1B.groupby('LOCATN_K')
for group in rate_plan_1B_Loc_N:
    tmp = group[1].sort_values(by=['DATE'])
    # print(np.unique(tmp.RATE))
    for rate in np.unique(tmp.RATE):
        tmp1 = tmp[tmp.RATE == rate].sort_values(by=['DATE'])
        rate_info_1B.append([str(int(np.unique(tmp1.LOCATN_K))), tmp1.DATE.iloc[0], tmp1.DATE.iloc[-1], rate])
rate_plan_info_1B = pd.DataFrame(rate_info_1B, columns=['LOCATN_K', 'START_DATE', 'END_DATE', 'RATE'])
rate_info_1C = []
rate_plan_1C_Loc_N = rate_plan_1C.groupby('LOCATN_K')
for group in rate_plan_1C_Loc_N:
    tmp = group[1].sort_values(by=['DATE'])
    # print(np.unique(tmp.RATE))
    for rate in np.unique(tmp.RATE):
        tmp1 = tmp[tmp.RATE == rate].sort_values(by=['DATE'])
        rate_info_1C.append([str(int(np.unique(tmp1.LOCATN_K))), tmp1.DATE.iloc[0], tmp1.DATE.iloc[-1], rate])
rate_plan_info_1C = pd.DataFrame(rate_info_1C, columns=['LOCATN_K', 'START_DATE', 'END_DATE', 'RATE'])
rate_info_2A = []
rate_plan_2A_Loc_N = rate_plan_2A.groupby('LOCATN_K')
for group in rate_plan_2A_Loc_N:
    tmp = group[1].sort_values(by=['DATE'])
    # print(np.unique(tmp.RATE))
    for rate in np.unique(tmp.RATE):
        tmp1 = tmp[tmp.RATE == rate].sort_values(by=['DATE'])
        rate_info_2A.append([str(int(np.unique(tmp1.LOCATN_K))), tmp1.DATE.iloc[0], tmp1.DATE.iloc[-1], rate])
rate_plan_info_2A = pd.DataFrame(rate_info_2A, columns=['LOCATN_K', 'START_DATE', 'END_DATE', 'RATE'])
rate_info_2B = []
rate_plan_2B_Loc_N = rate_plan_2B.groupby('LOCATN_K')
for group in rate_plan_2B_Loc_N:
    tmp = group[1].sort_values(by=['DATE'])
    # print(np.unique(tmp.RATE))
    for rate in np.unique(tmp.RATE):
        tmp1 = tmp[tmp.RATE == rate].sort_values(by=['DATE'])
        rate_info_2B.append([str(int(np.unique(tmp1.LOCATN_K))), tmp1.DATE.iloc[0], tmp1.DATE.iloc[-1], rate])
rate_plan_info_2B = pd.DataFrame(rate_info_2B, columns=['LOCATN_K', 'START_DATE', 'END_DATE', 'RATE'])
rate_info_3A = []
rate_plan_3A_Loc_N = rate_plan_3A.groupby('LOCATN_K')
for group in rate_plan_3A_Loc_N:
    tmp = group[1].sort_values(by=['DATE'])
    # print(np.unique(tmp.RATE))
    for rate in np.unique(tmp.RATE):
        tmp1 = tmp[tmp.RATE == rate].sort_values(by=['DATE'])
        rate_info_3A.append([str(int(np.unique(tmp1.LOCATN_K))), tmp1.DATE.iloc[0], tmp1.DATE.iloc[-1], rate])
rate_plan_info_3A = pd.DataFrame(rate_info_3A, columns=['LOCATN_K', 'START_DATE', 'END_DATE', 'RATE'])
rate_info_3C = []
rate_plan_3C_Loc_N = rate_plan_3C.groupby('LOCATN_K')
for group in rate_plan_3C_Loc_N:
    tmp = group[1].sort_values(by=['DATE'])
    # print(np.unique(tmp.RATE))
    for rate in np.unique(tmp.RATE):
        tmp1 = tmp[tmp.RATE == rate].sort_values(by=['DATE'])
        rate_info_3C.append([str(int(np.unique(tmp1.LOCATN_K))), tmp1.DATE.iloc[0], tmp1.DATE.iloc[-1], rate])
rate_plan_info_3C = pd.DataFrame(rate_info_3C, columns=['LOCATN_K', 'START_DATE', 'END_DATE', 'RATE'])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
     "text-align": "center",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
     "text-align": "center",
}

def generate_plot():
    global fig0
    fig0= go.Figure()
    fig0 = go.Scatter(x=date.tolist(), y=dataset.values[:, 5:].flatten().tolist())
    fig0.update_layout(title='Time series smart meter data',title_x=0.3, xaxis_title='Date',yaxis_title='Value',font=dict(size=18))
    return fig0
'''

        xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Date",
            font=dict(
                family="Courier New, monospace",
                size=30,
                color="#7f7f7f"
            )
        )
    ),
        yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Value",
            font=dict(
                family="Courier New, monospace",
                size=30,
                color="#7f7f7f"
            )
        )
    ),)),
'''


def generate_plot1(mea_type):
    global fig, fig_0
    fig = px.histogram(df[df['CHNM'] == mea_type].iloc[:,2:].to_numpy().flatten())
    if mea_type == 'Voltage Phase A':
        x_label = 'Voltage value'
    else:
        x_label = 'Kwh value'
    fig.update_layout(title='Histogram of ' + mea_type, title_x=0.5, xaxis_title=x_label,yaxis_title='Frequency',font=dict( size=18))
    fig.update_xaxes(rangeslider_visible=True)
    plotly.io.write_image(fig,file='fig.png',format='png',width=700, height=450)
    fig_0= (os.getcwd()+'/'+"fig.png")

    return fig

def generate_plot2(mea_type):
    global fig1, fig_1
    fig1= px.box(df[df['CHNM'] == mea_type].iloc[:,2:].to_numpy().flatten())
    if mea_type == 'Voltage Phase A':
        x_label = 'Voltage value'
    else:
        x_label = 'Kwh value'
    fig1.update_layout(title='Boxplot of ' + mea_type,title_x=0.5,  xaxis_title=mea_type,yaxis_title=x_label,font=dict( size=18))    
    plotly.io.write_image(fig1,file='fig1.png',format='png',width=700, height=450)
    fig_1=(os.getcwd()+'/'+"fig1.png")

    return fig1


def generate_plot5(data, value):
    global fig4, fig_4
    fig4= go.Figure()
    for i in range(data.shape[0]):
        name_for_legend = data.values[i, :5].flatten().tolist()
        name_for_legend = [str(j) for j in name_for_legend]
        fig4.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data.values[i, 5:].flatten().tolist(),
                                 name=', '.join(name_for_legend)))
    fig4.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=((980+value)*np.ones(96)).tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 0.5, dash = 'dash')) )
    fig4.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=((980-value)*np.ones(96)).tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 0.5, dash = 'dash')) )
    fig4.update_layout(title='Time series smart meter data',title_x=0.3, xaxis_title='Time Index of a Day',yaxis_title='Data',font=dict(size=18))
    plotly.io.write_image(fig4, file='fig4.png',format='png',width=1980, height=1080)
    fig_4=(os.getcwd()+'/'+"fig4.png")

    return fig4

def generate_plot6(data, value):
    global fig5, fig_5
    fig5= go.Figure()
    for i in range(data.shape[0]):
        name_for_legend = data.values[i, :5].flatten().tolist()
        name_for_legend = [str(j) for j in name_for_legend]
        fig5.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data.values[i, 5:].flatten().tolist(),
                                 name=', '.join(name_for_legend)))
    fig5.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=((value)*np.ones(96)).tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 0.5, dash = 'dash')) )
    fig5.update_layout(title='Time series smart meter data', title_x=0.3, xaxis_title='Time Index of a Day',yaxis_title='Data',font=dict( size=18))
    plotly.io.write_image(fig5, file='fig5.png',format='png',width=1980, height=1080)
    fig_5=(os.getcwd()+'/'+"fig5.png")

    return fig5


def generate_plot7(data1_plot7, data2_plot7, data3_plot7, data4_plot7):
    global fig6, fig_6
    fig6= go.Figure()
    for i in range(data1_plot7.shape[0]):
        fig6.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data1_plot7.values[i, :96].flatten().tolist(),
                                  ))
        fig6.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data2_plot7.values[i, :96].flatten().tolist(),
                                 ))

    fig6.update_traces({"line":{"color":"#8F8F8F", "width": 0.5}})
    fig6.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data3_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 3, dash = 'dash')) )
    fig6.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data4_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(0,0,255)'), width = 3, dash = 'dash')) )    

    fig6.update_layout(
        title_text = 'The First Behavior Pattern', title_x=0.5,
        xaxis_title='Time Index of a Day',
        yaxis_title='Data',
        font=dict(size=18))
    plotly.io.write_image(fig6, file='fig6.png',format='png',width=1980, height=1080)
    fig_6=(os.getcwd()+'/'+"fig6.png")

    return fig6

def generate_plot8(data1_plot8, data2_plot8, data3_plot8, data4_plot8):
    global fig7, fig_7
    fig7= go.Figure()
    for i in range(data1_plot8.shape[0]):
        fig7.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data1_plot8.values[i, :96].flatten().tolist(),
                                  ))
        fig7.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data2_plot8.values[i, :96].flatten().tolist(),
                                 ))

    fig7.update_traces({"line":{"color":"#8F8F8F", "width": 0.5}})
    fig7.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data3_plot8.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 3, dash = 'dash')) )
    fig7.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data4_plot8.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(0,0,255)'), width = 3, dash = 'dash')) )    

    fig7.update_layout(
        title_text = 'The Second Behavior Pattern', title_x=0.5,
        xaxis_title='Time Index of a Day',
        yaxis_title='Data',
        font=dict(size=18))
    plotly.io.write_image(fig7, file='fig7.png',format='png',width=1980, height=1080)
    fig_7=(os.getcwd()+'/'+"fig7.png")

    return fig7

def generate_plot9(data1_plot9, data2_plot9, data3_plot9, data4_plot9):
    global fig8,fig_8
    fig8= go.Figure()
    for i in range(data1_plot9.shape[0]):
        fig8.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data1_plot9.values[i, :96].flatten().tolist(),
                                  ))
        fig8.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data2_plot9.values[i, :96].flatten().tolist(),
                                 ))

    fig8.update_traces({"line":{"color":"#8F8F8F", "width": 0.5}})
    fig8.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data3_plot9.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 3, dash = 'dash')) )
    fig8.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data4_plot9.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(0,0,255)'), width = 3, dash = 'dash')) )    

    fig8.update_layout(
        title_text = 'The Third Behavior Pattern', title_x=0.5,
        xaxis_title='Time Index of a Day',
        yaxis_title='Data',
        font=dict(size=18))
    plotly.io.write_image(fig8, file='fig8.png',format='png',width=1980, height=1080)
    fig_8=(os.getcwd()+'/'+"fig8.png")

    return fig8

def generate_plot10(data3_plot7, data4_plot7, data_5_plot7, data_8_plot7):
    global fig9
    fig9= go.Figure()
    for i in range(data_5_plot7.shape[0]):
        fig9.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data_5_plot7.values[i, :96].flatten().tolist(),
                                  ))
        fig9.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data_8_plot7.values[i, :96].flatten().tolist(),
                                 ))

    fig9.update_traces({"line":{"color":"orange", "width": 0.5}})
    fig9.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data3_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 3, dash = 'dash')) )
    fig9.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data4_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(0,0,255)'), width = 3, dash = 'dash')) )    

    fig9.update_layout(
        title_text = 'The Data of the First Abnormal Customer in the First Behavior Pattern', title_x=0.5,
        xaxis_title='Time Index of a Day',
        yaxis_title='Data',
        font=dict(size=18))    
    return fig9

def generate_plot11(data3_plot7, data4_plot7, data_5_plot7, data_8_plot7):
    global fig10
    fig10= go.Figure()
    for i in range(data_5_plot7.shape[0]):
        fig10.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data_5_plot7.values[i, :96].flatten().tolist(),
                                  ))
        fig10.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data_8_plot7.values[i, :96].flatten().tolist(),
                                 ))

    fig10.update_traces({"line":{"color":"green", "width": 0.5}})
    fig10.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data3_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 3, dash = 'dash')) )
    fig10.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data4_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(0,0,255)'), width = 3, dash = 'dash')) )    

    fig10.update_layout(
        title_text = 'The Data of the Second Abnormal Customer in the First Behavior Pattern', title_x=0.5,
        xaxis_title='Time Index of a Day',
        yaxis_title='Data',
        font=dict(size=18))    
    return fig10

def generate_plot12(data3_plot7, data4_plot7, data_5_plot7, data_8_plot7):
    global fig11
    fig11= go.Figure()
    for i in range(data_5_plot7.shape[0]):
        fig11.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data_5_plot7.values[i, :96].flatten().tolist(),
                                  ))
        fig11.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), 
                                  y=data_8_plot7.values[i, :96].flatten().tolist(),
                                 ))

    fig11.update_traces({"line":{"color":"cyan", "width": 0.5}})
    fig11.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data3_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(205, 12, 24)'), width = 3, dash = 'dash')) )
    fig11.add_trace(go.Scatter(x=np.linspace(0,95,96).tolist(), y=data4_plot7.tolist(), mode = 'lines',
                   line = dict(color = ('rgb(0,0,255)'), width = 3, dash = 'dash')) )    

    fig11.update_layout(
        title_text = 'The Data of the Third Abnormal Customer in the First Behavior Pattern', title_x=0.5,
        xaxis_title='Time Index of a Day',
        yaxis_title='Data',
        font=dict(size=18))    
    return fig11


# initialize the application
app = dash.Dash()

# define the layout of the app

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        html.Div(id="output-clientside"),
        html.Div([html.Div([
                        html.Img(
                            src=app.get_asset_url("dash-srp.png"),
                            id="plotly-image",
                            style={
                                "height": "220px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )],
                    className="two columns",
                ),
                html.Div([
                        html.Div([
                                html.H1(
                                    "Big Data Analytics Software for Smart Meter Status Monitoring and Situational Awareness",
                                    style = dict(textAlign = 'center')
                                ),
                                html.H2(
                                    "SRP-ASU Collaboration", 
                                    style = dict(textAlign = 'center')
                                ),
                                html.Hr(),
                            ])
                    ],
                    className="eight columns",
                    id="title",
                ),

    html.Div(id='output-provider'),
                 
        ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
    html.Div([
                html.H3("Goal"),
                html.P("The software is developed to visualize various sources of information, give indications to mismatch records, meter communication\
                       issues, special or suspect events, and conduct machine learning, such as clustering and forecasting on smart meter data." ,
                    style={"color": "#000000"},
                    className="row"),
                    html.Br(),
                 html.H3("Main functions"),
                    html.Li(
                    "<Uploading Files>: Let users to upload data for visualization and big data analytics."),
                    html.Li(
                    "<Data Visualizations>: Visualize the data for the overall knowledge check."),
                    html.Li(
                    "<Distribution Visualizations>: Gain more data insights from statistical learning."), 
                    html.Li(
                    "<Bad Data Indicator>: Find and indicate inconsistent data information."),
                    html.Li(
                    "<Behavior Analysis>: Analyze user behavior for abnormal patterns."),
                    html.Li(
                    "<AC Failing Prediction / EV Level>: Future functions on AC failing prediction and EV level prediction (next project). "),
   
            ],
            className="product",
        ),

   
    html.Div(
    [
        html.H2("Navigation", className="display-4"),
        html.Br(),
        html.Hr(),

        html.Br(),

        dbc.Nav(
            [            
    html.A('User Manual', download='readme.pdf', href= '/assets/readme1.pdf' )

            ],
      
        ),
    ],
    style=SIDEBAR_STYLE,
),                    
    ########################### title end ##########################
    ########################### tabs begin ##########################
   html.Div([
        dcc.Tabs(id='tabs_example', value='tab-1',        parent_className='custom-tabs',
        className='custom-tabs-container',
                 children=[
                     dcc.Tab(label='Uploading Files', value='tab-1',                className='custom-tab',
                selected_className='custom-tab--selected'),
                     dcc.Tab(label='Data Visualizations', value='tab-2',                className='custom-tab',
                selected_className='custom-tab--selected'),
                     dcc.Tab(label='Distribution Visualizations', value='tab-3',                className='custom-tab',
                selected_className='custom-tab--selected'),
                     dcc.Tab(label='Bad Data Indicator', value='tab-4',                className='custom-tab',
                selected_className='custom-tab--selected'),
                     dcc.Tab(label='Behavior Analysis', value='tab-5',                className='custom-tab',
                selected_className='custom-tab--selected'),
                     dcc.Tab(label='AC Failing / EV Level Prediction (in future)', value='tab-6',                className='custom-tab',
                selected_className='custom-tab--selected'),
                     ], style={'font-size': '3rem', 'margin-top': '-15px','height': '150px','lineHeight': '40px'} ),
        html.Div(id='tabs-example-content')]),
],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},               
)
########################### front page end ##########################

######## call to show contents in the table
@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs_example', 'value'))

########################## process the file #########################

def render_content(tab):
    global meter_data_B_kWh_2B_27_minmax, meter_data_B_kWh_2B_27_minmax_pred
    if tab == 'tab-1':       
        return html.Div([
                
            html.Div([html.P("In this tab, you can upload a file, view the file,   \
                             and filter some specific information from the file."),],
                             className="bare_container",),
                html.Div(
                    [html.P("* Please upload a smart meter data file \
                             that you would like to analyze"),
                         dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                html.A('Drag or Select Files'),
                          ]),
                            style={
                                'width': '99%',
                                'height': '380px',
                                'lineHeight': '390px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '15px',
                                'textAlign': 'center',
                                'margin': '15px'
                          },
                                # multiple=True
                          ),],
                    className="bare_container",
                    id="cross-filter-options",
                ),
            html.Div([html.H2("Description"),
                 html.Li( "The file needs to contain exactly the keys listed."),
                 html.Li( "LOCATN_K: The unique ID of a customer."),
                 html.Li( "APCODE: The code for smart meter, options are Z, B, S, \
                         where Z indicates a billing meter, B indicates a battery \
                         meter, and S indicates a solar meter. "),
                 html.Li( "METER: The name of the smart meter, options are BILLING, \
                         DER_STORAGE, DER_GEN, where BILLING indicates a billing meter, \
                         DER_STORAGE indicates a battery meter, and DER_GEN indicates \
                         a solar meter."),
                 html.Li( "CHNM: The types of the measured data, options are \
                         kWh - Delivered, kWh - Received, and Voltage Phase A, \
                         where kWh - Delivered indicates the recorded data are \
                         from smart meters in delivered direction, kWh - Received \
                         indicates the recorded data are from smart meters in \
                         received direction, and Voltage Phase A indicates \
                         the recorded data are the voltage value measured \
                         by a smart meter.)"),
                 html.Li( "DATE (The date of the recorded data with a format MM/DD/YYYY.), \
                         D01 (The first data point recorded by a smart meter.), D02 (The second \
                         data point recorded by a smart meter.), ..., D96 (The 96th data point \
                       recorded by a smart meter)."),
                 html.Li( "More detailed information and one example of the input \
                         file can be found in the user manual."),
                 html.Li( "Please make sure that the suffix of the file being \
                         uploaded is .csv, .xls, .txt, or .tsv."),
                      ], className="bare_container",),    html.Div(
                children=[
                    dcc.Tabs(
                    id="id='tabs-example-content'",),  
                html.Img(id='image1',height="auto", width="100%",), 
                html.Div(id='eight columns div-for-charts'),
                          html.Br(),                        
                dcc.Interval(id='interval1', n_intervals=0),
                html.H1(id='div-out', children=''),

                html.Div(id='output-data-upload'),                              
                html.Div(id="content"),
                          html.Br(),
                          html.Img(id='image',height="auto", width="100%",),                          
                        ],
                    id="right-column",
                    className="#",
                ),
            ],            
            className="flex-display",
            ),    



      
    
    elif tab == 'tab-2':
        
        return html.Div([
            html.Div([html.P("In this tab, in order to show a time series smart meter data,   \
                             you will need to choose a \"LOCATN_K\", a \"APCODE\", and a \"CHNM\" to specify the customer, the \
                            smart meter of the customer, and the measurement type of the smart meter."),
                 html.Br(),
                    html.Button('Click Me to Generate PDF', id='button2'),
                    html.H3(id='button-clicks2'), 
                    html.H2("Description"),
                 html.Li( "LOCATN_K: The unique ID of a customer."),
                 html.Li( "APCODE: The code for smart meter, options are Z, B, S, where Z \
                         indicates a billing meter, B indicates a battery meter, and S indicates a solar meter. "),
                 html.Li( "CHNM: The types of the measured data, options are kWh - Delivered, \
                         kWh - Received, and Voltage Phase A, where kWh - Delivered indicates the \
                         recorded data are from smart meters in delivered direction, kWh - Received \
                         indicates the recorded data are from smart meters in received direction, \
                         and Voltage Phase A indicates the recorded data are the voltage value measured by a smart meter.)"),
                            ], className="bare_container",),   
                      
            html.Div([html.P('Please select a LOCATN_K:'),], className="subtitle",),
			html.Div([dcc.Dropdown(
				id = 'country-dropdown',
				options = [{'label': i, 'value': i} for i in df.LOCATN_K.unique()],
                value = '442850007',#[], #multi = True
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),
            html.Br(),
            
            html.Div([html.P('Please select a APCODE:'),], className="subtitle",),
			html.Div([dcc.Dropdown(
				id = 'type-dropdown',
				options = [{'label': i, 'value': i} for i in df.APCODE.unique()],
                value = 'B',#[], #multi = True
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),   
            html.Br(),
            html.Div([html.P('Please select a CHNM:'),], className="subtitle",),
			html.Div([dcc.Dropdown(
				id = 'continent-dropdown',
				options = [{'label': i, 'value': i} for i in df.CHNM.unique()],
                value = 'Voltage Phase A',#[], #multi = True
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),   
            html.Br(),
            html.Div(id = 'output-graph-1'),
            ])








    elif tab == 'tab-3':  
        return html.Div([
            html.Div([html.P("In this tab, in order to show the overall distribution of the smart meter data,   \
                             you will need to choose a \"CHNM\" to specify the measurement type of the smart meter."),
                      html.Br(),
                    html.Button('Click Me to Generate PDF1', id='button3'),
                    html.H3(id='button-clicks3'), 
                       html.H2("Description"),
                      html.Li( "CHNM: The types of the measured data, options are kWh - Delivered, \
                         kWh - Received, and Voltage Phase A, where kWh - Delivered indicates the \
                         recorded data are from smart meters in delivered direction, kWh - Received \
                         indicates the recorded data are from smart meters in received direction, \
                         and Voltage Phase A indicates the recorded data are the voltage value measured by a smart meter.)"),
                      ], className="bare_container",),
            html.Div([html.P('Please select a CHNM:'),], className="subtitle",),
			html.Div([dcc.Dropdown(
				id = 'measure-dropdown',
				options = [{'label': i, 'value': i} for i in df.CHNM.unique()],
                value = 'kWh - Received',
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),   
            html.Br(),
            html.Div(id = 'output-graph'),           
        ],
                className="flex-display",
                )
          
                
    elif tab == 'tab-4':  
        Battery_Info_1B = Battery_Info[Battery_Info.EssDerConfiguration == '1B']
        Battery_Info_1C = Battery_Info[Battery_Info.EssDerConfiguration == '1C']
        Battery_Info_2A = Battery_Info[Battery_Info.EssDerConfiguration == '2A']
        Battery_Info_2B = Battery_Info[Battery_Info.EssDerConfiguration == '2B']
        Battery_Info_3A = Battery_Info[Battery_Info.EssDerConfiguration == '3A']
        Battery_Info_3C = Battery_Info[Battery_Info.EssDerConfiguration == '3C']
        Battery_Info_Wrong_1B = Battery_Info_1B[Battery_Info_1B.BatteryConfig != 'AC-Coupled']
        Battery_Info_Wrong_1C = Battery_Info_1C[Battery_Info_1C.BatteryConfig != 'AC-Coupled']
        Battery_Info_Wrong_2A = Battery_Info_2A[Battery_Info_2A.BatteryConfig != 'AC-Coupled']
        Battery_Info_Wrong_2B = Battery_Info_2B[Battery_Info_2B.BatteryConfig != 'AC-Coupled']
        Battery_Info_Wrong_3A = Battery_Info_3A[Battery_Info_3A.BatteryConfig != 'DC-Coupled']
        Battery_Info_Wrong_3C = Battery_Info_3C[Battery_Info_3C.BatteryConfig != 'DC-Coupled']
        inconsistant_info = pd.concat([Battery_Info_Wrong_1B, Battery_Info_Wrong_1C, Battery_Info_Wrong_2A, \
                                       Battery_Info_Wrong_2B, Battery_Info_Wrong_3A, Battery_Info_Wrong_3C, ])
        duplicated_info = df[df.LOCATN_K.isin(df[df.iloc[:,:5].duplicated()].LOCATN_K) & \
                df.CHNM.isin(df[df.iloc[:,:5].duplicated()].CHNM) & \
                df.DATE.isin(df[df.iloc[:,:5].duplicated()].DATE)]
        duplicated_battery = duplicated_info[duplicated_info.APCODE=='B']
        
        duplicated_battery_1 = duplicated_battery[['LOCATN_K','APCODE','METER','CHNM','DATE']].drop_duplicates().sort_values(by = ['LOCATN_K', 'DATE'])
        inconsistant_info_1 = inconsistant_info.loc[:, ['LocationNumber', 'EssDerConfiguration','BatteryConfig']]
        
        th = pdf.font_size
        pdf.set_font('Times','B',12.0)   
        pdf.cell(epw, th, 'IV. Indicators for Bad Data: ')
        pdf.ln(th)
        pdf.set_font('Times','',10.0)  
        th = pdf.font_size
        col_width = epw/5
        pdf.multi_cell(epw, th, 'In this part, firstly, we pulled out inconsistent information on the battery configuration from the database file named "Battery Info.xlsx". Secondly, we pulled out all the duplicated records of the smart meter data in the uploaded file. Thirdly, we pulled out all the smart meter readings that violate the threshold you defined at least once and we print out all the information about the readings except the data themselves. Lastly, we pulled out all the smart meter readings whose daily readings never exceed the threshold you set and we also print out all the information about the readings except the data themselves.')
        pdf.ln(th)
        pdf.cell(epw, th,'1. Incorrect Battery Configuration from Database')
        pdf.ln(th)
        pdf.multi_cell(epw, th, 'Here, we pulled out some inconsistent information on the battery configuration from the database. As we know, for battery configuration, "1B" is AC coupled system (DER only, with backup load panel), "1C" is AC coupled system (DER only, with no backup load panel), "2A" is AC coupled system (DER storage & DER generation, with no backup load panel), "2B" is AC coupled system (DER storage & DER generation, with backup load panel), "3A" is DC coupled system (DER storage & DER generation, with backup load panel), "3C" is DC coupled system (DER storage & DER generation, with no backup load panel). We compare the "BatteryConfig" in file "Battery Info.xlsx" with the definition in the last sentence and pulled out all the records that do not match.')
        pdf.ln(th)
        pdf.multi_cell(epw, th, 'Note that if you would like to check another file for inconsistent records, you can replace the "Battery Info.xlsx" with the new file in the local space but please remember to keep the same format.')
        pdf.ln(th) 
                      
        for col in inconsistant_info_1:
            pdf.cell(col_width, th, str(col), border=1)
        pdf.ln(th)
        for i in range(inconsistant_info_1.shape[0]):
            for j in range(inconsistant_info_1.shape[1]):
                pdf.cell(col_width, th, str(inconsistant_info_1.iloc[i,j]), border=1)    
            pdf.ln(th)
        pdf.ln(th)
        if str(inconsistant_info_1.iloc[0,2]) == 'DC-Coupled':
            pdf.multi_cell(epw, th, 'For example, customer with location number: ' + str(inconsistant_info_1.iloc[0,0]) + ' and with battery configuration: ' + str(inconsistant_info_1.iloc[0,1]) + ' is documented to be: ' + str(inconsistant_info_1.iloc[0,2]) + '. However, it should be: AC-Coupled by definition.')
        else:
            pdf.multi_cell(epw, th, 'For example, customer with location number: ' + str(inconsistant_info_1.iloc[0,0]) + ' and with battery configuration: ' + str(inconsistant_info_1.iloc[0,1]) + ' is documented to be: ' + str(inconsistant_info_1.iloc[0,2]) + '. However, it should be: DC-Coupled by definition.')
            
        pdf.ln(th)
            
        pdf.cell(col_width, th,'2. Duplicated Battery Meter Records')
        pdf.ln(th)
        pdf.multi_cell(epw, th, 'Here, we pulled out all the duplicated smart meter readings of the battery meter from the uploaded file. We print out all the information about the readings except the data themselves.')
        pdf.ln(th)
        for col in duplicated_battery_1:
            pdf.cell(col_width, th, str(col), border=1)
        pdf.ln(th)
        for i in range(duplicated_battery_1.shape[0]):
            for j in range(duplicated_battery_1.shape[1]):
                pdf.cell(col_width, th, str(duplicated_battery_1.iloc[i,j]), border=1)    
            pdf.ln(th)

        pdf.ln(th)
        pdf.ln(th)

        return html.Div([
            html.Div([html.P("In this tab, the table named \"Incorrect Battery Configuration from Database\" \
                             will directly pull out some inconsistent information on the battery configuration \
                            with the \"EssDerConfiguration\". The table named \"Duplicated Battery Meter Records\"\
                            will pull out all the duplicated records from the smart meter data. The two text boxes \
                            below allow you to enter threshold values to filter the violating voltage values and \
                                battery kWh values."),
                      html.Br(),
                      ], className="bare_container",),
        html.Button('Click Me to Generate PDF', id='button4'),
        html.H3(id='button-clicks4'), 
            html.Div([html.P('Incorrect Battery Configuration from Database'),], className="subtitle",),
            html.Div([dash_table.DataTable(
			id = 'table-output-incorrect', 
            style_table={'overflowX': 'auto'},
            style_cell={'width' : '100%',
                        'height' : '80px',
                        'lineHeight': '80px',
                        'textAlign' : 'left',
                        'font_size': '26px',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',},
			style_header={'backgroundColor': 'rgb(230, 230, 230)',
                             'fontWeight': 'bold'},
            style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        },
        {
            'if': {
                'column_id': 'BatteryConfig',
                'filter': 'Region eq "Montreal"'
            },
            'backgroundColor': '#3D9970',
            'color': 'white',
        },
    ],
			columns = [{'name': i, 'id': i, 'selectable': True} for i in inconsistant_info.columns],
			data = inconsistant_info.to_dict('records'),
			sort_action = 'native', sort_mode = 'multi', page_action = 'native',
			page_current =  0, page_size = 15, export_format = 'xlsx', export_headers = 'display',
		),], className="normal_container",), 
            html.Br(),
            
            html.H2("Description"),
            html.Li("For battery configuration, 1B is AC coupled system (DER only, with backup load panel), \
                    1C is AC coupled system (DER only, with no backup load panel), \
                    2A is AC coupled system (DER storage & DER generation, with no backup load panel), \
                    2B is AC coupled system (DER storage & DER generation, with backup load panel), \
                    3A is DC coupled system (DER storage & DER generation, with backup load panel), \
                    3C is DC coupled system (DER storage & DER generation, with no backup load panel), \
                    we pull out all the data that have wrong \"BatteryConfig\"."), 
            html.Br(),          
            html.Hr(),
            html.Div([html.P('Duplicated Battery Meter Records'),], className="subtitle",),
            html.Div([dash_table.DataTable(
			id = 'table-output-duplicated', 
            style_table={'overflowX': 'auto'},
            style_cell={'width' : '80px',
                        'height' : '80px',
                        'lineHeight': '80px',
                        'textAlign' : 'left',
                        'font_size': '26px',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',},
			style_header={'backgroundColor': 'rgb(230, 230, 230)',
                             'fontWeight': 'bold'},
            style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
			columns = [{'name': i, 'id': i, 'selectable': True} for i in duplicated_battery.columns],
			data = duplicated_battery.to_dict('records'), 
			sort_action = 'native', sort_mode = 'multi', page_action = 'native',
			page_current =  0, page_size = 15, export_format = 'xlsx', export_headers = 'display',
		),], className="normal_container",), 
            html.Br(),
            
            html.H2("Description"),
            html.Li("Please sort the \"DATE\" to locate the duplicated information."), 
            html.Hr(),
            html.Br(),
            html.Div([html.P('Voltage Violation'),], className="subtitle",),
            html.Div([html.Li('Please enter the allowable variance of the voltage:'),], className="row",),
            dcc.Input(
            id = 'threshold',
            placeholder='Enter the threshold value...',
            type='number',
            value=80,
            min=0,
            step=1,
        ),  
            html.Br(),
            
            pdf.ln(th),
            pdf.cell(epw, th, '3. Voltage Violation'),            
            pdf.ln(th),
            pdf.cell(epw, th, 'Here, we pulled out all the daily smart meter readings that violate the threshold you defined at least once.'),
            pdf.ln(th),
  
            html.Div(id = 'output-graph-2'),
            
            
            html.Hr(),
            html.Div([html.P('Battery Kwh Violation'),], className="subtitle",),
            html.Div([html.Li('Please enter a small value of kwh that considered as abnormal:'),], className="row",),
            dcc.Input(
            id = 'maximium_value',
            placeholder='Enter a small value...',
            type='number',
            value=0.06,
            min=0,
            step=0.01,
        ),  
            html.Br(),
            
            pdf.ln(th),
            pdf.cell(epw, th, '4. Battery Kwh Violation'),            
            pdf.ln(th),
            pdf.cell(epw, th, 'Here, we pulled out all the daily smart meter readings whose readings never exceed the threshold you set.'),
            pdf.ln(th),
            
            html.Br(),
            html.Div([html.Li('Please select a Measurement Type'),], className="row",),
			html.Div([dcc.Dropdown(
				id = 'type-dropdown',
				options = [{'label': i, 'value': i} for i in ['kWh - Delivered', 'kWh - Received']],
                value = 'kWh - Delivered',\
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),   
            html.Br(),
            html.Div(id = 'output-graph-3'),
            ])

    
    elif tab == 'tab-5':
        return html.Div([
            html.Div([html.P("In this tab, in order to cluster the behavior patterns of a customer \
                             and identify the customers that have abnormal behavior patterns, you \
                            will need to choose a configuration of the battery system, a rate plan \
                            of the users, and a season to conduct analysis. The algorithm will \
                                automatically select the first three most abnormal customers out \
                                    of one behavior pattern to visualize."),
                      html.Br(),
                      ], className="bare_container",),
             html.Button('Click Me to Generate PDF', id='button5'),
            html.H3(id='button-clicks5'), 
            html.Div([html.P('Please select a configuration:'),], className="subtitle",),
            html.Div([dcc.Dropdown(
				id = 'configuration-dropdown',
				options = [{'label': i, 'value': i} for i in ['1B', '1C', '2A', '2B', '3A', '3C']],
                value = '2B',#[], #multi = True
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),  
            html.Br(),
            html.Div([html.P('Please select a rate plan:'),], className="subtitle",),
            html.Div([dcc.Dropdown(
				id = 'rate-dropdown',
				options = [{'label': i, 'value': i} for i in ['13', '14', '15', '21', '23', '25', '26', '27', '29']],
                value = '26',#[], #multi = True
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),  
            html.Br(),
            html.Div([html.P('Please select a season:'),], className="subtitle",),
            html.Div([dcc.Dropdown(
				id = 'season-dropdown',
				options = [{'label': i, 'value': i} for i in ['Summer', 'Winter']],
                value = 'Summer',#[], #multi = True
                style={
                        'height': '5px', 
                        'width': '100%', 
                        'font-size': '2.5rem',
                        'min-height': '2px',
                        },
			),], className="normal_container",),  
            html.Br(),
            html.Div(id = 'output-graph-4'),        
            ])
    elif tab == 'tab-6':
        return html.Div([html.Div([
     
            html.H6('AC failing prediction and EV level prediction in-demand.\
                                          Our next project helps users gain an in-depth \
                                          understanding of machine learning based prediction for real-world implementation.'),], className="row",),])

    

@app.callback(
    Output('button-clicks2', 'children'),
    [Input('button2', 'n_clicks')])
def clicks(n_clicks):
    if n_clicks == 1:
         th = pdf2.font_size
         epw = pdf2.w - 2*pdf2.l_margin
         col_width = epw/5
 
         df1 = df[['LOCATN_K','APCODE','METER','CHNM']]
         pdf.ln(th)
         pdf.ln(th)
    
         for col in df1:
            pdf.cell(col_width, th, str(col), border=1)
         pdf.ln(th)
    

         pdf2.ln(th)
         for i in range(4):
             for j in range(4):
                 pdf2.cell(col_width, th, str(dataset.iloc[i,j]), border=1)
             pdf2.ln(th)
         pdf2.ln(th)
        
         pdf2.output('test_2.pdf','F')
         return 'Report sucessfully generated!'






@app.callback(
    Output('button-clicks3', 'children'),
    [Input('button3', 'n_clicks')])

def clicks(n_clicks):
    if n_clicks == 1:
        th = pdf3.font_size
        pdf3.ln(th)
        pdf3.image(fig_0,  link='', type='', w=5, h=4)
        pdf3.ln(th)
        pdf3.ln(th)
        pdf3.image(fig_1,  link='', type='', w=4, h=3)
        pdf3.ln(th)
        pdf3.output('test_3.pdf','F')
        return 'Report sucessfully generated!'





@app.callback(
    Output('button-clicks4', 'children'),
    [Input('button4', 'n_clicks')])

def clicks(n_clicks):
    if n_clicks == 1:
      
        pdf.output('test_4.pdf','F') 
        return 'Report sucessfully generated!'


@app.callback(
    Output('button-clicks5', 'children'),
    [Input('button5', 'n_clicks')])
def clicks(n_clicks):
    if n_clicks == 1:
        th = pdf5.font_size
        epw = pdf5.w - 2*pdf5.l_margin
        col_width = epw/5
        pdf5.cell(col_width, th, 'The First Behavior Pattern')
        pdf5.ln(th)
        pdf5.image(fig_6,  link='', type='', w=6, h=4)
        pdf5.ln(th)
        pdf5.ln(th)
        
        pdf5.cell(col_width, th, 'The Second Behavior Pattern')
        pdf5.ln(th)
        pdf5.image(fig_7,  link='', type='', w=6, h=4)
        pdf5.ln(th)
        pdf5.ln(th)

        pdf5.cell(col_width, th, 'The Third Behavior Pattern')
        pdf5.ln(th)
        pdf5.image(fig_8,  link='', type='', w=6, h=4)
        pdf5.ln(th)
        pdf5.ln(th)



        pdf5.output('test_5.pdf','F')
        return 'Report sucessfully generated!'














@app.callback(Output('output-graph', 'children'), [Input('measure-dropdown', 'value')])
def update_data_dis(mea_type):
    return html.Div([
            html.Div([
                dcc.Graph(figure = generate_plot1(mea_type)),],className="six columns"),  
             html.Div([
                dcc.Graph(figure = generate_plot2(mea_type)),
                ],className="six columns"),
            html.Div([ html.Br(),
             html.Br(),
             html.Br(),
        html.H2("Description"),
        html.Li( "The area that has high frequency tells the normal range of the measurement, \
                we should also pay attention to the areas that have low frequencies, which \
                shows that there might be some issues with these data."),],className="bare_container"),
        html.Br(),
                ], )


@app.callback(Output('output-graph-4', 'children'), [Input('configuration-dropdown', 'value'), 
                                                     Input('rate-dropdown', 'value'), 
                                                     Input('season-dropdown', 'value')])

def update_data_4(config, rate_sel, season):
    df.DATE = pd.to_datetime(df.DATE)
    meter_data = df.copy()
    meter_data_B = meter_data[meter_data['APCODE'] == 'B']
    meter_data_B = meter_data_B.drop(columns=['METER', 'APCODE'])
    meter_data_B_kWh_Delivered = meter_data_B[meter_data_B['CHNM'] == 'kWh - Delivered'].drop(columns=['CHNM'])
    meter_data_B_kWh_Received = meter_data_B[meter_data_B['CHNM'] == 'kWh - Received'].drop(columns=['CHNM'])
    meter_data_S = meter_data[meter_data['APCODE'] == 'S']
    meter_data_S = meter_data_S.drop(columns=['METER', 'APCODE'])
    meter_data_S_kWh_Delivered = meter_data_S[meter_data_S['CHNM'] == 'kWh - Delivered'].drop(columns=['CHNM'])
    meter_data_S_kWh_Received = meter_data_S[meter_data_S['CHNM'] == 'kWh - Received'].drop(columns=['CHNM'])
    meter_data_Z = meter_data[meter_data['APCODE'] == 'Z']
    meter_data_Z = meter_data_Z.drop(columns=['METER', 'APCODE'])
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/7
    th = 0.2
    pdf.set_font('Times','B',14.0) 
    pdf.cell(epw, 0.0, 'Test Report', align='C')  
    pdf.set_font('Times','',10.0)   
    pdf.ln(0.5)



    if config == '2B':
        
        meter_data_B_kWh_Delivered_2B = meter_data_B_kWh_Delivered[meter_data_B_kWh_Delivered.LOCATN_K.isin(location_2B_info_1.LocationNumber)]
        meter_data_B_kWh_Received_2B = meter_data_B_kWh_Received[meter_data_B_kWh_Received.LOCATN_K.isin(location_2B_info_1.LocationNumber)]
        meter_data_B_kWh_2B = pd.merge(meter_data_B_kWh_Received_2B, meter_data_B_kWh_Delivered_2B, how='inner',
                                on=['LOCATN_K', 'DATE'], suffixes=('_Received', '_Delivered'))
        meter_data_B_kWh_2B.DATE = pd.to_datetime(meter_data_B_kWh_2B.DATE)
        if season == 'Summer':

            rate_date = kWh_date_info_2B[kWh_date_info_2B.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_2B_summer = meter_data_B_kWh_2B[(meter_data_B_kWh_2B.DATE.dt.month >= 5) & (meter_data_B_kWh_2B.DATE.dt.month <= 10)]
            meter_data_B_kWh_2B_summer_rate = meter_data_B_kWh_2B_summer[meter_data_B_kWh_2B_summer.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_2B_summer_rate = meter_data_B_kWh_2B_summer_rate.dropna()
            
            meter_data_B_kWh_2B_summer_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_B_kWh_2B_summer_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_2B_summer_rate[meter_data_B_kWh_2B_summer_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_2B_summer_rate_date = meter_data_B_kWh_2B_summer_rate_date.append(df_range)
            except:
                
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                
            if meter_data_B_kWh_2B_summer_rate_date.empty == True:
                pdf.cell(col_width, th, '1. ' + 'configuration'+ ': '  + config)
                pdf.ln(th)
                pdf.cell(col_width, th, '2. ' + 'rate plan'+ ': '  + rate_sel)
                pdf.ln(th)
                pdf.cell(col_width, th, '3. ' + 'season'+ ': '  + season)
                pdf.ln(th)
                
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_2B_summer_rate_date["Index"] = meter_data_B_kWh_2B_summer_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_2B_summer_rate_date.DATE.map(str)
                meter_data_B_kWh_2B_summer_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_2B_summer_rate_date = meter_data_B_kWh_2B_summer_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_2B_summer_rate_date = meter_data_B_kWh_2B_summer_rate_date.loc[~(abs(meter_data_B_kWh_2B_summer_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_2B_summer_rate_minmax = (meter_data_B_kWh_2B_summer_rate_date.T - meter_data_B_kWh_2B_summer_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_2B_summer_rate_date.T.max(axis=0) - meter_data_B_kWh_2B_summer_rate_date.T.min(axis=0))
                meter_data_B_kWh_2B_summer_rate_minmax = meter_data_B_kWh_2B_summer_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_2B_summer_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_2B_summer_rate_minmax)
                data1_plot7 = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_2B_summer_rate_minmax[meter_data_B_kWh_2B_summer_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                ####### for each user, calculate his/her quantile to center
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                               
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                pdf.cell(col_width, th, '1. ' + 'configuration'+ ': '  + str(config))
                pdf.ln(th)
                pdf.cell(col_width, th, '2. ' + 'rate plan'+ ': '  + str(rate_sel))
                pdf.ln(th)
                pdf.cell(col_width, th, '3. ' + 'season'+ ': '  + str(season))
                pdf.ln(th)
                # # plot top three
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
                
                return html.Div(children = [
                dcc.Graph(
                figure = generate_plot7(data1_plot7, data2_plot7,
                                        data3_plot7, data4_plot7)),    			
                html.Br(),
                dcc.Graph(
                figure = generate_plot8(data1_plot8, data2_plot8,
                                        data3_plot8, data4_plot8)),     			
                html.Br(),
                dcc.Graph(
                figure = generate_plot9(data1_plot9, data2_plot9,
                                        data3_plot9, data4_plot9)),
                html.Br(),       
                html.P("Abnormal customers in the first behavior pattern", className="row"),
        #         dcc.Graph(
        #         figure = generate_plot10(data3_plot7, data4_plot7, 
        #                                  data_5_plot7, data_8_plot7)),
     			# html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot11(data3_plot7, data4_plot7, 
        #                                  data_6_plot7, data_9_plot7)),
     			# html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot12(data3_plot7, data4_plot7, 
        #                                  data_7_plot7, data_10_plot7)),
     			# html.Br(), 
                 ])
        else: 
            rate_date = kWh_date_info_2B[kWh_date_info_2B.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_2B_winter = meter_data_B_kWh_2B[(meter_data_B_kWh_2B.DATE.dt.month >= 11) | (meter_data_B_kWh_2B.DATE.dt.month <= 4)]
            meter_data_B_kWh_2B_winter_rate = meter_data_B_kWh_2B_winter[meter_data_B_kWh_2B_winter.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_2B_winter_rate = meter_data_B_kWh_2B_winter_rate.dropna()            
            
            meter_data_B_kWh_2B_winter_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_B_kWh_2B_winter_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_2B_winter_rate[meter_data_B_kWh_2B_winter_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_2B_winter_rate_date = meter_data_B_kWh_2B_winter_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_2B_winter_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_2B_winter_rate_date["Index"] = meter_data_B_kWh_2B_winter_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_2B_winter_rate_date.DATE.map(str)
                meter_data_B_kWh_2B_winter_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_2B_winter_rate_date = meter_data_B_kWh_2B_winter_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_2B_winter_rate_date = meter_data_B_kWh_2B_winter_rate_date.loc[~(abs(meter_data_B_kWh_2B_winter_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_2B_winter_rate_minmax = (meter_data_B_kWh_2B_winter_rate_date.T - meter_data_B_kWh_2B_winter_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_2B_winter_rate_date.T.max(axis=0) - meter_data_B_kWh_2B_winter_rate_date.T.min(axis=0))
                meter_data_B_kWh_2B_winter_rate_minmax = meter_data_B_kWh_2B_winter_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_2B_winter_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_2B_winter_rate_minmax)
                data1_plot7 = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_2B_winter_rate_minmax[meter_data_B_kWh_2B_winter_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),                     
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),                 
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
                    # html.Br(), 
                ])                        
            # return html.Div(children = [html.Br(),
            #                                 html.P("2B Winter Imcomplete", className="row"),])   
                


    
    elif config == '2A':        
        meter_data_B_kWh_Delivered_2A = meter_data_B_kWh_Delivered[meter_data_B_kWh_Delivered.LOCATN_K.isin(location_2A_info_1.LocationNumber)]
        meter_data_B_kWh_Received_2A = meter_data_B_kWh_Received[meter_data_B_kWh_Received.LOCATN_K.isin(location_2A_info_1.LocationNumber)]
        meter_data_B_kWh_2A = pd.merge(meter_data_B_kWh_Received_2A, meter_data_B_kWh_Delivered_2A, how='inner',
                                on=['LOCATN_K', 'DATE'], suffixes=('_Received', '_Delivered'))
        meter_data_B_kWh_2A.DATE = pd.to_datetime(meter_data_B_kWh_2A.DATE)
        if season == 'Summer':
            rate_date = kWh_date_info_2A[kWh_date_info_2A.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_2A_summer = meter_data_B_kWh_2A[(meter_data_B_kWh_2A.DATE.dt.month >= 5) & (meter_data_B_kWh_2A.DATE.dt.month <= 10)]
            meter_data_B_kWh_2A_summer_rate = meter_data_B_kWh_2A_summer[meter_data_B_kWh_2A_summer.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_2A_summer_rate = meter_data_B_kWh_2A_summer_rate.dropna()
            

            meter_data_B_kWh_2A_summer_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_B_kWh_2A_summer_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_2A_summer_rate[meter_data_B_kWh_2A_summer_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_2A_summer_rate_date = meter_data_B_kWh_2A_summer_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_2A_summer_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_2A_summer_rate_date["Index"] = meter_data_B_kWh_2A_summer_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_2A_summer_rate_date.DATE.map(str)
                meter_data_B_kWh_2A_summer_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_2A_summer_rate_date = meter_data_B_kWh_2A_summer_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_2A_summer_rate_date = meter_data_B_kWh_2A_summer_rate_date.loc[~(abs(meter_data_B_kWh_2A_summer_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_2A_summer_rate_minmax = (meter_data_B_kWh_2A_summer_rate_date.T - meter_data_B_kWh_2A_summer_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_2A_summer_rate_date.T.max(axis=0) - meter_data_B_kWh_2A_summer_rate_date.T.min(axis=0))
                meter_data_B_kWh_2A_summer_rate_minmax = meter_data_B_kWh_2A_summer_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_2A_summer_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_2A_summer_rate_minmax)
                data1_plot7 = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_2A_summer_rate_minmax[meter_data_B_kWh_2A_summer_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),         			
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),        			
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
         			# html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
         			# html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
         			# html.Br(), 
                ])
        else: 
            rate_date = kWh_date_info_2A[kWh_date_info_2A.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_2A_winter = meter_data_B_kWh_2A[(meter_data_B_kWh_2A.DATE.dt.month >= 11) | (meter_data_B_kWh_2A.DATE.dt.month <= 4)]
            meter_data_B_kWh_2A_winter_rate = meter_data_B_kWh_2A_winter[meter_data_B_kWh_2A_winter.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_2A_winter_rate = meter_data_B_kWh_2A_winter_rate.dropna()            
            
            meter_data_B_kWh_2A_winter_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_B_kWh_2A_winter_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_2A_winter_rate[meter_data_B_kWh_2A_winter_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_2A_winter_rate_date = meter_data_B_kWh_2A_winter_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_2A_winter_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_2A_winter_rate_date["Index"] = meter_data_B_kWh_2A_winter_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_2A_winter_rate_date.DATE.map(str)
                meter_data_B_kWh_2A_winter_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_2A_winter_rate_date = meter_data_B_kWh_2A_winter_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_2A_winter_rate_date = meter_data_B_kWh_2A_winter_rate_date.loc[~(abs(meter_data_B_kWh_2A_winter_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_2A_winter_rate_minmax = (meter_data_B_kWh_2A_winter_rate_date.T - meter_data_B_kWh_2A_winter_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_2A_winter_rate_date.T.max(axis=0) - meter_data_B_kWh_2A_winter_rate_date.T.min(axis=0))
                meter_data_B_kWh_2A_winter_rate_minmax = meter_data_B_kWh_2A_winter_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_2A_winter_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_2A_winter_rate_minmax)
                data1_plot7 = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_2A_winter_rate_minmax[meter_data_B_kWh_2A_winter_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),                     
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),                 
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
                    # html.Br(), 
                ])            
            
            # return html.Div(children = [html.Br(),
            #                                 html.P("2A Winter Imcomplete", className="row"),])  
       
                       
    elif config == '1B':        
        meter_data_B_kWh_Delivered_1B = meter_data_B_kWh_Delivered[meter_data_B_kWh_Delivered.LOCATN_K.isin(location_1B_info_1.LocationNumber)]
        meter_data_B_kWh_Received_1B = meter_data_B_kWh_Received[meter_data_B_kWh_Received.LOCATN_K.isin(location_1B_info_1.LocationNumber)]
        meter_data_B_kWh_1B = pd.merge(meter_data_B_kWh_Received_1B, meter_data_B_kWh_Delivered_1B, how='inner',
                                on=['LOCATN_K', 'DATE'], suffixes=('_Received', '_Delivered'))
        meter_data_B_kWh_1B.DATE = pd.to_datetime(meter_data_B_kWh_1B.DATE)
        if season == 'Summer':
            rate_date = kWh_date_info_1B[kWh_date_info_1B.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_1B_summer = meter_data_B_kWh_1B[(meter_data_B_kWh_1B.DATE.dt.month >= 5) & (meter_data_B_kWh_1B.DATE.dt.month <= 10)]
            meter_data_B_kWh_1B_summer_rate = meter_data_B_kWh_1B_summer[meter_data_B_kWh_1B_summer.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_1B_summer_rate = meter_data_B_kWh_1B_summer_rate.dropna()
            
            meter_data_B_kWh_1B_summer_rate_date = pd.DataFrame()
            try: 
                for loc in np.unique(meter_data_B_kWh_1B_summer_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_1B_summer_rate[meter_data_B_kWh_1B_summer_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_1B_summer_rate_date = meter_data_B_kWh_1B_summer_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_1B_summer_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_1B_summer_rate_date["Index"] = meter_data_B_kWh_1B_summer_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_1B_summer_rate_date.DATE.map(str)
                meter_data_B_kWh_1B_summer_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_1B_summer_rate_date = meter_data_B_kWh_1B_summer_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_1B_summer_rate_date = meter_data_B_kWh_1B_summer_rate_date.loc[~(abs(meter_data_B_kWh_1B_summer_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_1B_summer_rate_minmax = (meter_data_B_kWh_1B_summer_rate_date.T - meter_data_B_kWh_1B_summer_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_1B_summer_rate_date.T.max(axis=0) - meter_data_B_kWh_1B_summer_rate_date.T.min(axis=0))
                meter_data_B_kWh_1B_summer_rate_minmax = meter_data_B_kWh_1B_summer_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_1B_summer_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_1B_summer_rate_minmax)
                data1_plot7 = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_1B_summer_rate_minmax[meter_data_B_kWh_1B_summer_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),                                 
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),                         
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
                                # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
                                # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
                                # html.Br(), 
                ])
        else: 
            rate_date = kWh_date_info_1B[kWh_date_info_1B.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_1B_winter = meter_data_B_kWh_1B[(meter_data_B_kWh_1B.DATE.dt.month >= 11) | (meter_data_B_kWh_1B.DATE.dt.month <= 4)]
            meter_data_B_kWh_1B_winter_rate = meter_data_B_kWh_1B_winter[meter_data_B_kWh_1B_winter.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_1B_winter_rate = meter_data_B_kWh_1B_winter_rate.dropna()            
            
            meter_data_B_kWh_1B_winter_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_B_kWh_1B_winter_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_1B_winter_rate[meter_data_B_kWh_1B_winter_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_1B_winter_rate_date = meter_data_B_kWh_1B_winter_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_1B_winter_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_1B_winter_rate_date["Index"] = meter_data_B_kWh_1B_winter_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_1B_winter_rate_date.DATE.map(str)
                meter_data_B_kWh_1B_winter_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_1B_winter_rate_date = meter_data_B_kWh_1B_winter_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_1B_winter_rate_date = meter_data_B_kWh_1B_winter_rate_date.loc[~(abs(meter_data_B_kWh_1B_winter_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_1B_winter_rate_minmax = (meter_data_B_kWh_1B_winter_rate_date.T - meter_data_B_kWh_1B_winter_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_1B_winter_rate_date.T.max(axis=0) - meter_data_B_kWh_1B_winter_rate_date.T.min(axis=0))
                meter_data_B_kWh_1B_winter_rate_minmax = meter_data_B_kWh_1B_winter_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_1B_winter_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_1B_winter_rate_minmax)
                data1_plot7 = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_1B_winter_rate_minmax[meter_data_B_kWh_1B_winter_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),                     
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),                 
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
                    # html.Br(), 
                ])                        
            # return html.Div(children = [html.Br(),
            #                                 html.P("1B Winter Imcomplete", className="row"),])  



    elif config == '1C':        
        meter_data_B_kWh_Delivered_1C = meter_data_B_kWh_Delivered[meter_data_B_kWh_Delivered.LOCATN_K.isin(location_1C_info_1.LocationNumber)]
        meter_data_B_kWh_Received_1C = meter_data_B_kWh_Received[meter_data_B_kWh_Received.LOCATN_K.isin(location_1C_info_1.LocationNumber)]
        meter_data_B_kWh_1C = pd.merge(meter_data_B_kWh_Received_1C, meter_data_B_kWh_Delivered_1C, how='inner',
                                on=['LOCATN_K', 'DATE'], suffixes=('_Received', '_Delivered'))
        meter_data_B_kWh_1C.DATE = pd.to_datetime(meter_data_B_kWh_1C.DATE)
        if season == 'Summer':
            rate_date = kWh_date_info_1C[kWh_date_info_1C.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_1C_summer = meter_data_B_kWh_1C[(meter_data_B_kWh_1C.DATE.dt.month >= 5) & (meter_data_B_kWh_1C.DATE.dt.month <= 10)]
            meter_data_B_kWh_1C_summer_rate = meter_data_B_kWh_1C_summer[meter_data_B_kWh_1C_summer.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_1C_summer_rate = meter_data_B_kWh_1C_summer_rate.dropna()
            
            meter_data_B_kWh_1C_summer_rate_date = pd.DataFrame()
            try: 
                for loc in np.unique(meter_data_B_kWh_1C_summer_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_1C_summer_rate[meter_data_B_kWh_1C_summer_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_1C_summer_rate_date = meter_data_B_kWh_1C_summer_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_1C_summer_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_1C_summer_rate_date["Index"] = meter_data_B_kWh_1C_summer_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_1C_summer_rate_date.DATE.map(str)
                meter_data_B_kWh_1C_summer_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_1C_summer_rate_date = meter_data_B_kWh_1C_summer_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_1C_summer_rate_date = meter_data_B_kWh_1C_summer_rate_date.loc[~(abs(meter_data_B_kWh_1C_summer_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_1C_summer_rate_minmax = (meter_data_B_kWh_1C_summer_rate_date.T - meter_data_B_kWh_1C_summer_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_1C_summer_rate_date.T.max(axis=0) - meter_data_B_kWh_1C_summer_rate_date.T.min(axis=0))
                meter_data_B_kWh_1C_summer_rate_minmax = meter_data_B_kWh_1C_summer_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_1C_summer_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_1C_summer_rate_minmax)
                data1_plot7 = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_1C_summer_rate_minmax[meter_data_B_kWh_1C_summer_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),                                 
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),                         
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
                                # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
                                # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
                                # html.Br(), 
                ])
        else:
            rate_date = kWh_date_info_1C[kWh_date_info_1C.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_B_kWh_1C_winter = meter_data_B_kWh_1C[(meter_data_B_kWh_1C.DATE.dt.month >= 11) | (meter_data_B_kWh_1C.DATE.dt.month <= 4)]
            meter_data_B_kWh_1C_winter_rate = meter_data_B_kWh_1C_winter[meter_data_B_kWh_1C_winter.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_B_kWh_1C_winter_rate = meter_data_B_kWh_1C_winter_rate.dropna()            
            
            meter_data_B_kWh_1C_winter_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_B_kWh_1C_winter_rate.LOCATN_K):
                    df_range = meter_data_B_kWh_1C_winter_rate[meter_data_B_kWh_1C_winter_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_B_kWh_1C_winter_rate_date = meter_data_B_kWh_1C_winter_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
                        
            if meter_data_B_kWh_1C_winter_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_B_kWh_1C_winter_rate_date["Index"] = meter_data_B_kWh_1C_winter_rate_date.LOCATN_K.map(str) + ', ' + meter_data_B_kWh_1C_winter_rate_date.DATE.map(str)
                meter_data_B_kWh_1C_winter_rate_date.set_index("Index", inplace=True)
                meter_data_B_kWh_1C_winter_rate_date = meter_data_B_kWh_1C_winter_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_B_kWh_1C_winter_rate_date = meter_data_B_kWh_1C_winter_rate_date.loc[~(abs(meter_data_B_kWh_1C_winter_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_B_kWh_1C_winter_rate_minmax = (meter_data_B_kWh_1C_winter_rate_date.T - meter_data_B_kWh_1C_winter_rate_date.T.min(axis=0)) \
                / (meter_data_B_kWh_1C_winter_rate_date.T.max(axis=0) - meter_data_B_kWh_1C_winter_rate_date.T.min(axis=0))
                meter_data_B_kWh_1C_winter_rate_minmax = meter_data_B_kWh_1C_winter_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_B_kWh_1C_winter_rate_minmax_pred = kmeans.fit_predict(meter_data_B_kWh_1C_winter_rate_minmax)
                data1_plot7 = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_B_kWh_1C_winter_rate_minmax[meter_data_B_kWh_1C_winter_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                
                
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
        
                return html.Div(children = [
                    dcc.Graph(
                    figure = generate_plot7(data1_plot7, data2_plot7,
                                            data3_plot7, data4_plot7)),
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot8(data1_plot8, data2_plot8,
                                            data3_plot8, data4_plot8)),                     
                    html.Br(),
                    dcc.Graph(
                    figure = generate_plot9(data1_plot9, data2_plot9,
                                            data3_plot9, data4_plot9)),                 
                    html.Br(),       
                    html.P("Abnormal customers in the first behavior pattern", className="row"),
            #         dcc.Graph(
            #         figure = generate_plot10(data3_plot7, data4_plot7, 
            #                                   data_5_plot7, data_8_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot11(data3_plot7, data4_plot7, 
            #                                  data_6_plot7, data_9_plot7)),
                    # html.Br(), 
            #         dcc.Graph(
            #         figure = generate_plot12(data3_plot7, data4_plot7, 
            #                                  data_7_plot7, data_10_plot7)),
                    # html.Br(), 
                ])                        
            # return html.Div(children = [html.Br(),
            #                                 html.P("1C Winter Imcomplete", className="row"),])      
        

        
                

    elif config == '3A':
        meter_data_S_kWh_Delivered_3A = meter_data_S_kWh_Delivered[meter_data_S_kWh_Delivered.LOCATN_K.isin(location_3A_info_1.LocationNumber)]
        meter_data_S_kWh_Received_3A = meter_data_S_kWh_Received[meter_data_S_kWh_Received.LOCATN_K.isin(location_3A_info_1.LocationNumber)]
        meter_data_S_kWh_3A = pd.merge(meter_data_S_kWh_Received_3A, meter_data_S_kWh_Delivered_3A, how='inner',
                            on=['LOCATN_K', 'DATE'], suffixes=('_Received', '_Delivered'))   
        meter_data_S_kWh_3A.DATE = pd.to_datetime(meter_data_S_kWh_3A.DATE)
        if season == 'Summer':
            rate_date = kWh_date_info_3A[kWh_date_info_3A.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_S_kWh_3A_summer = meter_data_S_kWh_3A[(meter_data_S_kWh_3A.DATE.dt.month >= 5) & (meter_data_S_kWh_3A.DATE.dt.month <= 10)]
            meter_data_S_kWh_3A_summer_rate = meter_data_S_kWh_3A_summer[meter_data_S_kWh_3A_summer.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_S_kWh_3A_summer_rate = meter_data_S_kWh_3A_summer_rate.dropna()
        
            meter_data_S_kWh_3A_summer_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_S_kWh_3A_summer_rate.LOCATN_K):
                    df_range = meter_data_S_kWh_3A_summer_rate[meter_data_S_kWh_3A_summer_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_S_kWh_3A_summer_rate_date = meter_data_S_kWh_3A_summer_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
  
            if meter_data_S_kWh_3A_summer_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_S_kWh_3A_summer_rate_date["Index"] = meter_data_S_kWh_3A_summer_rate_date.LOCATN_K.map(str) + ', ' + meter_data_S_kWh_3A_summer_rate_date.DATE.map(str)
                meter_data_S_kWh_3A_summer_rate_date.set_index("Index", inplace=True)
                meter_data_S_kWh_3A_summer_rate_date = meter_data_S_kWh_3A_summer_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_S_kWh_3A_summer_rate_date = meter_data_S_kWh_3A_summer_rate_date.loc[~(abs(meter_data_S_kWh_3A_summer_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_S_kWh_3A_summer_rate_minmax = (meter_data_S_kWh_3A_summer_rate_date.T - meter_data_S_kWh_3A_summer_rate_date.T.min(axis=0)) \
                / (meter_data_S_kWh_3A_summer_rate_date.T.max(axis=0) - meter_data_S_kWh_3A_summer_rate_date.T.min(axis=0))
                meter_data_S_kWh_3A_summer_rate_minmax = meter_data_S_kWh_3A_summer_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_S_kWh_3A_summer_rate_minmax_pred = kmeans.fit_predict(meter_data_S_kWh_3A_summer_rate_minmax)
                data1_plot7 = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_S_kWh_3A_summer_rate_minmax[meter_data_S_kWh_3A_summer_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                ####### for each user, calculate his/her quantile to center
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                               
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # # plot top three
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
                
                return html.Div(children = [
                dcc.Graph(
                figure = generate_plot7(data1_plot7, data2_plot7,
                                        data3_plot7, data4_plot7)),                     
                html.Br(),
                dcc.Graph(
                figure = generate_plot8(data1_plot8, data2_plot8,
                                        data3_plot8, data4_plot8)),                             
                html.Br(),
                dcc.Graph(
                figure = generate_plot9(data1_plot9, data2_plot9,
                                        data3_plot9, data4_plot9)),
                html.Br(),       
                html.P("Abnormal customers in the first behavior pattern", className="row"),
        #         dcc.Graph(
        #         figure = generate_plot10(data3_plot7, data4_plot7, 
        #                                  data_5_plot7, data_8_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot11(data3_plot7, data4_plot7, 
        #                                  data_6_plot7, data_9_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot12(data3_plot7, data4_plot7, 
        #                                  data_7_plot7, data_10_plot7)),
                        # html.Br(), 
                 ])      

        else: 
            rate_date = kWh_date_info_3A[kWh_date_info_3A.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_S_kWh_3A_winter = meter_data_S_kWh_3A[(meter_data_S_kWh_3A.DATE.dt.month >= 5) & (meter_data_S_kWh_3A.DATE.dt.month <= 10)]
            meter_data_S_kWh_3A_winter_rate = meter_data_S_kWh_3A_winter[meter_data_S_kWh_3A_winter.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_S_kWh_3A_winter_rate = meter_data_S_kWh_3A_winter_rate.dropna()
        
            meter_data_S_kWh_3A_winter_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_S_kWh_3A_winter_rate.LOCATN_K):
                    df_range = meter_data_S_kWh_3A_winter_rate[meter_data_S_kWh_3A_winter_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_S_kWh_3A_winter_rate_date = meter_data_S_kWh_3A_winter_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
  
            if meter_data_S_kWh_3A_winter_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_S_kWh_3A_winter_rate_date["Index"] = meter_data_S_kWh_3A_winter_rate_date.LOCATN_K.map(str) + ', ' + meter_data_S_kWh_3A_winter_rate_date.DATE.map(str)
                meter_data_S_kWh_3A_winter_rate_date.set_index("Index", inplace=True)
                meter_data_S_kWh_3A_winter_rate_date = meter_data_S_kWh_3A_winter_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_S_kWh_3A_winter_rate_date = meter_data_S_kWh_3A_winter_rate_date.loc[~(abs(meter_data_S_kWh_3A_winter_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_S_kWh_3A_winter_rate_minmax = (meter_data_S_kWh_3A_winter_rate_date.T - meter_data_S_kWh_3A_winter_rate_date.T.min(axis=0)) \
                / (meter_data_S_kWh_3A_winter_rate_date.T.max(axis=0) - meter_data_S_kWh_3A_winter_rate_date.T.min(axis=0))
                meter_data_S_kWh_3A_winter_rate_minmax = meter_data_S_kWh_3A_winter_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_S_kWh_3A_winter_rate_minmax_pred = kmeans.fit_predict(meter_data_S_kWh_3A_winter_rate_minmax)
                data1_plot7 = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_S_kWh_3A_winter_rate_minmax[meter_data_S_kWh_3A_winter_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                ####### for each user, calculate his/her quantile to center
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                               
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # # plot top three
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
                
                return html.Div(children = [
                dcc.Graph(
                figure = generate_plot7(data1_plot7, data2_plot7,
                                        data3_plot7, data4_plot7)),                     
                html.Br(),
                dcc.Graph(
                figure = generate_plot8(data1_plot8, data2_plot8,
                                        data3_plot8, data4_plot8)),                             
                html.Br(),
                dcc.Graph(
                figure = generate_plot9(data1_plot9, data2_plot9,
                                        data3_plot9, data4_plot9)),
                html.Br(),       
                html.P("Abnormal customers in the first behavior pattern", className="row"),
        #         dcc.Graph(
        #         figure = generate_plot10(data3_plot7, data4_plot7, 
        #                                  data_5_plot7, data_8_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot11(data3_plot7, data4_plot7, 
        #                                  data_6_plot7, data_9_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot12(data3_plot7, data4_plot7, 
        #                                  data_7_plot7, data_10_plot7)),
                        # html.Br(), 
                 ])                  
            
            # return html.Div(children = [html.Br(),
            #                                 html.P("3A Winter Imcomplete", className="row"),])   
  
            

    elif config == '3C':
        meter_data_S_kWh_Delivered_3C = meter_data_S_kWh_Delivered[meter_data_S_kWh_Delivered.LOCATN_K.isin(location_3C_info_1.LocationNumber)]
        meter_data_S_kWh_Received_3C = meter_data_S_kWh_Received[meter_data_S_kWh_Received.LOCATN_K.isin(location_3C_info_1.LocationNumber)]
        meter_data_S_kWh_3C = pd.merge(meter_data_S_kWh_Received_3C, meter_data_S_kWh_Delivered_3C, how='inner',
                            on=['LOCATN_K', 'DATE'], suffixes=('_Received', '_Delivered'))   
        meter_data_S_kWh_3C.DATE = pd.to_datetime(meter_data_S_kWh_3C.DATE)
        if season == 'Summer':
            rate_date = kWh_date_info_3C[kWh_date_info_3C.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_S_kWh_3C_summer = meter_data_S_kWh_3C[(meter_data_S_kWh_3C.DATE.dt.month >= 5) & (meter_data_S_kWh_3C.DATE.dt.month <= 10)]
            meter_data_S_kWh_3C_summer_rate = meter_data_S_kWh_3C_summer[meter_data_S_kWh_3C_summer.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_S_kWh_3C_summer_rate = meter_data_S_kWh_3C_summer_rate.dropna()
        
            meter_data_S_kWh_3C_summer_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_S_kWh_3C_summer_rate.LOCATN_K):
                    df_range = meter_data_S_kWh_3C_summer_rate[meter_data_S_kWh_3C_summer_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_S_kWh_3C_summer_rate_date = meter_data_S_kWh_3C_summer_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
  
            if meter_data_S_kWh_3C_summer_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_S_kWh_3C_summer_rate_date["Index"] = meter_data_S_kWh_3C_summer_rate_date.LOCATN_K.map(str) + ', ' + meter_data_S_kWh_3C_summer_rate_date.DATE.map(str)
                meter_data_S_kWh_3C_summer_rate_date.set_index("Index", inplace=True)
                meter_data_S_kWh_3C_summer_rate_date = meter_data_S_kWh_3C_summer_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_S_kWh_3C_summer_rate_date = meter_data_S_kWh_3C_summer_rate_date.loc[~(abs(meter_data_S_kWh_3C_summer_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_S_kWh_3C_summer_rate_minmax = (meter_data_S_kWh_3C_summer_rate_date.T - meter_data_S_kWh_3C_summer_rate_date.T.min(axis=0)) \
                / (meter_data_S_kWh_3C_summer_rate_date.T.max(axis=0) - meter_data_S_kWh_3C_summer_rate_date.T.min(axis=0))
                meter_data_S_kWh_3C_summer_rate_minmax = meter_data_S_kWh_3C_summer_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_S_kWh_3C_summer_rate_minmax_pred = kmeans.fit_predict(meter_data_S_kWh_3C_summer_rate_minmax)
                data1_plot7 = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_S_kWh_3C_summer_rate_minmax[meter_data_S_kWh_3C_summer_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                ####### for each user, calculate his/her quantile to center
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                               
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # # plot top three
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
                
                return html.Div(children = [
                dcc.Graph(
                figure = generate_plot7(data1_plot7, data2_plot7,
                                        data3_plot7, data4_plot7)),                     
                html.Br(),
                dcc.Graph(
                figure = generate_plot8(data1_plot8, data2_plot8,
                                        data3_plot8, data4_plot8)),                             
                html.Br(),
                dcc.Graph(
                figure = generate_plot9(data1_plot9, data2_plot9,
                                        data3_plot9, data4_plot9)),
                html.Br(),       
                html.P("Abnormal customers in the first behavior pattern", className="row"),
        #         dcc.Graph(
        #         figure = generate_plot10(data3_plot7, data4_plot7, 
        #                                  data_5_plot7, data_8_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot11(data3_plot7, data4_plot7, 
        #                                  data_6_plot7, data_9_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot12(data3_plot7, data4_plot7, 
        #                                  data_7_plot7, data_10_plot7)),
                        # html.Br(), 
                 ])      

        else: 
            rate_date = kWh_date_info_3C[kWh_date_info_3C.RATE == int(rate_sel)]
            rate_date.START_DATE = pd.to_datetime(rate_date.START_DATE)
            rate_date.END_DATE = pd.to_datetime(rate_date.END_DATE)
            meter_data_S_kWh_3C_winter = meter_data_S_kWh_3C[(meter_data_S_kWh_3C.DATE.dt.month >= 5) & (meter_data_S_kWh_3C.DATE.dt.month <= 10)]
            meter_data_S_kWh_3C_winter_rate = meter_data_S_kWh_3C_winter[meter_data_S_kWh_3C_winter.LOCATN_K.isin(rate_date.LOCATN_K)]
            meter_data_S_kWh_3C_winter_rate = meter_data_S_kWh_3C_winter_rate.dropna()
        
            meter_data_S_kWh_3C_winter_rate_date = pd.DataFrame()
            try:
                for loc in np.unique(meter_data_S_kWh_3C_winter_rate.LOCATN_K):
                    df_range = meter_data_S_kWh_3C_winter_rate[meter_data_S_kWh_3C_winter_rate.LOCATN_K == loc]
                    date_range = rate_date[rate_date.LOCATN_K == loc]
                    df_range = df_range[(df_range.DATE >= str(date_range.iloc[0, 1]) ) & (df_range.DATE <= str(date_range.iloc[0, 2]) )]
                    meter_data_S_kWh_3C_winter_rate_date = meter_data_S_kWh_3C_winter_rate_date.append(df_range)
            except:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
  
            if meter_data_S_kWh_3C_winter_rate_date.empty == True:
                return html.Div(children = [html.Br(),
                                            html.P("No data", className="row"),])
            else: 
                meter_data_S_kWh_3C_winter_rate_date["Index"] = meter_data_S_kWh_3C_winter_rate_date.LOCATN_K.map(str) + ', ' + meter_data_S_kWh_3C_winter_rate_date.DATE.map(str)
                meter_data_S_kWh_3C_winter_rate_date.set_index("Index", inplace=True)
                meter_data_S_kWh_3C_winter_rate_date = meter_data_S_kWh_3C_winter_rate_date.drop(columns=['LOCATN_K', 'DATE'])
                meter_data_S_kWh_3C_winter_rate_date = meter_data_S_kWh_3C_winter_rate_date.loc[~(abs(meter_data_S_kWh_3C_winter_rate_date)<=0.02).all(axis=1), :]
                
                meter_data_S_kWh_3C_winter_rate_minmax = (meter_data_S_kWh_3C_winter_rate_date.T - meter_data_S_kWh_3C_winter_rate_date.T.min(axis=0)) \
                / (meter_data_S_kWh_3C_winter_rate_date.T.max(axis=0) - meter_data_S_kWh_3C_winter_rate_date.T.min(axis=0))
                meter_data_S_kWh_3C_winter_rate_minmax = meter_data_S_kWh_3C_winter_rate_minmax.T
                
                kmeans = KMeans(n_clusters=3, random_state=0)
                meter_data_S_kWh_3C_winter_rate_minmax_pred = kmeans.fit_predict(meter_data_S_kWh_3C_winter_rate_minmax)
                data1_plot7 = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 0].iloc[:, :96]
                data2_plot7 = -meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 0].iloc[:, 96:]
                data3_plot7 = kmeans.cluster_centers_[0][:96]
                data4_plot7 = -kmeans.cluster_centers_[0][96:]
                data1_plot8 = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 1].iloc[:, :96]
                data2_plot8 = -meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 1].iloc[:, 96:]
                data3_plot8 = kmeans.cluster_centers_[1][:96]
                data4_plot8 = -kmeans.cluster_centers_[1][96:]
                data1_plot9 = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 2].iloc[:, :96]
                data2_plot9 = -meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 2].iloc[:, 96:]
                data3_plot9 = kmeans.cluster_centers_[2][:96]
                data4_plot9 = -kmeans.cluster_centers_[2][96:]
            
                ######## For the top plot ##############
                center1p = kmeans.cluster_centers_[0][:96]
                center1n = kmeans.cluster_centers_[0][96:]
                data1p_ = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 0].iloc[:, :96].copy()
                data1n_ = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 0].iloc[:, 96:].copy()
                data1p = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 0].iloc[:, :96].to_numpy()
                data1n = meter_data_S_kWh_3C_winter_rate_minmax[meter_data_S_kWh_3C_winter_rate_minmax_pred == 0].iloc[:, 96:].to_numpy()
                
                idx_1 = data1p_.index.str.split(pat=' ', n=1, expand=True)
                idx_1_loc = [i[0] for i in idx_1]
                
                data1p_.index = idx_1_loc
                data1n_.index = idx_1_loc
                
                ####### for each user, calculate his/her quantile to center
                dist = []
                for i in np.unique(idx_1_loc):
                    dff1 = data1p_[data1p_.index==i]
                    data1p_10_quantile = np.percentile(dff1, 90, axis=0)
                    dist1 = (data1p_10_quantile - center1p)**2
                    dist2 = np.sum(dist1)
                    dist.append({'loc': i, 'dist': dist2})
                
                dist_df = pd.DataFrame(dist)
                dist_df = dist_df.sort_values('dist', ascending=False)
                               
                dist_n = []
                for i in np.unique(idx_1_loc):
                    dff1_n = data1p_[data1p_.index==i]
                    data1n_10_quantile = np.percentile(dff1_n, 90, axis=0)
                    dist1_n = (data1n_10_quantile - center1n)**2
                    dist2_n = np.sum(dist1_n)
                    dist_n.append({'loc': i, 'dist': dist2_n})
                
                dist_df_n = pd.DataFrame(dist_n)
                dist_df_n = dist_df_n.sort_values('dist', ascending=False)
                
                # # plot top three
                # data_5_plot7 = data1p_[data1p_.index==dist_df.iloc[0,0]]
                # data_6_plot7 = data1p_[data1p_.index==dist_df.iloc[1,0]]
                # data_7_plot7 = data1p_[data1p_.index==dist_df.iloc[2,0]]
                # data_8_plot7 = -data1n_[data1n_.index==dist_df.iloc[0,0]]
                # data_9_plot7 = -data1n_[data1n_.index==dist_df.iloc[1,0]]
                # data_10_plot7 = -data1n_[data1n_.index==dist_df.iloc[2,0]]
                
                return html.Div(children = [
                dcc.Graph(
                figure = generate_plot7(data1_plot7, data2_plot7,
                                        data3_plot7, data4_plot7)),                     
                html.Br(),
                dcc.Graph(
                figure = generate_plot8(data1_plot8, data2_plot8,
                                        data3_plot8, data4_plot8)),                             
                html.Br(),
                dcc.Graph(
                figure = generate_plot9(data1_plot9, data2_plot9,
                                        data3_plot9, data4_plot9)),
                html.Br(),       
                html.P("Abnormal customers in the first behavior pattern", className="row"),
        #         dcc.Graph(
        #         figure = generate_plot10(data3_plot7, data4_plot7, 
        #                                  data_5_plot7, data_8_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot11(data3_plot7, data4_plot7, 
        #                                  data_6_plot7, data_9_plot7)),
                        # html.Br(), 
        #         dcc.Graph(
        #         figure = generate_plot12(data3_plot7, data4_plot7, 
        #                                  data_7_plot7, data_10_plot7)),
                        # html.Br(), 
                 ])                  
            
            # return html.Div(children = [html.Br(),
            #                                 html.P("3C Winter Imcomplete", className="row"),])   
  
              

    else: 
        return html.Div(children = [html.Br(),
                                            html.P("Imcomplete", className="row"),])    
@app.callback(Output('output-graph-3', 'children'), [Input('maximium_value', 'value'), 
                                                     Input('type-dropdown', 'value')])

def update_data_3(value, sm_type):
    global dataset_kwhe
    df.DATE = pd.to_datetime(df.DATE).dt.date
    dataset_kwh = df[(df.CHNM==sm_type)&(df.APCODE=='B')]
    dataset_kwhe = dataset_kwh[dataset_kwh.index.isin(dataset_kwh[(dataset_kwh.iloc[:, 5:]<=value).all(axis=1)].dropna(how='all').index)]
    th = pdf.font_size
    col_width = epw/5
    
    pdf.multi_cell(epw, th, 'The threshold you entered is: ' + str(value) + '(kWh) and the measurement type you select is: ' + str(sm_type) + '.')
    pdf.ln(th)
    pdf.multi_cell(epw, th, 'Below is the table of all the information about the readings except the data themselves.')
    pdf.ln(th)
    print(dataset_kwhe['DATE'])
    
    for i in range(dataset_kwhe.shape[0]):
        for j in range(5):
            pdf.cell(col_width, th, str(dataset_kwhe.iloc[i,j]), border=1)
        pdf.ln(th)
    pdf.ln(th)
    
    return html.Div(children = [
		
	    html.Br(),
        dcc.Graph(
 			id = 'graph-output-3',
            figure = generate_plot6(dataset_kwhe, value),
 	    ),
        html.Br(),
        html.Br(),
	    html.Div([dash_table.DataTable(
			id = 'table-kwh-output', 
            style_table={'overflowX': 'auto'},
            style_cell={'width' : '80px',
                        'height' : '80px',
                        'lineHeight': '80px',
                        'textAlign' : 'left',
                        'font_size': '26px',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',},
			style_header={'backgroundColor': 'rgb(230, 230, 230)',
                             'fontWeight': 'bold'},
            style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
			columns = [{'name': i, 'id': i, 'selectable': True} for i in dataset_kwhe.columns],
			data = dataset_kwhe.to_dict('records'),
			sort_action = 'native', sort_mode = 'multi', page_action = 'native', filter_action='native', 
			page_current =  0, page_size = 15, export_format = 'xlsx', export_headers = 'display',
		),	], className="normal_container",), 
            html.Br(),	
	])

# voltage violation.


@app.callback(Output('output-graph-2', 'children'), [Input('threshold', 'value')])
def update_data_2(value):
    global dataset_ve
    df.DATE = pd.to_datetime(df.DATE).dt.date
    dataset_v = df[(df.CHNM=='Voltage Phase A')]
    dataset_ve = dataset_v[dataset_v.index.isin(dataset_v[(dataset_v.iloc[:, 5:]>=980+value) | (dataset_v.iloc[:, 5:]<=980-value)].dropna(how='all').index)]
    th = pdf.font_size
    col_width = epw/5
    print(dataset_ve['DATE'])
    pdf.multi_cell(epw, th, 'The threshold you entered is: ' + str(value) + '(V). ')
    pdf.ln(th)
    pdf.multi_cell(epw, th, 'Below is the table of all the information about the readings except the data themselves.')
    pdf.ln(th)
    
    for i in range(dataset_ve.shape[0]):
        for j in range(5):
            pdf.cell(col_width, th, str(dataset_ve.iloc[i,j]), border=1)
        pdf.ln(th)
    pdf.ln(th)   

    return html.Div(children = [
		
	    html.Br(),
        dcc.Graph(
 			id = 'graph-output-2',
            figure = generate_plot5(dataset_ve, value),
 	    ),
        html.Br(),
        html.Br(),
	    html.Div([dash_table.DataTable(
			id = 'table-v-output', 
            style_table={'overflowX': 'auto'},
            style_cell={'width' : '80px',
                        'height' : '80px',
                        'lineHeight': '80px',
                        'textAlign' : 'left',
                        'font_size': '26px',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',},
			style_header={'backgroundColor': 'rgb(230, 230, 230)',
                             'fontWeight': 'bold'},
            style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
			columns = [{'name': i, 'id': i, 'selectable': True} for i in dataset_ve.columns],
			data = dataset_ve.to_dict('records'),
			sort_action = 'native', sort_mode = 'multi', page_action = 'native', filter_action='native', 
			page_current =  0, page_size = 15, export_format = 'xlsx', export_headers = 'display',
		),], className="normal_container",), 
            html.Br(),
	])



##### tab-2 (Data Visualizations), report generate ####
@app.callback(Output('output-graph-1', 'children'), [Input('country-dropdown', 'value'),
    Input('continent-dropdown', 'value'), Input('type-dropdown', 'value')])
def update_data_1(value, chnm, apcode):
    global dataset,date
    
    df.DATE = pd.to_datetime(df.DATE)
    dataset = df[(df.LOCATN_K.isin([value])) & (df.CHNM.isin([chnm])) & (df.APCODE.isin([apcode])) ]
    dataset = dataset.sort_values(by='DATE')
    date = pd.date_range(start=dataset.DATE.iloc[0], end=dataset.DATE.iloc[0]+datetime.timedelta(minutes=1425),  periods=96)
    for i in range(1, dataset.shape[0]):
	    date = date.union(pd.date_range(start=dataset.DATE.iloc[i], end=dataset.DATE.iloc[i]+\
                                         datetime.timedelta(minutes=1425),  periods=96))

    
    return html.Div([
		html.Br(),
		dcc.Graph(id = 'graph-output-1',
            figure = generate_plot(),),
                    
                html.Br(),
                html.H2("Description"),
                html.Li( "The blank spaces in the plot show the time range \
                                 the smart meter data are missing."),
                html.Br(),         
                    dash_table.DataTable(
                                id = 'table-output', 
                    style_table={'overflowX': 'auto'},
                    style_cell={'width' : '80px',
                                'height' : '80px',
                                'lineHeight': '80px',
                                'textAlign' : 'left',
                                'font_size': '26px',
                                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',},
                                style_header={'backgroundColor': 'rgb(230, 230, 230)',
                                     'fontWeight': 'bold'},
                    style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['Date', 'Region']
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
                                columns = [{'name': i, 'id': i, 'selectable': True} for i in dataset.columns],
                                data = dataset.to_dict('records'),
                                sort_action = 'native', sort_mode = 'multi', page_action = 'native', 
                    page_current =  0, page_size = 15, export_format = 'xlsx', export_headers = 'display',
                        )
                ])

@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def parse_contents(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # assume that the user uploaded a CSV file
            global df
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df = df.drop_duplicates()
            
        elif 'xls' in filename:
            # assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # assume that the user uploaded a TXT file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
            ])
    unique_num_1 = np.unique(df['APCODE'])
    unique_num_2 = np.unique(df['LOCATN_K'])
    unique_num_3 = np.unique(df['CHNM'])
 
    
            
    return html.Div([
     
        html.Div([
        html.Div([html.P("File Name"),], className="subtitle",),            
        html.Div([html.P(filename, style={"margin-bottom": "0px"}),], className="bare_container",),
        html.Br(),
        html.Div([html.P("Unique Contents in Three Most Important Keys of the File for Filtering"),], className="subtitle",),
        html.Div(children=html.P(['Unique APCODE: ' + str(unique_num_1)]), className="bare_container",),
        html.Div(children=html.P(['Unique LOCATION: ' + str(unique_num_2)]), className="bare_container",),
        html.Div(children=html.P(['Unique CHNM: ' + str(unique_num_3)]), className="bare_container",),
        html.Br(),
        html.Div([html.P("File Contents"),], className="subtitle",),
        html.Div([html.P("The table below provides all the information contained in \
                         the uploaded file. You may filter the table to gain the information \
                         you want, some commands are listed under the table."),],className="bare_container",),
                  ]),

        dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            sort_action='native',
            filter_action='native',
            sort_mode='multi',
            page_action='native',
            page_size= 15,
            style_table={
                          'overflowX': 'auto'},
            style_cell={'width' : '80px',
                        'height' : '80px',
                        'lineHeight': '80px',
                        'textAlign' : 'left',
                        'font_size': '26px',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',},
            style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
            ),
                            html.Br(),
                    html.Br(),        
         html.Div([
        html.Div([html.P('Here are some filtering operators:'),], className="row",),
        html.Div([html.P("Text & String Filtering:"),], className="row",),
        html.Div([html.Li("Voltage"),], className="row",),
        html.Div([html.Li("contains Voltage"), ], className="row",),
        html.Div([html.Li("\"Voltage Phase A\""), ], className="row",),
        html.Div([html.Li("= Voltage Phase A"),], className="row",),
        ],  className="three columns",),
        
        html.Div([html.Br(),html.Br(),html.Br(),
        html.Div([html.P("Numeric Filtering:"),], className="row",),
        html.Div([html.Li("0.828"),], className="row",),
        html.Div([html.Li("= 0.828"), ], className="row",),
        html.Div([html.Li("> 0.828"), ], className="row",),
        html.Div([html.Li("=> 0.828"),], className="row",),        
        html.Div([html.Li("< 0.828"), ], className="row",),
        html.Div([html.Li("<= 0.828"),], className="row",),
        ],  className="three columns",),
        
        html.Div([html.Br(),html.Br(),html.Br(),
        html.Div([html.P("Datetime Filtering:"),], className="row",),
        html.Div([html.Li("2019"),], className="row",),
        html.Div([html.Li("2019-06"), ], className="row",),
        html.Div([html.Li("2019-06-01"), ], className="row",),
        html.Div([html.Li("datestartswith 2019"),], className="row",),        
        html.Div([html.Li("datestartswith 2019-03"), ], className="row",),
        html.Div([html.Li("datestartswith 2019-03-01"),], className="row",),        
        html.Div([html.Li("> 2019-03"), ], className="row",),
        html.Div([html.Li("> 2019-03-01"), ], className="row",),
        html.Div([html.Li(">= 2019-03-01"), ], className="row",),
        html.Div([html.Li("< 2019-03"), ], className="row",),
        html.Div([html.Li("<= 2019-03"), ], className="row",),
                ],  className="three columns",),

],className="bare_container")



@app.callback(Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')])



def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run_server(debug=False)

