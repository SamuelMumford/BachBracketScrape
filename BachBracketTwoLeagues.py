# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 23:45:56 2020

@author: Sam
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import numpy as np
import matplotlib.pyplot as plt
import infoSet

def getInfo(bs, teams):
    names = [None]*teams
    scores = [None]*teams
    scoreList = bs.findAll("div", {"class": "score-flex-box score-flex-text"})
    for i in range(0, teams):
        names[i] = scoreList[3*i].h2.get_text()
        scores[i] = scoreList[3*i + 2].h2.get_text()
    return names, scores


LOGIN_TIME = 3
SLEEP_SECONDS = 1
teams = 14
emailAd = infoSet.USERNAME
password = infoSet.PASSWORD
password = password + '\n'

driver = webdriver.Chrome()

print("logging in")
driver.get("https://bachelor.bachbracket.com/sign_in")
email = driver.find_element_by_id('session_email')
email.send_keys(emailAd)
pw = driver.find_element_by_id('session_password')
pw.send_keys(password)
time.sleep(LOGIN_TIME)

ad1 = "https://bachelor.bachbracket.com/leagues/" + str(infoSet.PAS_LEAGUEID) + "/scoreboard"
driver.get(ad1)
time.sleep(SLEEP_SECONDS)
print("Get PickAndStick")
content = driver.page_source
bs = BeautifulSoup(content, features="html.parser")
namesPAS, scoresPAS = getInfo(bs, teams)

ad2 = "https://bachelor.bachbracket.com/leagues/" + str(infoSet.W2W_LEAGUEID) + "/scoreboard"
driver.get(ad2)
time.sleep(SLEEP_SECONDS)
print("Get WeekToWeek")
content = driver.page_source
bs2 = BeautifulSoup(content, features="html.parser")
#print(bs2)
namesW2W, scoresW2W = getInfo(bs2, teams)

driver.quit()

FinalNames = [None]*teams
FinalScores = [None]*teams

for i in range(0, teams):
    FinalNames[i] = namesW2W[i]
    FinalScores[i] = int(scoresW2W[i]) + int(scoresPAS[namesPAS.index(namesW2W[i])])

SortedScores = sorted(FinalScores, reverse = True)
SortedNames = [n for _,n in sorted(zip(FinalScores,FinalNames), reverse=True)]
SortedW2W = [None]*teams
SortedPAS = [None]*teams
for i in range(0, teams):
    SortedW2W[i] = int(scoresW2W[namesW2W.index(SortedNames[i])])
    SortedPAS[i] = int(scoresPAS[namesPAS.index(SortedNames[i])])
#
export = np.vstack((SortedScores, SortedNames, SortedW2W, SortedPAS)).T
print()
print()
print('Total Score, Name, Week to Week, Pick and Stick')
print(export)
import csv

with open('testFile.txt', 'w', newline='\n') as myfile:
    wr = csv.writer(myfile, delimiter='\t')
    wr.writerow(["Name", "Total", "Week 2 Week", "Pick/Stick"])
    wr.writerows(export)
    
CutOut = 1
teams = teams - CutOut
SortedNames = SortedNames[0:teams]
SortedScores = SortedScores[0:teams]
SortedW2W = SortedW2W[0:teams]

index = 1.5*np.arange(teams)
bar_width = 0.35
opacity = 0.8

rects1 = plt.barh(index, SortedScores, bar_width,
alpha=opacity,
color='b',
label='Total Scores')

rects2 = plt.barh(index + bar_width, SortedW2W, bar_width,
alpha=opacity,
color='g',
label='Week To Week')

plt.xlim(min(SortedW2W), max(SortedScores))

plt.xlabel('Score')
plt.ylabel('Names')
plt.yticks(index + bar_width, SortedNames)
plt.legend(loc = 1)

plt.tight_layout()
plt.savefig('scores.png')
plt.show()