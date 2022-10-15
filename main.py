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
st.write('If you want to see the logic of bootstrapping check the box below.')
if st.checkbox('See the Logic of Bootstrapping'):
    func.bootstrap_method_exp()

# Implementing Bootstrap method
st.subheader('P-Value Caclulation with Bootstrapping method')

st.write("First let's define the MDE (Minumum Detectable Effect)")
st.write("MDE is the smallest improvement you are willing to be able to detect.")
st.write("Let's say, you expect to see at least 0.2 minute improvement on the Variant group, then set MDE = 0.2")
st.caption("If you just want to compare which group has bigger mean, let MDE=0.0")
MDE = st.number_input('What is your MDE?', min_value=0.0, value=0.0, step=0.1)

p_val = func.p_value_with_bootstrapping(data[data['Group']=='Control'], data[data['Group']=='Variant'], col_name='IGT', mde=MDE)

# Conclusion
st.subheader('Conclusion')
func.conclusion()