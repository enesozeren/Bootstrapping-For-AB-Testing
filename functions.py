import numpy as np
import pandas as pd
import streamlit as st
from sklearn.utils import shuffle

def streamlit_setup():
    st.set_page_config(page_title='A/B Testing with Bootstrapping')
    st.header('A/B Testing with Bootstrapping')
    st.write('This study shows an implementation of Bootstrapping Method in A/B testing with an example case.')
    st.write('The method applied in this study is easy to understand for people with no statistical background and also easy to implement.')

    st.subheader('Case')
    st.write('A mobile game company wants to increase their players in game time.')
    st.write('So that they decided to test showing adds to the players less frequent. Currently a player is exposed to ads in every 3 minutes.')
    st.write('The team wants the test adds with 4 minutes interval.')
    st.write('Therefore, we have 2 groups and 1 metric for the test')
    st.write('1) Control: Exposed to ads in every 3 minutes \n2) Variant: Exposed to ads in every 4 minutes')
    st.write('METRIC: Average in game time of the customer (Avg IGT)')
    st.write('We will test if the less frequent ad exposure increased Avg IGT.')

def generate_data()-> pd.DataFrame:
    np.random.seed(34)
    control_group_igt = np.random.normal(loc=20, scale=5, size=10_500)
    control_user_ids = np.arange(0, 10_500)
    control_df = pd.DataFrame({'User ID': control_user_ids, 'Group': 'Control', 'IGT': control_group_igt})

    variant_group_igt = np.random.normal(loc=22, scale=5, size=11_000)
    variant_user_ids = np.arange(10_500, 10_500+11_000)
    variant_df = pd.DataFrame({'User ID': variant_user_ids, 'Group': 'Variant', 'IGT': variant_group_igt})

    data = pd.concat([control_df, variant_df])
    data = shuffle(data)
    
    return data