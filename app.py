# -*- coding: utf-8 -*-
"""
Created on Mon May  2 11:38:36 2022

@author: Raimundo
"""
import pandas as pd
import streamlit as st
import plotly.express as px

filename = 'american_soccer_analysis_nwsl_goals-added_goalkeepers_2022-05-02.csv'
df = pd.read_csv(filename).drop('Unnamed: 0', axis = 1)
df = df.sort_values(by = ['Player', 'Season']).reset_index(drop = True)

st.set_page_config(page_title='NWSL GKs')
st.header('NWSL GKs')
#st.subheader('Was the tutorial helpful?')

# --- DF MANIPULATION
g_cols = ('Goals Added', 'Claiming', 'Fielding', 'Handling', 'Passing', 'Shotstopping', 'Sweeping')
for col in df:
    if col in g_cols:
        df.loc[:, col] = round(df[col] * 96/90, 3)
names_dict = {'Goals Added': 'Total g+/90', 'Claiming': 'g+/90 by claiming',
              'Fielding': 'g+/90 by fielding', 'Handling': 'g+/90 by handling',
              'Passing': 'g+/90 by passing', 'Shotstopping': 'g+/90 by shotstopping',
              'Sweeping': 'g+/90 by sweeping', 'Season': 'Year'}
df = df.rename(names_dict, axis = 1)
players = df['Player'].unique().tolist()
years = df['Year'].unique().tolist()

# seasons played
seasons_played = []
for player in players:
    n = len(df[df['Player'] == player])
    seasons_played += list(range(n))
df['Seasons played'] = seasons_played

# --- OPTIONS SELECTION
player_selection = st.multiselect('Player:',
                                    players,
                                    default=['Abby Smith','Jane Campbell', 'Kailen Sheridan'])

time_type_selection = st.selectbox(
     'Time', ('Year', 'Seasons played'))

if time_type_selection == 'Year':
    time_selection = st.slider('Years:',
                        min_value= min(years),
                        max_value= max(years),
                        value=(min(years), max(years)))
else:
    time_selection = st.slider('Seasons played:',
                        min_value= min(seasons_played),
                        max_value= max(seasons_played),
                        value=(min(seasons_played), max(seasons_played)))
    
column_selection = option = st.selectbox(
     'Stat:', ('Total goals added', 'Minutes', 'Claiming', 'Fielding', 'Handling', 'Passing', 'Shotstopping', 'Sweeping'))
if column_selection == 'Total goals added':
    column_selection = 'Goals Added'

# Filter df with selected options 
mask = (df[time_type_selection].between(*time_selection)) & (df['Player'].isin(player_selection))   
filtered_df = df[mask]
# --- PLOT
line = px.line(filtered_df, x = time_type_selection, y = names_dict[column_selection], color = 'Player', markers = True)
st.plotly_chart(line)
st.write('Data: [American Soccer Analysis](https://app.americansocceranalysis.com/#!/nwsl/goals-added/goalkeepers)')

