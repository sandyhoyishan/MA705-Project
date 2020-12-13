#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 11:48:20 2020

@author: heyishan
"""

import webbrowser
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 1000) 
pd.set_option('display.max_rows', 1000) 
pd.set_option('display.width', 1000)

headers = {"User-Agent": "Safari"}
site = "https://www.espn.com/nba/teams"

teams = requests.get(site, headers=headers)
teams.raise_for_status()

teams = BeautifulSoup(teams.text, 'html.parser')
teamLinks = teams.select('.TeamLinks__Link a')

# Find the link to each team's page
rosterLinks=[]
player = []
for link in teamLinks:
    if link.text=="Roster":
        rosterLinks.append('https://www.espn.com' + link['href'])
        
# Get the link to each player
for link in rosterLinks:
    teamRoster = requests.get(link, headers=headers)
    teamRoster.raise_for_status()
    teamRoster = BeautifulSoup(teamRoster.text, 'html.parser')
    playerLinks = teamRoster.select('a[class="AnchorLink"]')
    for playerLink in playerLinks[1::2]:
        player.append(playerLink['href'])
        
# Find the link to each player's stat page
playerStatLink = []
for i in player:
    IDs = i.split("/_/")
    playerStatLink.append("https://www.espn.com/nba/player/stats/_/" + IDs[1])

playerStat = []
statTitle = []
playerFirstName = []
playerLastName = []
playerName = []

'''
site2 = 'https://www.espn.com/nba/player/stats/_/id/3917376/jaylen-brown'
JB = requests.get(site2, headers=headers)
JB.raise_for_status()
JB = BeautifulSoup(JB.text, 'html.parser')
stats = JB.select("td[class='fw-bold clr-gray-01 Table__TD']")
columns = JB.select("th[class='Table__TH']")
for stat in stats[1:19]:
    playerStat.append(stat.text.strip())
for column in columns[2:20]:
    if column not in statTitle:
        statTitle.append(column.text.strip())
firstNames = JB.select("span[class='truncate min-w-0 fw-light']")
lastNames = JB.select("span[class='truncate min-w-0']")
for name in firstNames:
    playerFirstName.append(name.text.strip())

for name in lastNames:
    playerLastName.append(name.text.strip()) 

for i in range(len(playerFirstName)):
    playerName.append(playerFirstName[i] +" " + playerLastName[i])
    
print(playerName)
print(playerStat)
print(statTitle)
'''

# Find the index the get rid of players that don't have available stats.
N = len(playerStatLink)
countNum = 0
eliminate = []

for link in playerStatLink[0:N]:   
    players = requests.get(link, headers = headers)
    players.raise_for_status()
    ds = BeautifulSoup(players.text, "html.parser")
    noData = ds.select("div[class='Wrapper Card__Content NoDataAvailable__Content']")
    if noData != []:
        #print(noData)
        #print(countNum)
        eliminate.append(countNum)
    countNum += 1
#print(eliminate)

for i in sorted(eliminate, reverse = True):
    #print(playerStatLink[i])
    del playerStatLink[i]
#print(playerStatLink)

N = len(playerStatLink)
for link in playerStatLink[0:N]:
    
    players = requests.get(link, headers = headers)
    players.raise_for_status()
    ds = BeautifulSoup(players.text, "html.parser")
    stats = ds.select("td[class='fw-bold clr-gray-01 Table__TD']")
    columns = ds.select("th[class='Table__TH']")
    
    for stat in stats[1:19]:
        playerStat.append(stat.text.strip())
    if noData:
        playerStat.extend([0]*18)
    for column in columns[2:20]:
        if column not in statTitle:
            statTitle.append(column.text.strip())
    firstNames = ds.select("span[class='truncate min-w-0 fw-light']")
    lastNames = ds.select("span[class='truncate min-w-0']")
    for name in firstNames:
        if name not in playerFirstName:
            playerFirstName.append(name.text.strip())
    for name in lastNames:
        if name not in playerLastName:
            playerLastName.append(name.text.strip()) 
    #zips = zip(playerFirstName, playerStat)
    #print(zips)
for i in range(len(playerFirstName)):
    playerName.append(playerFirstName[i] +" " + playerLastName[i])
    
statTitle = statTitle[:18]

stats = np.array(playerStat).reshape(N,len(statTitle))
#print(stats)
playerCareerStat = pd.DataFrame(stats, index = playerName, columns = statTitle)
pd.DataFrame.to_csv(playerCareerStat,"playerStat.csv")