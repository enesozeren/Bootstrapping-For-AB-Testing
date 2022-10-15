from dataclasses import replace
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from PIL import Image

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

def bootstrap_method_exp():
    st.write('Bootstraping is any test or metric that uses random sampling with replacement and falls under the broader class of resampling methods.')

    bootstrap_image = Image.open('bootstrap_image.png')
    st.image(bootstrap_image, caption='Bootstrapping Diagram by blogs.sas.com')

    st.write('Just like in the diagram, we take N resamples from our Control and Variant groups with size is equal to the group itself.')
    st.write('We set N (Number of Bootstrap Samples) as large enough. You can play with different N values below to see how it effects the results.')
    st.write('With this N samples we can generate the boostrap distribution for our Control and Variant Group means (In our case Avg IGT).')

    st.write("Let's demonstrate the boostrapping with N=1 to understand")
    dummy_control = [5, 2, 2, 1, 4]
    dummy_variant = [6, 7, 8, 9, 20, 11]

    st.write(f"Dummy Control Group IGTs: {dummy_control}")
    st.write(f"Dummy Variant Group IGTs: {dummy_variant}")
    bootstrap_sample_control = np.random.choice(dummy_control, size=len(dummy_control), replace=True)
    st.write(f"Bootstrap sample from Control: {bootstrap_sample_control} and Mean of Bootstrap Sample: {round(np.mean(bootstrap_sample_control), 2)}")
    bootstrap_sample_variant = np.random.choice(dummy_variant, size=len(dummy_variant), replace=True)
    st.write(f"Bootstrap sample from Control: {bootstrap_sample_variant} and Mean of Bootstrap Sample: {round(np.mean(bootstrap_sample_variant), 2)}")

    st.write(f"Variant Mean - Control Mean = {round(np.mean(bootstrap_sample_variant) - np.mean(bootstrap_sample_control), 2)}")

    st.write("We do this for N times, and then we have the distribution of difference between Variant and Control. And with that distribution we can calculate p-values.")

def p_value_with_bootstrapping(control_df: pd.DataFrame, variant_df: pd.DataFrame, col_name: str, number_of_samples=10_000, alpha=0.05, mde=0) -> float:
    
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

    st.write(f'Observed Difference (Variant - Control) = {difference}')
    p_value = round(1 - len(list((filter(lambda x: x > 0 + mde, difference_list ))))/number_of_samples, 3)
    st.write(f"P-Value = {p_value}")

    if p_value <= alpha:
        st.write(f"We can say that {col_name} is improved at the level of our MDE since P-Value({p_value}) <= Alpha({alpha})")
    else:
        st.write(f"We can NOT say that {col_name} is improved  at the level of our MDE since P-Value({p_value}) > Alpha({alpha})")

    confidence_interval_for_difference = {'Lower Bound': np.quantile(difference_list, q=alpha/2), 'Upper Bound': np.quantile(difference_list, q=1-alpha/2)}
    st.write(f"The {(1-alpha)*100}% confidence interval for Avg IGT Difference between Variant & Control Groups:")
    st.write(confidence_interval_for_difference)
    


    return p_value

def conclusion():
    st.write('The Pros and Cons of Bootstrapping for A/B Testing are listed below')

    st.write('PROS')
    st.write('1) We do not make any assumptions about the distribution of our metric')
    st.write('2) No required sample size for the test.')
    st.write('3) Easy to implement and understand')

    st.write('CONS')
    st.write('1) With big data, this bootstrap simulation approach has computational burden')
