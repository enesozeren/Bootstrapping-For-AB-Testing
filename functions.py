import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

def page_setup():
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
    np.random.seed(7)
    size_of_control = 1_500
    control_group_igt = np.random.normal(loc=20, scale=5, size=size_of_control)
    control_user_ids = np.arange(0, size_of_control)
    control_df = pd.DataFrame({'User ID': control_user_ids, 'Group': 'Control', 'IGT': control_group_igt})

    size_of_variant = 1_100
    variant_group_igt = np.random.normal(loc=20.5, scale=6, size=size_of_variant)
    variant_user_ids = np.arange(size_of_control, size_of_control+size_of_variant)
    variant_df = pd.DataFrame({'User ID': variant_user_ids, 'Group': 'Variant', 'IGT': variant_group_igt})

    data = pd.concat([control_df, variant_df])
    data = shuffle(data)
    
    return data

def summary_of_data(data):
    st.write(f"Total Client Volume: {data['User ID'].nunique()}")

    diff = data[data['Group']=='Variant']['IGT'].mean() - data[data['Group']=='Control']['IGT'].mean()
    lift = round((diff/ data[data['Group']=='Control']['IGT'].mean()), 3)

    col1, col2 = st.columns(2)
    col1.metric("Control Group Client Volume", f"{data[data['Group']=='Control']['User ID'].nunique()}")
    col2.metric("Control Group Avg IGT", f"{round(data[data['Group']=='Control']['IGT'].mean(), 3)}")

    col3, col4 = st.columns(2)
    col3.metric("Variant Group Client Volume", f"{data[data['Group']=='Variant']['User ID'].nunique()}")
    col4.metric("Variant Group Avg IGT", f"{round(data[data['Group']=='Variant']['IGT'].mean(), 3)}", f"{lift*100}%")

    st.write(f"Difference between Variant and Control groups for Avg IGT: {round(diff, 3)}")
    st.write(f'Avg IGT is {lift*100}% up for Variant group. However, how statistically significant is the difference?')

def p_value_with_bootstrapping(control_df: pd.DataFrame, variant_df: pd.DataFrame, col_name: str, number_of_samples=10_000, alpha=0.05) -> float:
    
    control_values = control_df[col_name].values
    variant_values = variant_df[col_name].values

    difference = round(np.mean(variant_values) - np.mean(control_values), 3)

    difference_list = []

    number_of_samples = st.slider('Number of Bootstrap Samples:', min_value=20, max_value=20_000)

    for i in range(number_of_samples):
        
        first_sample_mean = np.mean(np.random.choice(a=control_values, size=len(control_values), replace=True))
        second_sample_mean = np.mean(np.random.choice(a=variant_values, size=len(variant_values), replace=True))
        
        difference_list.append(second_sample_mean - first_sample_mean)
    
    fig, ax = plt.subplots()
    ax.hist(difference_list, bins=50)
    plt.xlabel('Avg IGT difference between bootstrap samples')
    plt.ylabel('# of observed difference')
    st.pyplot(fig)
    st.caption('The distribution of differences between bootstrap samples')

    p_value = round(1 - len(list((filter(lambda x: x > 0, difference_list ))))/number_of_samples, 3)
    st.write(f"P-Value = {p_value}")

    if p_value <= alpha:
        st.write(f"We can say that {col_name} is improved since P-Value({p_value}) <= Alpha({alpha})")
    else:
        st.write(f"We can NOT say that {col_name} is improved since P-Value({p_value}) > Alpha({alpha})")

    confidence_interval_for_difference = {'Lower Bound': np.quantile(difference_list, q=alpha/2), 'Upper Bound': np.quantile(difference_list, q=1-alpha/2)}
    st.write(f"The {(1-alpha)*100}% confidence interval for Avg IGT Difference between Variant & Control Groups:")
    st.write(confidence_interval_for_difference)
    


    return p_value
