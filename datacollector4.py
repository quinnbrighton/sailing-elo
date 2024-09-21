## Find all regattas -> put them in an array
## For each regatta take the results and export them into the SQL database
## Each regatta should have a week number on it -> alphabetical works for sorting

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

def get_sailor(sailor_set, team1, school1):
    for sailors in sailor_set:
        if any(team1 in s for s in sailors):
            if any(school1 in h for h in sailors):
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
    except: 
        namelist = names[start_index+2:]
    new_namelist = []
    if(len(namelist) == 2):
        return namelist
    else: 
        for index in range(len(namelist)):
            if(is_first_char_integer(namelist[index]) and index > 0):
                if("," in namelist[index] or "-" in namelist[index]):
                    allcommas = namelist[index].split(',')
                    for comma in allcommas: 
                        if("-" in comma):
                            twoints = comma.partition('-')
                            if(race in range(int(twoints[0]),int(twoints[2])+1)):
                                new_namelist.append(namelist[index-1])
                        try: 
                            if(race == int(comma)):
                                new_namelist.append(namelist[index-1])
                        except: 
                            comma = 1
                elif(race == int(namelist[index])):
                    new_namelist.append(namelist[index-1])
            elif(index > 0):
                if not is_first_char_integer(namelist[index-1]):
                    new_namelist.append(namelist[index-1])
            if('Reserves' in namelist[index]):
                return new_namelist
            if(not is_first_char_integer(namelist[index]) and index == len(namelist) - 1):
                new_namelist.append(namelist[index])
        if(len(new_namelist) != 2 and len(new_namelist) != 0 and False):
            print(names)
            print(regatta)
            print(new_namelist)
            print(namelist)
            print(div)
            print(race)

        return new_namelist
                
def convert_race(results, divisions, combined, race_count):
    #print(results)
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
        
    #print(new_results)
    return new_results

    ## race results structure -> team, race, division, result, sailors
    #results = convert_race(race_results, divisions, combined, race_number)

def convert_to_place(string_val,races):
    try:
        return int(string_val)
    except: 
        return races+1

def update_elo(race_result):
    race_result.sort(key = lambda x: x[0])
    for i in range(0, len(race_result)):
        for j in range(i+1, len(race_result)):
            elo_matchup(race_result[i][1], race_result[j][1])

    #print(race_result)


def elo_matchup(winners, losers):
    #print("winners" + str(winners))
    #print("losers" + str(losers)) 
    for winner in winners: 
        for loser in losers: 
            elo_match(winner, loser)

def elo_match(winner, loser):
    try: 
        if(" *" in winner):
            winner = winner[:-2]
        if(" *" in loser):
            loser = loser[:-2]
        winnerelo = elo_dict.get(winner[:-4])[-1]
        loserelo = elo_dict.get(loser[:-4])[-1]
        K = 5  # K-factor, adjust as needed
        expected_score_winner = 1 / (1 + 10**((loserelo - winnerelo) / 500))
        expected_score_loser = 1 - expected_score_winner
        elochange = K * (1-expected_score_winner)
        #elochange = abs((winnerelo-loserelo)/100)
        elo_dict[winner[:-4]][-1] = (winnerelo + elochange)
        elo_dict[loser[:-4]][-1] = (loserelo - elochange)
        #print(elochange)
        global matchup_count
        matchup_count = matchup_count + 1
    except: 
        print("elo failure")

def create_elo_dict(dict, sailors):
    for sailor in sailors:
        if "'2" in str(sailor) or "'1" in str(sailor): 
            if(" *" in str(sailor)):
                sailor = sailor[:-2]
                #print(sailor)
            #print(sailor)
            if(sailor[:-4] not in elo_dict):
                elo_dict[sailor[:-4]] = [[[1000, "regatta"]], 1000]

def get_sailors_from(school, elo_dict):
    score_table = []
    page = requests.get("https://scores.collegesailing.org/schools/" + school + "/f24/roster/")
    soup = BeautifulSoup(page.content, "html.parser")
    all_sailors = BeautifulSoup(str(soup.find_all(class_="sailor-name")), 'html.parser')
    print(all_sailors.text)
    all_sailors = all_sailors.text.split(", ")
    for sailor in all_sailors:
        print(sailor)
        if sailor in elo_dict:
            score_table.append([sailor, elo_dict[sailor]])
    print(score_table)

race_data = [["raceid", "year", "race", "division", "combined", "regatta","sailors"]]
for i in range(36):
    race_data[0].append(i+1)

