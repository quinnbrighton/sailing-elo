URL = "https://scores.collegesailing.org/"
elo_dict = {}
failed = []
import requests
import csv
from bs4 import BeautifulSoup
matchup_count = 0
race_id = 1

def is_first_char_integer(string):
  if not string:
    return False  # Empty strings are not considered integers
  try:
    int(string[0])
    return True
  except ValueError:
    return False

def get_sailor(sailor_set, params):
    #print(sailor_set)
    for sailors in sailor_set:
        returnval = True
        for param in params.splitlines():
            print(param)
            if not any(param in s for s in sailors):
                returnval = False
        if(returnval):
            return sailors

    return ["FAILURE"]

def get_sailors(divisions, div, race, names):
    start_index = 0
    try: 
        if(div == 1):
            start_index = names.index('A')
            if(divisions >= 2):
                end_index = names.index('B')
        elif(div == 2):
            start_index = names.index('B')
            if(divisions >= 3):
                end_index = names.index('C')
        else:
            start_index = names.index('C')
    except:
        start_index = 0
    try: 
        namelist = names[start_index+2:end_index]
        #print(namelist)
    except: 
        namelist = names[start_index+2:]
        #print(namelist)

    for i in range(len(namelist)):
        if("*" == namelist[i][-1]):
            namelist[i] = namelist[i][:-2]

    new_namelist = []
    #print(namelist)
    for index in range(len(namelist)):
        element = namelist[index]
        if(is_first_char_integer(element) and index > 0):
            allcommas = namelist[index].split(sep=',')
            for comma in allcommas: 
                if("-" in comma):
                    twoints = comma.split(sep='-')
                    #can delete next 3 lines once compiles
                    if(len(twoints) != 2): 
                        print([twoints, race, names])
                        break
                    if(race in range(int(twoints[0]),int(twoints[1])+1)):
                        new_namelist.append(namelist[index-1])
                else: 
                    if(race == int(comma)):
                        new_namelist.append(namelist[index-1])
        elif(index > 0):
            #if first char is a char (sailor name) + next index is not a number
            if not is_first_char_integer(namelist[index-1]):
                new_namelist.append(namelist[index-1])
        if('reserve' in element.lower()):
            return new_namelist
        if(not is_first_char_integer(element) and index == len(namelist) - 1):
            new_namelist.append(namelist[index])

    if(len(new_namelist) != 2):
        print(names)
        print(regatta)
        '''print(new_namelist)
        print(namelist)
        print(div)
        print(race)'''
        return []
    
    return new_namelist

                
def convert_race(results, divisions, combined, race_count):
    new_results = []
    if(not combined):
        for i in range(divisions):
            new_results.append([])
            for j in range(race_count):
                new_results[-1].append([])
        for element in results: 
            #print(element)
            new_results[element[2]-1][element[1]-1].append([element[3], element[4]])
            #print(new_results)
    else: 
        new_results.append([])
        for j in range(race_count):
            new_results[0].append([])
    
        for element in results: 
            #print(element)
            new_results[0][element[1]-1].append([element[3], element[4]])
        
    return new_results


def convert_to_place(string_val,races):
    try:
        return int(string_val)
    except: 
        return races+1

race_data = [["raceid", "year", "race", "division", "combined", "regatta", "sailors"]]
for i in range(36):
    race_data[0].append(i+1)


#index of school names in web-scraped list of sailors
sailor_index = []
regatta_result_set = []
#Week 18,rose-bowl,Rose Bowl,Southern Cal,NOT ALLOWED  Interconference,2 Divisions,01/02/2016,Official,

