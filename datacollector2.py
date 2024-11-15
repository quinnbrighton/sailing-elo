URL = "https://scores.collegesailing.org/"
elo_dict = {}
failed = []
import concurrent.futures
import requests
import csv
from bs4 import BeautifulSoup
matchup_count = 0

def is_first_char_integer(string):
    """
    Checks if the first character in the provided string is an integer.
    
    Args:
        string (str): The string to be evaluated.
    
    Returns:
        bool: True if the first character is an integer, False otherwise.
    
    Notes:
        - If the input string is empty, this function will return False.
        - If the first character is not a valid integer, a ValueError will be caught, and False will be returned.
    """  
    if not string:
        return False  # Empty strings are not considered integers
    try:
        int(string[0])
        return True
    except ValueError:
        return False

def get_sailor(sailor_set, params):
    """
    Searches for and returns a list of sailors from a set that meet all specified parameters.
    
    Args:
        sailor_set (list of list of str): List containing groups of sailors, where each group is a list of sailor details.
        params (str): Multi-line string of parameters, each line representing a different criterion to match.
    
    Returns:
        list of str: The first group of sailors that meet all the specified parameters, or ["FAILURE"] if no match is found.
    
    Notes:
        - Each sailor group must match every line of `params` for it to be returned.
        - Parameters are checked line by line; if any parameter is not found in a sailor group, the group is skipped.
    """
    #print(sailor_set)
    for sailors in sailor_set:
        returnval = True
        for param in params.splitlines():
            #print(param)
            if not any(param in s for s in sailors):
                returnval = False
        if(returnval):
            return sailors

    return ["FAILURE"]

def convert_race_data(data):
    """
    Adds default race data '1-100' if a name does not have associated race data.
    
    Args:
        data (list): The list containing names and race data.
    
    Returns:
        list: A new list with '1-100' added where race data is missing.
    """
    for i, element in enumerate(data):
        if "reserves" in element.lower():
            data = data[:i]  # Truncate and return the list up to and including the 'reserves' element
            
    updated_data = []
    i = 0
    while i < len(data):
        if i + 1 < len(data) and is_first_char_integer(data[i + 1]):
            # If the next item is race data, add both to the updated data
            updated_data.extend([data[i], data[i + 1]])
            i += 2
        else:
            # If there is no race data, add the name and '1-100'
            updated_data.extend([data[i], '1-100'])
            i += 1
    
    left = []
    right = []

    # Iterate over the list in chunks of four
    for i in range(0, len(updated_data), 4):
        # Collect the first and second elements (if they exist) into 'left'
        if i < len(updated_data):
            left.append(updated_data[i])
        if i + 1 < len(updated_data):
            left.append(updated_data[i + 1])
        # Collect the third and fourth elements (if they exist) into 'right'
        if i + 2 < len(updated_data):
            right.append(updated_data[i + 2])
        if i + 3 < len(updated_data):
            right.append(updated_data[i + 3])

    # Combine the 'left' and 'right' lists
    return left + right


def get_sailors(divisions, div, race, names):
    """
    Extracts the list of sailors for a specific division and race from a list of names.

    Args:
        divisions (int): Total number of divisions in the regatta.
        div (int): Current division (1, 2, or 3).
        race (int): Race number within the division.
        names (list of str): List of names and race data of sailors.
    
    Returns:
        list of str: A list of sailors who competed in the specified race and division, or an empty list if no match is found.
    
    Notes:
        - Handles variable index ranges for division starting points (e.g., 'A', 'B', 'C').
        - Sailors may have race assignments in the format '1-6,9-10', allowing flexibility for race grouping.
        - Adjusts entries if they include indicators such as '*' or 'reserve'.
    """
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
    namelist = convert_race_data(namelist)
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
        if('reserve' in element.lower() or 'no show' in element.lower()):
            #print(element.lower())
            return new_namelist
        if(not is_first_char_integer(element) and index == len(namelist) - 1):
            new_namelist.append(namelist[index])

    if(len(new_namelist) != 2):
        #print(names)
        #print(regatta)
        '''print(new_namelist)
        print(namelist)
        print(div)
        print(race)'''
        return []
    
    return new_namelist

                
