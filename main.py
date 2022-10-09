import pandas as pd
import numpy as np
import random
import streamlit as st
import os
import functions as func


# Setting up the page
func.streamlit_setup()

# Data generation
st.subheader('IGT data of players')
data = func.generate_data()
st.dataframe(data.head(10))
st.caption('Total IGT of players in the test time period.')

# Summary of the Data
st.subheader('Summary of the Data')
st.write(f"Total Client Volume: {data['User ID'].nunique()}")

col1, col2 = st.columns(2)
col1.metric("Control Group Client Volume", f"{data[data['Group']=='Control']['User ID'].nunique()}")
col2.metric("Control Group Avg IGT", f"{round(data[data['Group']=='Control']['IGT'].mean(), 3)}")

col3, col4 = st.columns(2)
col3.metric("Variant Group Client Volume", f"{data[data['Group']=='Variant']['User ID'].nunique()}")
col4.metric("Variant Group Avg IGT", f"{round(data[data['Group']=='Variant']['IGT'].mean(), 3)}")