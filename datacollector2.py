## Find all regattas -> put them in an array
## For each regatta take the results and export them into the SQL database
## Each regatta should have a week number on it -> alphabetical works for sorting

URL = "https://scores.collegesailing.org/"
regatta_array = []
regatta_array2 = []
import requests
import csv
from bs4 import BeautifulSoup


with open("regattas23-24.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        regatta_array.append(row)

#print(regatta_array)

for row in regatta_array:
    if(row[4] == 'Showcase Regatta' or row[4] == 'Cross Regional Regatta'):
        if("FJ" in row[5] or "420" in row[5]):
            if("Combined" in row[6]):
                regatta_array2.append([row[0], row[1], 1, True])
            elif("1" in row[6]): 
                regatta_array2.append([row[0], row[1], 1, False])
            elif("2" in row[6]):
                regatta_array2.append([row[0], row[1], 2, False])
            elif("3" in row[6]):
                regatta_array2.append([row[0], row[1], 2, False])
            else: 
                print(row)

with open('topregattas.csv', mode="w") as racefile: 
        race_writer = csv.writer(racefile)
        race_writer.writerows(regatta_array2)