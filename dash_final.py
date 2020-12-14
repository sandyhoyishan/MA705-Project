#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:53:41 2020

@author: heyishan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:16:38 2020

@author: heyishan
"""

import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # control interaction
import plotly.io as pio

pio.templates.default = "seaborn"


# Read the two files
players = pd.read_csv("NBAPlayers.csv", index_col = [0])
players['Number'] = players['Number'].astype('Int64')
#players['Age'] = players['Age'].astype('Int64')
stats = pd.read_csv("playerStat.csv")

# Merge the two data frames and clean up the data
df = pd.merge(players, stats, how = "left", left_on = "Name", right_on = "Unnamed: 0")
df.Salary = df.Salary.str.split("$").str.get(1).str.replace(",", "").astype(float)
df["FG_High"] = df.FG.str.split("-").str.get(1).astype(float)
df["FG_Low"] = df.FG.str.split("-").str.get(0).astype(float)
df["FG"] = round((df["FG_High"] + df["FG_Low"])/2,2)
df["3PT_High"] = df["3PT"].str.split("-").str.get(1).astype(float)
df["3PT_Low"] = df["3PT"].str.split("-").str.get(0).astype(float)
df["3PT"] = round((df["3PT_High"] + df["3PT_Low"])/2,2)
df["FT_High"] = df.FT.str.split("-").str.get(1).astype(float)
df["FT_Low"] = df.FT.str.split("-").str.get(0).astype(float)
df["FT"] = round((df["FT_High"] + df["FT_Low"])/2,2)



df2 = df.reindex(columns = ['Name', 'Number', 'Position', 'Age', 'Height', 'Weight', 'College',
       'Salary', 'Team', 'GP', 'GS', 'MIN', 'FG', 'FG%', '3PT', '3P%',
       'FT', 'FT%', 'OR', 'DR', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS'])
df2 = df2.replace(np.nan, '', regex=True)

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=stylesheet)

server = app.server

fig01 = px.bar(df, x="Name", y="Age")
fig02 = px.bar(df, x="Name", y="HeightNum")
fig03 = px.bar(df, x="Name", y="WeightNum")
fig04 = px.bar(df, x="Name", y="SalaryNum")
fig11 = px.bar(df, x="Name", y="PTS")
fig12 = px.bar(df, x="Name", y="TO")
fig13 = px.bar(df, x="Name", y="PF")
fig14 = px.bar(df, x="Name", y="STL")
fig15 = px.bar(df, x="Name", y="BLK")
fig16 = px.bar(df, x="Name", y="AST")
fig17 = px.bar(df, x="Name", y="REB")
fig18 = px.bar(df, x="Name", y="FT%")
fig19 = px.bar(df, x="Name", y="3P%")
fig20 = px.bar(df, x="Name", y="FG%")


markdown_text = "Want to discover some interesting facts about your favorite NBA teams? You've come to the right place!"
markdown_text1 = "Below are some graphs that show the information and perfomance for players on each team. \n Update the graphs by selecting different teams."
markdown_text2 = "Click on the stat that you're interested in."


app.layout = html.Div([
    # Create a header and style it
    
    html.H1('Explore your favorite NBA Teams!', style={'textAlign': 'center'}, id="top"),
    dcc.Markdown(children=markdown_text),
    html.Div([html.H4("Choose your favorite teams: "),
              dcc.Dropdown(options=[{'label': 'Atlanta Hawks', 'value': 'Atlanta Hawks'},
                                    {'label': 'Boston Celtics', 'value': 'Boston Celtics'},
                                    {'label': 'Brooklyn Nets', 'value': 'Brooklyn Nets' },
                                    {'label': 'Charlotte Hornets', 'value': 'Charlotte Hornets'},
                                    {'label': 'Chicago Bulls', 'value': 'Chicago Bulls'},
                                    {'label': 'Cleveland Cavaliers', 'value': 'Cleveland Cavaliers'},
                                    {'label': 'Dallas Mavericks', 'value': 'Dallas Mavericks'},
                                    {'label': 'Denver Nuggets', 'value': 'Denver Nuggets'},
                                    {'label': 'Detroit Pistons', 'value': 'Detroit Pistons'},
                                    {'label': 'Golden State Warriors', 'value': 'Golden State Warriors'},
                                    {'label': 'Houston Rockets', 'value': 'Houston Rockets'},
                                    {'label': 'Indiana Pacers', 'value': 'Indiana Pacers'},
                                    {'label': 'Los Angeles Clippers', 'value': 'Los Angeles Clippers'},
                                    {'label': 'Los Angeles Lakers', 'value': 'Los Angeles Lakers'},
                                    {'label': 'Memphis Grizzlies', 'value': 'Memphis Grizzlies'},
                                    {'label': 'Miami Heat', 'value': 'Miami Heat'},
                                    {'label': 'Milwaukee Bucks', 'value': 'Milwaukee Bucks'},
                                    {'label': 'Minnesota Timberwolves', 'value': 'Minnesota Timberwolves'},
                                    {'label': 'New Orleans Pelicans', 'value': 'New Orleans Pelicans'},
                                    {'label': 'New York Knicks', 'value': 'New York Knicks'},
                                    {'label': 'Oklahoma City Thunder', 'value': 'Oklahoma City Thunder'},                                    
                                    {'label': 'Orlando Magic', 'value': 'Orlando Magic'},
                                    {'label': 'Philadelphia 76ers', 'value': 'Philadelphia 76ers'},
                                    {'label': 'Phoenix Suns', 'value': 'Phoenix Suns'},
                                    {'label': 'Portland Trail Blazers', 'value': 'Portland Trail Blazers'},
                                    {'label': 'Sacramento Kings', 'value': 'Sacramento Kings'},
                                    {'label': 'San Antonio Spurs', 'value': 'San Antonio Spurs'},
                                    {'label': 'Toronto Raptors', 'value': 'Toronto Raptors'},
                                    {'label': 'Utah Jazz', 'value': 'Utah Jazz'},
                                    {'label': 'Washington Wizards', 'value': 'Washington Wizards'}],
                           id='my-dropdown',
                           multi = True,
                           style={'width': '300px'},
                           placeholder="Select a team"),
            html.H2('Player Stats', style={'textAlign': 'center'}),
            dt.DataTable(id='my_table', 
                         columns=[{"name": i, "id": i} for i in df2.columns.values],
                         style_cell={'textAlign': 'left', 'border': '1px solid grey'},
                         sort_action='native',
                         style_table={'overflowY': 'auto'},
                         style_header={'backgroundColor': 'white','fontWeight': 'bold'},
                         data=df2.to_dict("rows")),
            html.Br(),
                   
            html.H2('Team Stats Visualization', style={'textAlign': 'center'}),
            dcc.Markdown(children=markdown_text1),
            dcc.Markdown(children=markdown_text2),  
            html.A("Personal Information"),
            html.Br(),
            html.A("Age", href="#Age-graph"),
            html.Br(),
            html.A("Height", href="#Height-graph"),
            html.Br(),
            html.A("Weight", href="#Weight-graph"),
            html.Br(),
            html.A("Salary", href="#Salary-graph"),
            html.Br(),
            html.Br(),
            html.A("Performance"),
            html.Br(),
            html.A("Points", href="#PTS-graph"), 
            html.Br(),
            html.A("Turnover", href="#TO-graph"),
            html.Br(),
            html.A("Fouls", href="#PF-graph"),
            html.Br(),
            html.A("Steals", href="#STL-graph"),
            html.Br(),
            html.A("Blocks", href="#BLK-graph"),
            html.Br(),
            html.A("Assists", href="#AST-graph"),
            html.Br(),
            html.A("Rebounds", href="#REB-graph"),
            html.Br(),
            html.A("Free Throw %", href="#FT%-graph"),
            html.Br(),
            html.A("Three-pointers %", href="#3P%-graph"),
            html.Br(),
            html.A("Field Goals %", href="#FG%-graph"),
            html.Br(),
            
            html.H3('Personal Information', style={'textAlign': 'center'}),
            dcc.Graph(id='Age-graph', figure=fig01),
            dcc.Graph(id='Height-graph', figure=fig02),
            dcc.Graph(id='Weight-graph', figure=fig03),
            dcc.Graph(id='Salary-graph', figure=fig04),
            html.H3('Performance', style={'textAlign': 'center'}),
            dcc.Graph(id='PTS-graph', figure=fig11),
            dcc.Graph(id='TO-graph', figure=fig12),
            dcc.Graph(id='PF-graph', figure=fig13),
            dcc.Graph(id='STL-graph', figure=fig14),
            dcc.Graph(id='BLK-graph', figure=fig15),
            dcc.Graph(id='AST-graph', figure=fig16),
            dcc.Graph(id='REB-graph', figure=fig17),
            dcc.Graph(id='FT%-graph', figure=fig18),
            dcc.Graph(id='3P%-graph', figure=fig19),
            dcc.Graph(id='FG%-graph', figure=fig20),
            html.A('Data Source:'),
            html.A("https://www.espn.com/nba/", href="https://www.espn.com/nba/"),
            html.Br(),
            html.A("Back to top", href="#top")
    ])
])

            
@app.callback(
    Output(component_id='my_table', component_property='data'),
    #Output(component_id='my-graph', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value')]

)

def display_table(value):
    if value is not None:
        if type(value) == "str":
            dff = df2[df2['Team']==value]
        else:
            dff = df2[df2['Team'].isin(value)]
        dff = dff.sort_values(by = "Name")
    else:
        dff = df2
    return dff.to_dict('records')

@app.callback(
    Output(component_id='Age-graph', component_property='figure'),
    Output(component_id='Height-graph', component_property='figure'),
    Output(component_id='Weight-graph', component_property='figure'),
    Output(component_id='Salary-graph', component_property='figure'),
    Output(component_id='PTS-graph', component_property='figure'),
    Output(component_id='TO-graph', component_property='figure'),  
    Output(component_id='PF-graph', component_property='figure'),
    Output(component_id='STL-graph', component_property='figure'),
    Output(component_id='BLK-graph', component_property='figure'),
    Output(component_id='AST-graph', component_property='figure'),
    Output(component_id='REB-graph', component_property='figure'),
    Output(component_id='FT%-graph', component_property='figure'),
    Output(component_id='3P%-graph', component_property='figure'),
    Output(component_id='FG%-graph', component_property='figure'),    
    [Input(component_id='my-dropdown', component_property='value')]

)

def display_graph(value):
    if value is not None:
        if type(value) == "str":
            df_team = df[df.Team == value]
        else:
            df_team = df[df.Team.isin(value)]
    else:
        df_team = df
    df_team = df_team.sort_values(by = "Name")
    fig01 = px.bar(df_team, x="Name", y="Age", title="Age", color = "Team", text = "Age",
                   labels={"Name": "Player Name"})
    fig02 = px.bar(df_team, x="Name", y="HeightNum", title = "Height ", color = "Team",
                   labels={"Name": "Player Name", "HeightNum": "Height (inches) "}, text = "HeightNum")
    fig03 = px.bar(df_team, x="Name", y="WeightNum", title = "Weight ", color = "Team",
                   labels={"Name": "Player Name", "WeightNum": "Weight (lbs)"}, text = "WeightNum")
    fig04 = px.bar(df_team, x="Name", y="SalaryNum", title = "Salary", color = "Team",
                   labels={"Name": "Player Name", "SalaryNum": "Salary"}, text = "SalaryNum")
    fig11 = px.bar(df_team, x="Name", y="PTS", title = "Average Points per Game", color = "Team",
                   labels={"Name": "Player Name", "PTS": "PTS (per game)"}, text = "PTS")
    fig12 = px.bar(df_team, x="Name", y="TO", title = "Average Turnover per Game", color = "Team",
                   labels={"Name": "Player Name", "TO": "TO (per game)"}, text = "TO")
    fig13 = px.bar(df_team, x="Name", y="PF", title = "Average Fouls per Game", color = "Team",
                   labels={"Name": "Player Name", "PF": "PF (per game)"}, text = "PF")
    fig14 = px.bar(df_team, x="Name", y="STL", title = "Average Steals per Game", color = "Team",
                   labels={"Name": "Player Name", "STL": "STL (per game)"}, text = "STL")
    fig15 = px.bar(df_team, x="Name", y="BLK", title = "Average Blocks per Game", color = "Team",
                   labels={"Name": "Player Name", "BLK": "BLK (per game)"}, text = "BLK")
    fig16 = px.bar(df_team, x="Name", y="AST", title = "Average Assists per Game", color = "Team",
                   labels={"Name": "Player Name", "AST": "AST (per game)"}, text = "AST")
    fig17 = px.bar(df_team, x="Name", y="REB", title = "Average Rebounds per Game", color = "Team",
                   labels={"Name": "Player Name", "REB": "REB (per game)"}, text = "PF")
    fig18 = px.bar(df_team, x="Name", y="FT%", title = "Free Throw Percentage", color = "Team",
                   labels={"Name": "Player Name"} , text = "FT%")
    fig19 = px.bar(df_team, x="Name", y="3P%", title = "3-Point Field Goal Percentage", color = "Team",
                   labels={"Name": "Player Name"} , text = "3P%")
    fig20 = px.bar(df_team, x="Name", y="FG%", title = "Field Goal Percentage", color = "Team",
                   labels={"Name": "Player Name"} , text = "FG%")
    
    fig01.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig02.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig03.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig04.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig11.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig12.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig13.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig14.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig15.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig16.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig17.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig18.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig19.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig20.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    fig01.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig02.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig03.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig04.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig11.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig01.update_layout(height=600)
    fig02.update_layout(height=600)
    fig03.update_layout(height=600)
    fig04.update_layout(height=600)
    fig11.update_layout(height=600)
    fig12.update_layout(height=600)
    fig13.update_layout(height=600)
    fig14.update_layout(height=600)
    fig15.update_layout(height=600)
    fig16.update_layout(height=600)
    fig17.update_layout(height=600)
    fig18.update_layout(height=600)
    fig19.update_layout(height=600)
    fig20.update_layout(height=600)
    
    return fig01, fig02, fig03, fig04, fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20 

    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)