with open("all-regattainfo.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        regatta_result_set.append(row)

#print(regatta_result_set)

for regatta_data in regatta_result_set:
    #print(regatta_data)
    year = regatta_data[8]
    regatta = regatta_data[1]
    if("team" not in regatta_data[5].lower() and "single" not in regatta_data[5].lower() and "Official" == regatta_data[-2]
    and ("fundamental" in regatta_data[4].lower() or "conference" in regatta_data[4].lower() or "cross regional" in regatta_data[4].lower() or "national" in regatta_data[4].lower()) and ("23" in year or "24" in year)):
        print(regatta)
        print(year)
        regatta_set = []
        sailor_index = []
        team_set = []
        sailor_set = []
        regatta_results = []
        content_index = []
        school_set = []
        # parse every regatta
        page = requests.get(URL + year + regatta + '/sailors/')
        sailor_soup = BeautifulSoup(page.content, "html.parser")
        team = sailor_soup.find_all(class_="teamname")
        school = sailor_soup.find_all(class_="schoolname")
        sailors = sailor_soup.contents[1].get_text(separator="\n")
        sailor_list = sailors.splitlines()
        for schoolname in school: 
            school_set.append(schoolname.text)

        for teamname in team:
            team_set.append(teamname.text)
            sailor_index.append(sailor_list.index(teamname.text))
            sailor_list[sailor_index[-1]] = "removed"

        sailors = sailors.split("\n")
        
        for index in range(len(sailors)):
            if(sailors[index] in team_set):
                team_index = team_set.index(sailors[index])
                if(sailors[index] == sailors[index+1]):
                    #print(sailors[index-1:index+1])
                    team_set[team_index] = [sailors[index], sailors[index]]
                else: 
                    team_set[team_index] = [team_set[team_index], sailors[index-1]]
                

        sailor_index.append(len(sailor_list)-1)
        sailors = sailor_soup.contents[1].get_text(separator="\n")
        sailor_list = sailors.splitlines()
        for i in range(0, len(team_set)):
            sailor_set.append(sailor_list[sailor_index[i]-1:sailor_index[i+1]-1])
        print(sailor_set)
        #get full scores and store all data in content_list
        regatta_url = URL + year + regatta + '/full-scores/'
        print(regatta_url)
        page = requests.get(regatta_url)
        regatta_soup = BeautifulSoup(page.content, "html.parser")
        content = regatta_soup.contents[1].get_text(separator="\n")
        content_list = content.splitlines()

        #finds the number of races in a set
        try: 
            race_number = int(content_list[content_list.index("TOT") - 1])
        except: 
            failed.append("regatta isn't compatible (TOT failure): " + regatta + year)
            break

        #finds the index of every team name in the content_list
        temp = content_list.copy()
        for team in team_set:
            if(team[0] in content_list):
                content_index.append(content_list.index(team[0]))
                content_list[content_index[-1]] = "already used"
        content_list = temp

        combined = bool(regatta_data[5] == "Combined")
        if not combined:
            divisions = int(regatta_data[5][0])
        else:
            divisions = 1

        if(divisions == 1):
            for index in content_index:
                regatta_results.append([content_list[index], content_list[index+1:index+race_number+2]])
        if(divisions == 2):
            for index in content_index:
                regatta_results.append([content_list[index] + "\n" + content_list[index-race_number-3], content_list[index-race_number-2:index-1],content_list[index+1:index+race_number+2]])
        if(divisions == 3):
            for index in content_index:
                regatta_results.append([content_list[index] + "\n" + content_list[index-race_number-3], content_list[index-race_number-2:index-1],content_list[index+1:index+race_number+2],
                content_list[index+race_number+3:index+2*race_number+4]])

        print(regatta)
        print("Divisions: " + str(divisions))
        print("Races: " + str(race_number))
        print(str(combined))
        #print(regatta_results)
        #sample regatta_results: 
        # [['Eagles', ['A', '1', '8', '3', '3', '1', '9', '4', '2', '1', '1', '2', '2'], 
        # ['B', '9', '1', '14', '1', '8', '1', '6', '12', '1', '4', '1', '4'], 
        # ['C', '1', '1', '2', '3', '12', '1', '10', '6', '9', '7', '1', '3']], ... ]
        race_results = []

        try: 
            #print(team_set)
            for team in range(len(team_set)):
                for race in range(race_number):
                    if(not combined):
                        for div in range(divisions):
                            #race_results.append(["school name" + "division"], race number, division number, place of sailor in that race, sailors who competed for the team in that race)
                            race_results.append([regatta_results[team][0] + regatta_results[team][1][0], race+1, div+1, regatta_results[team][div+1][race+1], get_sailors(divisions, div+1, race+1, get_sailor(sailor_set, regatta_results[team][0] + "\n" + regatta_results[team][1][0]))])
                    else:
                        for div in range(divisions):
                            race_results.append([regatta_results[team][0] + regatta_results[team][1][0], race+1, 1, regatta_results[team][div+1][race+1], get_sailors(divisions, div+1, race+1, get_sailor(sailor_set, regatta_results[team][0] + "\n" + regatta_results[team][1][0]))]) 
            #print(race_results)
            ## race results structure -> team, race, division, result, sailors
            results = convert_race(race_results, divisions, combined, race_number)
            # results structure: 
            #[[[["14", ["Harry Stevenson '24", "Ryan Standaert '24", '1-6,9-10', "Emily DeLossa '24", '7-8,11']], 
            # ["7", ["Grant Adam '23", "Olivia MILLER '25", '1-6', "Ali Zaidi '24", '7-11']], 
            # ["11", ["Nicholas Leshaw '22", "Sarah Jane O’Connor '24"]], 
            # ["1", ["George Higham '23", "Jaqueline Frode '22", '1-6', "Izaiah Farr '23", '7-11']], 
            # ["10", ["Luke Hosek '24", "Ethan Snyder '25"]], 
            # ["6", ["Chase Reynolds '23", "Alden Sahi '25"]], 
            # ["8", ["Peter Cronin '22", "Olivia Lowthian '25"]], 
            # ["2", ["Connor Sheridan '22", "Harper McKerrow '23"]], 
            # ["3", ["Michael Pinto '23", "Jonathan Glander '24"]], 
            # ["5", ["Emma Snead '23", "Jin Johnson '24", '1-6', "Christina Mock '24", '7-11']], [12, ["Will Rudaz '22", '1-2,5-11', "Natalie Renehan '24", '1-2,5-11', "James Sullivan '25", '3-4', "Vincent (Vinny) Pallotto '23", '3-4']], [4, ["Miles Williams '24", "Anika Martz '22", '1-8,11', "Jonathan Riley '23", '9-10']], [9, ["Luke Quine '23", "Samuel Barrett '25"]], [13, ["Nick Ferrara '22", "Ryan Cloherty '22"]]],
        except: 
            print(str(regatta) + "failed 1")
            failed.append(str(regatta) + "failed 1" + year)

        try:
            for division in range(len(results)):
                racenum = 1
                for result in results[division]: 
                    cur_race = []
                    #result.sort(key = lambda x: x[0])
                    for race in result:
                        if(len(race[1]) != 0 and race[0] != "BKD" and race[0] != "DNS"):
                            cur_race.append([race[0], race[1]])
                    new_race = []
                    for race in cur_race: 
                        if(is_first_char_integer(race[0])):
                            new_race.append([int(race[0]), race[1]])
                        else: 
                            new_race.append([len(cur_race)+1, race[1]])
                    new_race.sort(key= lambda x:x[0])
                    #print(new_race)


                    cur_race = [race_id, year, regatta_data[3],regatta_data[4],regatta_data[6], division + 1, combined, regatta, racenum, len(cur_race)] + [race[1] for race in new_race]

                    if(cur_race[9] > 0 and len(new_race) > 8):
                        race_data.append(cur_race)
                        race_id = race_id + 1
                        racenum += 1

        except: 
            print(str(regatta) + " failed 2")
            failed.append(str(regatta) + "failed 2" + year)

with open('data/testracedata.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    race_writer.writerows(race_data)

print(failed)