#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:16:38 2020

@author: heyishan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # control interaction
import plotly.express as px # mini version of plotly

# Read the two files
players = pd.read_csv("NBAPlayers.csv", index_col = [0])
players['Number'] = players['Number'].astype('Int64')
#players['Age'] = players['Age'].astype('Int64')
stats = pd.read_csv("playerStat.csv")

# Merge the two data frames
df = pd.merge(players, stats, how = "left", left_on = "Name", right_on = "Unnamed: 0")
df.Salary = df.Salary.str.split("$").str.get(1).str.replace(",", "").astype(float)
df["FG_High"] = df.FG.str.split("-").str.get(1).astype(float)
df["FG_Low"] = df.FG.str.split("-").str.get(0).astype(float)
df["3PT_High"] = df["3PT"].str.split("-").str.get(1).astype(float)
df["3PT_Low"] = df["3PT"].str.split("-").str.get(0).astype(float)
df["FT_High"] = df.FT.str.split("-").str.get(1).astype(float)
df["FT_Low"] = df.FT.str.split("-").str.get(0).astype(float)

df["Age"] = df["Age"].fillna(0)


ageMin = 18
ageMax = int(max(df.Age))
age = list(range(ageMin-2, ageMax+2))

ageCount = pd.DataFrame(age, columns = ["Age"])
print(ageCount)
ageCount["Count"] = 0

'''
for i in df.Age:
    for age in ageCount.Age:
        if i == age:
            ageCount.Count[age] += 1
'''            
print(ageCount)

countAge = Counter(df.Age)

age = list(countAge.keys()) 
count = list(countAge.values()) 


fig = plt.figure(figsize = (10, 5)) 
 
# creating the bar chart
plt.bar(age, count, color ='green',  width = 0.7) 
    
#plt.xticks(age)
plt.grid(True)
plt.grid(linestyle='--')
plt.xlabel("Age", fontsize = 15) 
plt.ylabel("Number of Players", fontsize = 15) 
plt.title("Age Summary of NBA Players", fontsize = 18) 
plt.show() 



# Create a dashboard
# Show the table filter by Team
df2 = df.reindex(columns = ['Name', 'Number', 'Position', 'Age', 'Height', 'Weight', 'College',
       'Salary', 'Team', 'GP', 'GS', 'MIN', 'FG', 'FG%', '3PT', '3P%',
       'FT', 'FT%', 'OR', 'DR', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS'])
df2 = df2.replace(np.nan, '', regex=True)
print(df2)

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server


app.layout = html.Div([
    # Create a header and style it
    html.H1('Explore the data of your favorite NBA Team!', style={'textAlign': 'center'}),
    # Generate a table
     html.Div([html.H5("Dropdown: "),
              dcc.Dropdown(options=[{'label': 'Atlanta Hawks', 'value': 'Atlanta Hawks'},
                                    {'label': 'Boston Celtics', 'value': 'Boston Celtics'},
                                    {'label': 'Brooklyn Nets', 'value': 'Brooklyn Nets' }],
                                    {'label': 'Charlotte Hornets', 'value': 'Charlotte Hornets'}],
                                    {'label': 'Chicago Bulls', 'value': 'Chicago Bulls'}],
                                    {'label': 'Cleveland Cavaliers', 'value': 'Cleveland Cavaliers'}],
                                    {'label': 'Dallas Mavericks', 'value': 'Dallas Mavericks'}],
                                    {'label': 'Denver Nuggets', 'value': 'Denver Nuggets'}],
                                    {'label': 'Detroit Pistons', 'value': 'Detroit Pistons'}],
                                    {'label': 'Golden State Warriors', 'value': 'Golden State Warriors'}],
                                    {'label': 'Houston Rockets', 'value': 'Houston Rockets'}],
                                    {'label': 'Indiana Pacers', 'value': 'Indiana Pacers'}],
                                    {'label': 'Los Angeles Clippers', 'value': 'Los Angeles Clippers'}],
                                    {'label': 'Los Angeles Lakers', 'value': 'Los Angeles Lakers'}],
                                    {'label': 'Memphis Grizzlies', 'value': 'Memphis Grizzlies'}],
                                    {'label': 'Miami Heat', 'value': 'Miami Heat'}],
                                    {'label': 'Milwaukee Bucks', 'value': 'Milwaukee Bucks'}],
                                    {'label': 'Minnesota Timberwolves', 'value': 'Minnesota Timberwolves'}],
                                    {'label': 'New Orleans Pelicans', 'value': 'New Orleans Pelicans'}],
                                    {'label': 'New York Knicks', 'value': 'New York Knicks'}],
                                    {'label': 'Oklahoma City Thunder', 'value': 'Oklahoma City Thunder'}],                                    {'label': 'Memphis Grizzlies', 'value': 'Or'}],
                                    {'label': 'Orlando Magic', 'value': 'Orlando Magic'}],
                                    {'label': 'Philadelphia 76ers', 'value': 'Philadelphia 76ers'}],
                                    {'label': 'Phoenix Suns', 'value': 'Phoenix Suns'}],
                                    {'label': 'Portland Trail Blazers', 'value': 'Portland Trail Blazers'}],
                                    {'label': 'Sacramento Kings', 'value': 'Sacramento Kings'}],
                                    {'label': 'San Antonio Spurs', 'value': 'San Antonio Spurs'}],
                                    {'label': 'Toronto Raptors', 'value': 'Toronto Raptors'}],
                                    {'label': 'Utah Jazz', 'value': 'Utah Jazz'}],
                                    {'label': 'Washington Wizards', 'value': 'Washington Wizards'}],
    
                           id='my-dropdown',
                           value='Ap'),
             generate_table(df2, id='my_table'),
    ])
@app.callback(
    Output(component_id='my_table', component_property='row'),
    [Input(component_id='my-dropdown', component_property='value')]

)

def update_rows(selected_value):
    df2 = df2[df2['Team'] == selected_value]
    return df2


if __name__ == '__main__':
    app.run_server(debug=True)

