import csv

racedata = []
predictiondata = []
with open("testracedata.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        racedata.append(row)

#2,f23/,1,False,2024-rose-bowl,2,16,"[""Peter Busch '26"", ""Sara Schumann '25""]","[""Noah Robitshek '25"", ""Benjamin Luu '26""]","[""Diego Escobar '25"", ""Emily Panarella '24""]","[""Peter Lobaugh '24"", ""Kristen Healy '24""]","[""Oliver Stokke '26"", ""Maggie Fleming '27""]","[""Daniel Unangst '24"", ""Charles Pohl '26""]","[""Marianna Shand '24"", ""Linnea Jackson '25""]","[""Lars Osell '24"", ""Annika VanderHorst '27""]","[""Madison Bashaw '24"", ""Rachel O'Neill '24""]","[""Nicholas Mueller '27"", ""Sam Jennings '27""]","[""Anna Groszkowski '26"", ""Laura Rhodes '24""]","[""Robert Bloomfield '26"", ""Claire Wiley '27""]","[""Luke Harris '27"", ""Ariana Gabier '24""]","[""Emily Avey '25"", ""Aidan Clark '24""]","[""Jake Weinstein '27"", ""Millie Rose Taub '26""]","[""Daniel Unangst '24"", ""Charles Pohl '26""]"
sailor_dict = {}
for row in racedata[1:]: 
    place = 1
    for sailors in row[7:]:
        sailors = eval(sailors)
        try: 
            predictiondata.append([place, sailors[0], sailors[1], row[1], row[2], row[4], row[5], row[6]])
            #predictiondata.append([place, sailors[0], sailors[1], row[1], row[2], row[4], row[5], row[6]])
            place +=1
            sailor_dict[sailors[0]] = "Skipper"
            sailor_dict[sailors[1]] = "Crew"
        except: 
            print(sailors)


sailor_array = [["name", "position", "year"]]
for key in sailor_dict.keys():
    sailor_array.append([key[:-4], sailor_dict[key], key[-2:]])

with open("data/races.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(predictiondata)

with open("data/sailors.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(sailor_array)