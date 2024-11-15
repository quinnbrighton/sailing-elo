import csv

racedata = []
predictiondata = [['position', 'skipper', 'crew', 'season', 'venue', 'type', 'date', 'division', 'combined', 'regatta', 'race', 'entries']]
with open("data/10-24racedata.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        racedata.append(row)

#raceid,year,week,venue,type,date,division,combined,regatta,race,numsailors,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36
#1,s24/,Preweek 1,UC San Diego,Fundamental,01/27/2024,1,False,jeff-simon-open,1,11,"[""Luke Harris '27"", ""Ava Bergan '27""]","[""Davis Winsor '24"", ""Cara Loo '24""]","[""Robert Bloomfield '26"", ""Samuel Groom '24""]","[""Jan Matteo Bassi '27"", ""Jack Blackman '24""]","[""Jack Phibbs '27"", ""Annika Burns '27""]","[""Aidan Boylan '24"", ""Noah Lovelace '25""]","[""Camden Wacha '27"", ""Colin Wood '27""]","[""lucas kaemmerer '26"", ""Alexis Kovacevic '27""]","[""Ethan Lisle '25"", ""Nate Ingebritson '25""]","[""William Bailly '26"", ""Kyla Coubrough '24""]","[""Annika Altman '26"", ""Phoebe Liermann '27""]"
#2,s24/,Preweek 1,UC San Diego,Fundamental,01/27/2024,1,False,jeff-simon-open,2,11,"[""Luke Harris '27"", ""Ava Bergan '27""]","[""Davis Winsor '24"", ""Cara Loo '24""]","[""Jack Phibbs '27"", ""Annika Burns '27""]","[""Jan Matteo Bassi '27"", ""Jack Blackman '24""]","[""Robert Bloomfield '26"", ""Samuel Groom '24""]","[""Aidan Boylan '24"", ""Noah Lovelace '25""]","[""Ethan Lisle '25"", ""Nate Ingebritson '25""]","[""William Bailly '26"", ""Kyla Coubrough '24""]","[""Camden Wacha '27"", ""Colin Wood '27""]","[""lucas kaemmerer '26"", ""Alexis Kovacevic '27""]","[""Annika Altman '26"", ""Phoebe Liermann '27""]"
#3,s24/,Preweek 1,UC San Diego,Fundamental,01/27/2024,1,False,jeff-simon-open,3,11,"[""Luke Harris '27"", ""Ava Bergan '27""]","[""Davis Winsor '24"", ""Cara Loo '24""]","[""Robert Bloomfield '26"", ""Samuel Groom '24""]","[""Jan Matteo Bassi '27"", ""Jack Blackman '24""]","[""Aidan Boylan '24"", ""Noah Lovelace '25""]","[""Jack Phibbs '27"", ""Annika Burns '27""]","[""Ethan Lisle '25"", ""Madalyn Gordon '25""]","[""Camden Wacha '27"", ""Colin Wood '27""]","[""lucas kaemmerer '26"", ""Hazel Ross '27""]","[""William Bailly '26"", ""Kyla Coubrough '24""]","[""Annika Altman '26"", ""Phoebe Liermann '27""]"

enddate = 2500
margin = 400
skipper_dict = {}
crew_dict = {}
venue_dict = {}
for row in racedata[1:]: 
    if((int(row[0]) < enddate) and (int(row[0]) > (enddate - margin))):
        place = 1
        for sailors in row[11:]:
            if sailors != '':
                sailors = eval(sailors)
                try: 
                    predictiondata.append([place, sailors[0], sailors[1]] + row[1:11])
                    #predictiondata.append([place, sailors[0], sailors[1], row[1], row[2], row[4], row[5], row[6]])
                    place +=1
                    skipper_dict[sailors[0]] = "Skipper"
                    crew_dict[sailors[1]] = "Crew"
                    venue_dict[row[3]] = "Fun"
                except: 
                    print(sailors)

unique_dict1 = {}
reverse_dict = {}
skipper_array = [["id","name","position","year"]]

all_keys = [x for x in skipper_dict.keys()]
keynum = len(all_keys)
for index in range(0, keynum):
    unique_dict1[all_keys[index]] = index
    reverse_dict[index] = all_keys[index]

print(unique_dict1)

for index in range(1,len(predictiondata)):
    try:
        predictiondata[index][1] = unique_dict1[predictiondata[index][1]]
    except:
        a = 1

for index in range(0, keynum):
    key = all_keys[index][:-4]
    try: 
        e1 = unique_dict1[key]
    except: 
        e1 = unique_dict1[all_keys[index]]
    e2 = all_keys[index][:-4]
    e3 = skipper_dict[all_keys[index]]
    e4 = all_keys[index][-2:]
    skipper_array.append([e1, e2, e3, e4])
    
###
startindex = len(all_keys)
unique_dict2 = {}
reverse_dict = {}
crew_array = [["id","name","position","year"]]
all_keys = [x for x in crew_dict.keys()]
keynum = len(all_keys)
for index in range(0, keynum):
    unique_dict2[all_keys[index]] = index + startindex
    reverse_dict[index + startindex] = all_keys[index]

print(unique_dict2)

for index in range(1,len(predictiondata)):
    for index2 in range(2, len(predictiondata[index])):
        try:
            predictiondata[index][index2] = unique_dict2[predictiondata[index][index2]]
        except:
            a = 1

for index in range(0, keynum):
    key = all_keys[index][:-4]
    try: 
        e1 = unique_dict2[key]
    except: 
        e1 = unique_dict2[all_keys[index]]
    e2 = all_keys[index][:-4]
    e3 = crew_dict[all_keys[index]]
    e4 = all_keys[index][-2:]
    crew_array.append([e1, e2, e3, e4])

prediction_data = []
error = 0
for row in racedata[1:]:
    if((int(row[0]) < enddate) and (int(row[0]) > (enddate - margin))):
        prediction_data += [[]]
        for sailors in row[11:]:
            if sailors != '':
                sailors = eval(sailors)
                try: 
                    prediction_data[-1].append(unique_dict1[sailors[0]])
                except: 
                    print(sailors)
                    print(str(error))
                    error = error + 1


#print(prediction_data)
#print(all_keys)


venue_array = [["venue", "other"]]
for key in venue_dict.keys():
    venue_array.append([key, venue_dict[key]])



with open("data/races.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(predictiondata)

with open("data/skippers.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(skipper_array)
    
with open("data/testrdata.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(prediction_data)
    
with open("data/crews.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(crew_array)

with open("data/venues.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(venue_array)