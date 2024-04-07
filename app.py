import streamlit as st
import plotly.express as px
import pandas as pd

from func import get_one_coin
from func import COINS

def line_chart(data:pd.DataFrame,name)->None:

    fig = px.line(data, x = 'date', y = 'price_v', title= name, markers='-.')# hover_data=['category','price']
    # fig.add_hrect(y0=incomes,y1=data['spends'].max(),  line_width=0, fillcolor="red", opacity=0.2)
    # fig.add_vline(x = data[data['spends'] > incomes].iloc[0].date, line_width=3, line_dash="dash", line_color="green")

    st.write(fig)

def app():
    
    
    st.title("Select the coin")
    selected_coin = st.selectbox(
        label="выберите монету",
        options=COINS.keys(),
    )
    data = get_one_coin(name = selected_coin)
    
    line_chart(data,selected_coin)

if __name__=='__main__':
    app()