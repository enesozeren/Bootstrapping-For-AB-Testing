from tokenize import group
import pandas as pd
import numpy as np
import random
import streamlit as st
#import matplotlib.pyplot as plt
import os

#Setting up the page
st.set_page_config(page_title='Simulation for A/B Testing')
st.header('A/B Testing with Simulation')
st.caption('This study shows a way to make an A/B Test with small sample sizes where the required assumptions cannot be satisfied for hypothesis testing.')
st.caption('The method applied in this study also can be used for A/B Testing by the ones who do not have a statistical background.')

st.subheader('Case')
st.write('In a mobile game, marketing team tries to see the effect of the frequenct of ads which players are exposed.')
st.write('There are 2 groups of players: \n1) Exposed to ads in every 3 minutes \n2) Exposed to ads in every 4 minutes')
st.write('We will test if the frequency of the ads changes the played game rounds (sum_gamerounds) of players.')

#Data import
os.chdir("/Users/eno/Documents/Data_Analytics/Simulation_for_AB_Testing_Project/Project")
data = pd.read_csv('game_data.csv')
st.subheader('Gamerounds played by players')
st.dataframe(data)
st.write(f'Size: {len(data)} rows')

#Data Groups
interval_3 = data[data['ad_interval']=='3_min'].reset_index(drop=True)
interval_4 = data[data['ad_interval']=='4_min'].reset_index(drop=True)

#Summary of Data
st.subheader('Summary of Data')
summary_table = data.groupby('ad_interval').agg(['mean', 'size'])['sum_gamerounds']
st.dataframe(summary_table)
st.bar_chart(summary_table['mean'])


group_difference = round(interval_4['sum_gamerounds'].mean() - interval_3['sum_gamerounds'].mean(), 2)
st.write(f"Difference of Means (Group 4_min - Group 3_min) {group_difference}")
st.write('Is the difference enough to make a conclusion about the effect of the ads intervals?')
st.write("Let's see how confident we are when saying the players who see ads in every 4 minutes play more rounds when compared with the other group!")

#Explaning the logic of the simulation
st.subheader('Logic of the Simulation')
see_logic = st.checkbox('See The Logic of the Simulation')

if see_logic:
    st.write('1) Generate 2 groups randomly')
    random.seed(10)
    random_index_list = random.sample(range(len(data)), 20)
    first_group = data[data.index.isin(random_index_list)]
    second_group = data[~data.index.isin(random_index_list)]

    #Creating random groups
    st.caption('Group 1')
    st.dataframe(first_group)
    st.caption(f"Size of Group 1: {len(first_group)}")
    st.caption(f"Mean Gamerounds for Group 1: {round(first_group['sum_gamerounds'].mean(),2)}")
    st.caption('Group 2')
    st.dataframe(second_group)
    st.caption(f"Size of Group 2: {len(second_group)}")
    st.caption(f"Mean Gamerounds for Group 2: {round(second_group['sum_gamerounds'].mean(),2)}")
    if ((second_group['sum_gamerounds'].mean()-first_group['sum_gamerounds'].mean()) >= group_difference):
        st.caption(f"(Group 2 Mean - Group 1 Mean: {(second_group['sum_gamerounds'].mean()-first_group['sum_gamerounds'].mean())}) >= (Interval 4 Mean - Interval 3 Mean: {group_difference})")
    else:
        st.caption(f"(Group 2 Mean - Group 1 Mean: {(second_group['sum_gamerounds'].mean()-first_group['sum_gamerounds'].mean())}) < (Interval 4 Mean - Interval 3 Mean: {group_difference})")


    st.write('\n2) Do the same operation for 10 times (Number of Simulation Runs = 10)')
    difference_list = []
    for i in range(10):

            random_index_list = random.sample(range(len(data)), 20)
            
            first_sample_mean = data[data.index.isin(random_index_list)]['sum_gamerounds'].mean()    
            second_sample_mean = data[~data.index.isin(random_index_list)]['sum_gamerounds'].mean()
            
            difference_list.append(second_sample_mean - first_sample_mean)
        
    st.write(difference_list)
    st.caption('There is 1 simulation run where (Group 2 Mean - Group 1 Mean) >= 41.62 (Interval 4 Mean - Interval 3 Mean)')
    st.caption("This means: The difference for Interval 4 Mean and Interval 3 Mean can be randomly generated %10 of time ")


def p_value_with_simulation(group_a, group_b) -> float:
    """This is a simulation which returns the p-value for group_a > group_b"""
    size_a = len(group_a)
    difference = round(group_a['sum_gamerounds'].mean() - group_b['sum_gamerounds'].mean(), 3)
    
    all_samples = pd.concat([group_a, group_b])

    difference_list = []

    numb_of_simulations = st.slider('Number of Simulation Runs:', min_value=20, max_value=10000)

    for i in range(numb_of_simulations):

        random_index_list = random.sample(range(len(all_samples)), size_a)
        
        first_sample_mean = all_samples[all_samples.index.isin(random_index_list)]['sum_gamerounds'].mean()    
        second_sample_mean = all_samples[~all_samples.index.isin(random_index_list)]['sum_gamerounds'].mean()
        
        difference_list.append(second_sample_mean - first_sample_mean)
    
    
    hist_values = np.histogram((list(difference_list)), bins=50)[0]
    st.bar_chart(hist_values)
    st.caption('The distribution of differences between groups')

    return round(len(list((filter(lambda x: x > difference, difference_list ))))/numb_of_simulations, 3)

st.subheader('Simulation')
st.write("P-Value: Percentage of times where difference between random groups is greater than the difference between interval_4 and interval_3 group")
p_val = p_value_with_simulation(interval_4, interval_3)
st.write(f"P-Value: {p_val}")

st.subheader('Conclusion')
st.write(f"We can say that {p_val*100}% of time the observed difference ({group_difference}) can be explained by randomness.")
st.write(f"In other words we are {100-p_val*100}% certain that players who see ads in every 4 minutes play more rounds than the ones who see it in every 3 minutes.")