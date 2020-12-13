#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 12:58:38 2020

@author: heyishan
"""
import webbrowser
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re


pd.set_option('display.max_columns', 1000) 
pd.set_option('display.max_rows', 1000) 
pd.set_option('display.width', 1000)

headers = {"User-Agent": "Safari"}
site = "https://www.espn.com/nba/teams"

teams = requests.get(site, headers=headers)
teams.raise_for_status()

teams = BeautifulSoup(teams.text, 'html.parser')

teamLinks = teams.select('.TeamLinks__Link a')

rosterLinks=[]
for link in teamLinks:
    if link.text=="Roster":
        rosterLinks.append('https://www.espn.com' + link['href'])

players = []
information = []
teamDict = {}
teamNames1 = []
teamNames2 = []
playersCount = []

# Go into each team's page
for team in rosterLinks:
    teamPage = requests.get(team, headers=headers)
    teamPage = BeautifulSoup(teamPage.text, 'html.parser')
    
    # Get the cities and the names of the teams
    teamCities = teamPage.select("span[class='db pr3 nowrap']")
    teamNames = teamPage.select("span[class='db fw-bold']")
    for teamCity in teamCities:
        teamNames1.append(teamCity.text.strip())
    for teamName in teamNames:
        teamNames2.append(teamName.text.strip())
    
    # Extract the names and information about the players of each team from the website   
    teamPlayers = teamPage.select("a[class='AnchorLink']")
    infos = teamPage.select("div[class='inline']")
    
    # Get a list of all players
    for teamPlayer in teamPlayers[1::2]:
        players.append(teamPlayer.text.strip())
        
    # Get a list of all player's information     
    for info in infos:
        information.append(info.text.strip())
    # Get the accumulated count of players in the whole NBA
    playersCount.append(len(players))
#print(playersCount)

# Get the jersey number of each player
nums = []
for player in information[0::7]:
    results = re.findall("\d*", player)
    nums.append(results[-2])
   
# Get the complete team names    
teams = []
for i in range(len(teamNames1)):
   teamNames = teamNames1[i] + " " + teamNames2[i]
   teams.append(teamNames)
#print(teams)

# Create column titles and calculate the rows and columns needed for a dataframe
columns = ["Name", "Position", "Age", "Height", "Weight", "College", "Salary"] 
row = len(players)
column = len(columns)

# Put everything in a dataframe
df = pd.DataFrame(np.array(information).reshape(row,column), columns = columns)
#Add a new column Number to store the players' jersey number 
df["Number"] = nums

# Reformat the dataframe
df = df.reindex(columns = ["Name", "Number", "Position", "Age", "Height", "Weight", "College", "Salary"])
df.Name = df.Name.str.extract('(^\D*)')
df.replace('--', np.nan, inplace = True) 
#df.replace('', np.nan, inplace = True) 

df["WeightNum"] = df.Weight.str.split().str.get(0).astype(float)
df["Feet"] = df.Height.str.split().str.get(0).str.strip("'").astype(float)
df["Inches"] = df.Height.str.split().str.get(1).str.strip("\"").astype(float)
df["HeightNum"] = df.Feet * 12 + df.Inches
df["SalaryNum"] = df.Salary.str.split("$").str.get(1).str.replace(",", "").astype(float)
df["Team"] = ""


# Create a list to count the number of players on a team
count = []
for x, y in zip(playersCount[0::], playersCount[1::]): 
    count.append(y-x) 
count.insert(0, playersCount[0])    
#print(count)
 
# Update the team name for each player
df.iloc[:count[0] +1, -1] = teams[0]   
for i in range(1,len(count)):
    start = playersCount[i-1]
    end = playersCount[i] +1 
    team = teams[i]
    #print(start, end, team)
    df.iloc[start:end, -1] = team 

df = df.fillna("")
pd.DataFrame.to_csv(df, "NBAPlayers.csv")




  