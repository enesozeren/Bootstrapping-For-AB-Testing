import pandas as pd
import numpy as np
import streamlit as st
import functions as func


# Setting up the page
func.page_setup()

# Data generation
st.subheader('IGT data of players')
data = func.generate_data()
st.dataframe(data.head(10))
st.caption('Total IGT (in minutes) of players in the test time period (Only 10 data points are shown to illustrate)')

# Summary of the Data
st.subheader('Summary of the Data')
func.summary_of_data(data)
st.write('We can use bootstrapping method to calculate the statistical significance (P-Value).')

# What is Bootstrapping?    
st.subheader('Before applying the method: what is Bootstrapping?')
st.write('TBD')

# Implementing Bootstrap method
st.subheader('P-Value Caclulation with Bootstrapping method')
p_val = func.p_value_with_bootstrapping(data[data['Group']=='Control'], data[data['Group']=='Variant'], col_name='IGT')

# Conclusion
st.subheader('Conclusion')
st.write('TBD')