# -*- coding: utf-8 -*-
"""
Created on Mon May  2 11:38:36 2022

@author: Raimundo
"""
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

filename = 'american_soccer_analysis_nwsl_goals-added_goalkeepers_2022-05-02.csv'
df = pd.read_csv(filename).drop('Unnamed: 0', axis = 1)
df = df.sort_values(by = ['Player', 'Season'])

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
              'Sweeping': 'g+/90 by sweeping'}
df = df.rename(names_dict, axis = 1)
# --- STREAMLIT SELECTION
players = df['Player'].unique().tolist()
years = df['Season'].unique().tolist()

year_selection = st.slider('Seasons:',
                        min_value= min(years),
                        max_value= max(years),
                        value=(min(years), max(years)))

player_selection = st.multiselect('Player:',
                                    players,
                                    default=['Abby Smith','Jane Campbell', 'Kailen Sheridan'])

column_selection = option = st.selectbox(
     'Stat:', ('Total goals added', 'Minutes', 'Claiming', 'Fielding', 'Handling', 'Passing', 'Shotstopping', 'Sweeping'))

if column_selection == 'Total goals added':
    column_selection = 'Goals Added'
    
mask = (df['Season'].between(*year_selection)) & (df['Player'].isin(player_selection))

filtered_df = df[mask]
scatter = px.line(filtered_df, x = 'Season', y = names_dict[column_selection], color = 'Player', markers = True)

st.plotly_chart(scatter)
st.write('Data: [American Soccer Analysis](https://app.americansocceranalysis.com/#!/nwsl/goals-added/goalkeepers)')

