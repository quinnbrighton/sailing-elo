## Find all regattas -> put them in an array
## For each regatta take the results and export them into the SQL database
## Each regatta should have a week number on it -> alphabetical works for sorting

URL = "https://scores.collegesailing.org/"
regatta_array = []
regatta_array2 = []
import requests
import csv
from bs4 import BeautifulSoup


with open("all-regattainfo.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        regatta_array.append(row)

#print(regatta_array)
#sample

#Week 18,rose-bowl,Rose Bowl,Southern Cal,NOT ALLOWED  Interconference,2 Divisions,01/02/2016,Official,

for row in regatta_array:
    if("showcase" in row[4].lower() or "cross regional" in row[4].lower() or "national" in row[4].lower()):
        if("Team" not in row[5] and ("Official" in row[7] or "nevermind" in row[5])):
            if("Combined" in row[5]):
                regatta_array2.append([row[0], row[1], 1, True] + row[3:])
            elif("1" in row[5]): 
                regatta_array2.append([row[0], row[1], 1, False] + row[3:])
            elif("2" in row[5]):
                regatta_array2.append([row[0], row[1], 2, False] + row[3:])
            elif("3" in row[5]):
                regatta_array2.append([row[0], row[1], 2, False] + row[3:])
            elif("Singlehanded" in row[5]):
                None
                #print("singlehanded")
            else: 
                print(row)

with open('topregattas.csv', mode="w") as racefile: 
        race_writer = csv.writer(racefile)
        race_writer.writerows(regatta_array2)