#"f18/", "f19/", "f21/", "f22/", "f23/","f24/"
for year in ["f18/", "f19/", "f21/", "f22/", "f23/","f24/"]:
    page = requests.get(URL + year)

    soup = BeautifulSoup(page.content, "html.parser")

    all_regattas = BeautifulSoup(str(soup.find_all(class_="season-summary")), 'html.parser')

    regatta_result_set = []
    regatta_result_set2 = []
    for link in all_regattas.find_all('a'):
        #print(link.get('href'))
        regatta_result_set.insert(0,link.get('href'))
    
    #del regatta_result_set[2:]
    #regatta_result_set = ["mt-hope-bay-invite"]

    #index of school names in web-scraped list of sailors
    sailor_index = []
    for regatta in regatta_result_set:
        print(regatta)
        print(year)
        """ try: """
        regatta_set = []
        sailor_set = []
        #index of school names in web-scraped list of sailors
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
                team_set[team_index] = [team_set[team_index], sailors[index-1]]

        sailor_index.append(len(sailor_list)-1)
        sailors = sailor_soup.contents[1].get_text(separator="\n")
        sailor_list = sailors.splitlines()
        for i in range(0, len(team_set)):
            sailor_set.append(sailor_list[sailor_index[i]-1:sailor_index[i+1]-1])
        page = requests.get(URL + year + regatta + '/full-scores/')
        regatta_soup = BeautifulSoup(page.content, "html.parser")
        #race_soup = BeautifulSoup(page.content, "html.parser")
        content = regatta_soup.contents[1].get_text(separator="\n")
        content_list = content.splitlines()
        try: 
            index_of_tot = content_list.index("TOT")
        except: 
            failed.append("regatta isn't compatible (TOT failure): " + regatta + year)
            break
        race_number = int(content_list[index_of_tot - 1])
        temp = content_list.copy()
        for team in team_set:
            if(team[0] in content_list):
                content_index.append(content_list.index(team[0]))
                content_list[content_index[-1]] = "already used"
        content_list = temp

        divisions = 3
        try: 
            content_list.index("C") 
        except:
            divisions = 2
        try:
            content_list.index("B") 
        except:
            divisions = 1
        try: 
            content_list.index("A")
        except:
            divisions = 1
        try: 
            content_list.index("Combined") 
            combined = True
        except:
            combined = False

        if(divisions == 1):
            for index in content_index:
                regatta_results.append([content_list[index], content_list[index+1:index+race_number+2]])
        if(divisions == 2):
            for index in content_index:
                regatta_results.append([content_list[index], content_list[index-race_number-2:index-1],content_list[index+1:index+race_number+2]])
        if(divisions == 3):
            for index in content_index:
                regatta_results.append([content_list[index], content_list[index-race_number-2:index-1],content_list[index+1:index+race_number+2],
                content_list[index+race_number+3:index+2*race_number+4]])

        #Relevant data after this is done
        #print(sailor_set)
        print(regatta)
        print("Divisions: " + str(divisions))
        print("Races: " + str(race_number))
        print(str(combined))
        race_results = []

        try: 
            for team in range(len(team_set)):
                for race in range(race_number):
                    if(not combined):
                        for div in range(divisions):
                            race_results.append([regatta_results[team][0] + regatta_results[team][1][0], race+1, div+1, convert_to_place(regatta_results[team][div+1][race+1],race_number), get_sailors(divisions, div+1, race+1, get_sailor(sailor_set, regatta_results[team][0], regatta_results[team][1][0]))])
                    else: 
                        for div in range(divisions):
                            race_results.append([regatta_results[team][0] + regatta_results[team][1][0], race+1, 1, convert_to_place(regatta_results[team][div+1][race+1],race_number), get_sailors(divisions, div+1, race+1, get_sailor(sailor_set, regatta_results[team][0], regatta_results[team][1][0]))]) 
            ## race results structure -> team, race, division, result, sailors
            results = convert_race(race_results, divisions, combined, race_number)
        except: 
            print(str(regatta) + "failed 1")
            failed.append(str(regatta) + "failed 1" + year)

        try:
            create_elo_dict(elo_dict, sailor_list)
            for division in range(len(results)):
                racenum = 1
                for result in results[division]: 
                    cur_race = [race_id, year, division + 1, combined, regatta, racenum, len(result)]
                    result.sort(key = lambda x: x[0])
                    for race in result: 
                        cur_race.append(race[1])
                    race_data.append(cur_race)
                    race_id = race_id + 1
                    racenum += 1
                    #update_elo(result)

            for sailor in sailor_list:
                try: 
                    elo_dict[sailor[:-4]][0].append([elo_dict[sailor[:-4]][-1], regatta])
                except: 
                    None

        except: 
            print(str(regatta) + " failed 2")
            failed.append(str(regatta) + "failed 2" + year)

#print(elo_dict)
#print(elo_dict)
#ekeys = [key for key in elo_dict]
#ekeys.sort()
#print(ekeys)
#get_sailors_from("brown", elo_dict)

#sheet -> 25 columns, 50000 rows (one for each race)

#print(race_data)
with open('races.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    race_writer.writerows(race_data)

ekeys = [key for key in elo_dict]
#ekeys.sort()
#print(ekeys)
print("Sailor count: " + str(len(ekeys)))
print("Matchup count: " + str(matchup_count))
print(failed)