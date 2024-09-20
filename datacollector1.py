## Find all regattas -> put them in an array
## For each regatta take the results and export them into the SQL database
## Each regatta should have a week number on it -> alphabetical works for sorting

URL = "https://scores.collegesailing.org/"
regatta_info2 = []
import requests
import csv
from bs4 import BeautifulSoup

#"f18/", "f19/", "f21/", "f22/", "f23/","f24/"
for year in ["s22/","f22/","s23/","f23/","s24/","f24/"]:
    page = requests.get(URL + year)

    soup = BeautifulSoup(page.content, "html.parser")

    all_regattas = BeautifulSoup(str(soup.find_all(class_="season-summary")), 'html.parser')

    regatta_result_set = []
    regatta_result_set2 = []
    for link in all_regattas.find_all('a'):
        #print(link.get('href'))
        regatta_result_set.insert(0,link.get('href'))
    
    for regatta in regatta_result_set:
        page = requests.get(URL + year + regatta)
        sailor_soup = BeautifulSoup(page.content, "html.parser")
        regatta_info = sailor_soup.find_all(class_="page-info-value")
        print(regatta + " is a " + regatta_info[2].text)
        regatta_info2.append([year, regatta, regatta_info[0].text, regatta_info[1].text, regatta_info[2].text, regatta_info[3].text, regatta_info[4].text])



with open('regattas23-24.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    race_writer.writerows(regatta_info2)

