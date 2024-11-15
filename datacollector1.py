## Find all regattas -> put them in an array
## For each regatta take the results and export them into the SQL database
## Each regatta should have a week number on it -> alphabetical works for sorting

URL = "https://scores.collegesailing.org/"
regatta_info2 = []
import requests
import csv
from bs4 import BeautifulSoup

# years = ["f24/"]
# adds 08 and 09 -> starts with 0
years = ["f08/", "s09/", "f09/"]
for i in range(10,25):
    years.append("s" + str(i) + "/")
    years.append("f" + str(i) + "/")
    
final_array2 = []
for year in years[::-1]:
    print(years)
    # Make an HTTP GET request to fetch the page content for the given year
    page = requests.get(URL + year)

    soup = BeautifulSoup(page.content, "html.parser")

    # Locate and extract all regattas listed in the "season-summary" class section
    all_regattas = BeautifulSoup(str(soup.find_all(class_="season-summary")), 'html.parser')
    
    final_array = []
    # Loop over the HTML elements to extract and store each regatta's textual information
    for regatta2 in all_regattas:
        for regatta in regatta2:
            for regatta3 in regatta:
                try: 
                    #print(regatta3.text)
                    # If "Week" appears in the text, assume it's a weekly marker and add it to the list
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
    
    # Loop through links in the season summary section to get regatta names and corresponding URLs
    for link in all_regattas.find_all('a'):
        #print(link.get('href'))
        regatta_dict[link.text] = link.get('href')
        
    # Debugging print to show regatta dictionary for each year
    print(regatta_dict)
    lastblank = ""
    # Loop over each regatta's name in the dictionary of URLs
    for value in regatta_dict.keys():
        index = final_array.index(value)
        print(final_array[index])
        if("week" in final_array[index-1].lower()):
            lastblank = final_array[index-1]
        # Append the week, regatta URL, details from final_array, and year to final_array2
        final_array2.append([lastblank]+[regatta_dict[value]] + final_array[index:index+6]+[year])

# Sort the final list of regattas by alphabetical order of the week information for each regatta
final_array2.sort(key=lambda x: x[6])

with open('all-regattainfo.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    race_writer.writerows(final_array2)
