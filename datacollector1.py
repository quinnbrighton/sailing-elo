## Find all regattas -> put them in an array
## For each regatta take the results and export them into the SQL database
## Each regatta should have a week number on it -> alphabetical works for sorting

URL = "https://scores.collegesailing.org/"
regatta_info2 = []
import requests
import csv
from bs4 import BeautifulSoup
years = ["f08/", "s09/", "f09/"]
#"f18/", "f19/", "f21/", "f22/", "f23/","f24/"
#"f08/", "s09/", "f09/","s09/", "f09/","s09/", "f09/","s09/", "f09/", "s22/","f22/","s23/","f23/","s24/",

for i in range(10,25):
    years.append("s" + str(i) + "/")
    years.append("f" + str(i) + "/")
final_array2 = []
for year in years[::-1]:
    print(years)
    page = requests.get(URL + year)

    soup = BeautifulSoup(page.content, "html.parser")

    all_regattas = BeautifulSoup(str(soup.find_all(class_="season-summary")), 'html.parser')
    final_array = []
    for regatta2 in all_regattas:
        for regatta in regatta2:
            for regatta3 in regatta:
                try: 
                    #print(regatta3.text)
                    if("Week" in regatta3): 
                        #print(regatta3)
                        final_array.append(regatta3.text)
                    else: 
                        for regatta4 in regatta3: 
                            final_array.append(regatta4.text)
                except: 
                    print("no text")

    #final_array2.append(final_array)
    regatta_result_set = []
    regatta_dict = {}
    for link in all_regattas.find_all('a'):
        #print(link.get('href'))
        regatta_dict[link.text] = link.get('href')
    
    print(regatta_dict)
    lastblank = ""
    for value in regatta_dict.keys():
        index = final_array.index(value)
        print(final_array[index])
        if("week" in final_array[index-1].lower()):
            lastblank = final_array[index-1]
        final_array2.append([lastblank]+[regatta_dict[value]] + final_array[index:index+7])

    '''
    for regatta[0] in regatta_result_set:
        page = requests.get(URL + year + regatta[0])
        sailor_soup = BeautifulSoup(page.content, "html.parser")
        regatta_info = sailor_soup.find_all(class_="page-info-value")
        print(regatta[0] + " is a " + regatta_info[2].text)
        print(regatta_info)
        regatta_info2.append([year, regatta, regatta_info[0].text, regatta_info[1].text, regatta_info[2].text, regatta_info[3].text, regatta_info[4].text, regatta[0]])
'''
final_array2.sort(key=lambda x: x[6])

with open('all-regattainfo.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    race_writer.writerows(final_array2)