def convert_race(results, divisions, combined, race_count):
    """
    Reorganizes race results based on whether divisions are combined or separate.
    
    Args:
        results (list of lists): Raw race results data, where each entry contains team, race number, division, place, and sailor names.
        divisions (int): Total number of divisions in the regatta.
        combined (bool): Whether the divisions are combined into one division.
        race_count (int): Number of races within each division.

    Returns:
        list of lists: A structured list with race results separated by division and race number.
    
    Notes:
        - Creates a multi-dimensional list to store race results per division and per race.
        - When `combined` is True, results are stored under a single division, otherwise by each division.
    """
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
    """
    Converts a place value from string to integer, assigning a default value if conversion fails.
    
    Args:
        string_val (str): The place value as a string.
        races (int): Total number of races in the regatta, used as a default place if conversion fails.
    
    Returns:
        int: The converted integer place, or `races + 1` if conversion fails.
    
    Notes:
        - If `string_val` cannot be converted to an integer, it assumes the place is higher than all participants and returns `races + 1`.
    """
    try:
        return int(string_val)
    except: 
        return races+1


def scrape_regatta_data(inputyear, regatta_result_set):
    race_id = 1
    #index of school names in web-scraped list of sailors
    sailor_index = []
    race_data1 = []

    #all-regattainfo structure
    #Week 18,rose-bowl,Rose Bowl,Southern Cal,NOT ALLOWED  Interconference,2 Divisions,01/02/2016,Official,

    #print(regatta_result_set)

    for regatta_data in regatta_result_set:
        #print(regatta_data)
        year = regatta_data[8]
        regatta = regatta_data[1]
        week = regatta_data[0]
        #print(regatta)
        if("match" not in regatta_data[5].lower() and "team" not in regatta_data[5].lower() and "single" not in regatta_data[5].lower() and (year == "f" + str(inputyear) + "/" or year == "s" + str(inputyear) + "/")):
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
            #print(sailor_set)
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

            #print(regatta)
            #print("Divisions: " + str(divisions))
            #print("Races: " + str(race_number))
            #print(str(combined))
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
                failed.append(year + str(regatta) + "failed 1")

           #try:
            for division in range(len(results)):
                racenum = 1
                for result in results[division]: 
                    cur_race = []
                    #result.sort(key = lambda x: x[0])
                    for race in result:
                        if(len(race[1]) != 0 and race[0] != "BKD" and race[0] != "DNS"):
                            cur_race.append([race[0], race[1]])
                    try:
                        new_race = []
                        for race in cur_race: 
                            if(is_first_char_integer(race[0])):
                                new_race.append([int(race[0]), race[1]])
                            else: 
                                new_race.append([len(cur_race)+1, race[1]])
                        new_race.sort(key= lambda x:x[0])
                        #print(new_race)
                        cur_race = [race_id, year, week, regatta_data[3],regatta_data[4],regatta_data[6], division + 1, combined, regatta, racenum, len(cur_race)] + [race[1] for race in new_race]

                        if(cur_race[9] > 0 and len(new_race) > 8):
                            race_data1.append(cur_race)
                            race_id = race_id + 1
                            racenum += 1
                    except: 
                        print(str(regatta) + " failed 2")
                        failed.append(str(regatta) + "failed 2" + year)

    return race_data1


race_data = [["raceid","year","week","venue","type","date", "division", "combined", "regatta","race","numsailors"]]
for i in range(36):
    race_data[0].append(i+1)

# Number of threads to run in parallel
num_threads = 20
regatta_result_set = []
with open("all-regattainfo.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        regatta_result_set.append(row)


#scrape_regatta_data(23, regatta_result_set)


# Use ThreadPoolExecutor to process each regatta in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit each regatta data to the thread pool for processing
    futures = [executor.submit(scrape_regatta_data, year, regatta_result_set) for year in range(10,25)]

    # Handle the results and exceptions from threads
    for future in concurrent.futures.as_completed(futures):
        try:
            # If there was an error in the thread, it will be raised here
            race_data += future.result()
        except Exception as e:
            print(f"Error processing regatta: {e}")


with open('data/10-24racedata.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    race_writer.writerows(race_data)

