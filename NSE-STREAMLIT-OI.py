from nsepython import *
import streamlit as st
import plotly.graph_objects as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

placeholder = st.empty()
start_button = st.empty()

def running_status():
    start_now=datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
    end_now=datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
    return start_now<datetime.datetime.now()<end_now

print(running_status())

def data_processing():
    oi_data, ltp, crontime = oi_chain_builder("NIFTY","latest","full")

    oi_data['Strike_Price']=oi_data['Strike Price'].astype(float)
    oi_data['CALLS_OI']=oi_data['CALLS_OI'].astype(float)
    oi_data['PUTS_OI']=oi_data['PUTS_OI'].astype(float)

    oi_data = oi_data[oi_data.Strike_Price < (ltp+2000) ]
    oi_data = oi_data[oi_data.Strike_Price > (ltp-2000) ]


    plot = px.Figure(data=[px.Bar(name = 'CE',x = oi_data['Strike Price'],y = oi_data['CALLS_OI']*50), 
           px.Bar(name = 'PE',x = oi_data['Strike Price'],y = oi_data['PUTS_OI']*50)],
           layout = px.Layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(242, 242, 242, 0.8)'))
    
    plot.add_vline(x=(round(ltp/50)*50), line_width=2, line_dash="dash", line_color="black",annotation_text="NIFTY ATM Strike ",annotation_position="top")
    placeholder.write(plot)
    
    print(crontime)
    

if start_button.button('Start',key='start'):
    start_button.empty()
    if st.button('Stop',key='stop'):
        pass
    while True:
        data_processing()
        time.sleep(60)
print ('stopped')



