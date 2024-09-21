import csv

racedata = []
predictiondata = [['position', 'skipper', 'crew', 'season', 'venue', 'type', 'date', 'division', 'combined', 'regatta', 'race', 'entries']]
with open("data/testracedata.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        racedata.append(row)

#15,f23/,Southern Cal,2,False,2024-rose-bowl,7,14,"[""Peter Joslin '26"", ""Michaela O'Brien '24""]","[""Piper Holthus '25"", ""Poshu Ng '27""]","[""Bradley Whiteway '26"", ""Mia Quinlan '24""]","[""Reed McAllister '27"", ""Katherine Mason '27""]","[""Tiare Sierra '25"", ""Morgan Contrino '24""]","[""Daren Sathasivam '25"", ""Aidan Araoz '25""]","[""Jack Roman '26"", ""Addyson Fisher '27""]","[""Hudson Mayfield '27"", ""Jan Matteo Bassi '27""]","[""Max Kleha '25"", ""Brooke Bertrand '25""]","[""Garrison Guzzeau '25"", ""Anna Kovacs '25""]","[""Samuel Groom '24"", ""Daniel Gates '26""]","[""Ryan Tuttle '27"", ""Sadie Creemer '25""]","[""Bradley Whiteway '26"", ""Mia Quinlan '24""]","[""Brooke Davi '25"", ""James Unger '27""]"
#16,f23/,Southern Cal,2,False,2024-rose-bowl,8,15,"[""Bradley Whiteway '26"", ""Mia Quinlan '24""]","[""Connor Bennett '26"", ""Samantha Hemans '27""]","[""Jack Roman '26"", ""Addyson Fisher '27""]","[""Peter Joslin '26"", ""Michaela O'Brien '24""]","[""Piper Holthus '25"", ""Poshu Ng '27""]","[""Reed McAllister '27"", ""Katherine Mason '27""]","[""Tiare Sierra '25"", ""Morgan Contrino '24""]","[""Max Kleha '25"", ""Brooke Bertrand '25""]","[""Hudson Mayfield '27"", ""Jan Matteo Bassi '27""]","[""Brooke Davi '25"", ""James Unger '27""]","[""Bradley Whiteway '26"", ""Mia Quinlan '24""]","[""Daren Sathasivam '25"", ""Aidan Araoz '25""]","[""Samuel Groom '24"", ""Daniel Gates '26""]","[""Ryan Tuttle '27"", ""Sadie Creemer '25""]","[""Garrison Guzzeau '25"", ""Anna Kovacs '25""]"
#17,s22/,Charleston,1,False,south-collegiate-offshore,1,2,"[""Aidan naughton '22"", ""Parker Colantuono '22"", ""Tyler Miller '23"", ""Max Hooker '22"", ""AJ Kozaritz '23"", ""Clare Laroche '23"", ""Elizabeth Taylor '24"", ""Iain Jaeger '23""]","[""Wyatt Dennis '23"", ""Joe Serpa '24"", ""Zachary Beyer '25"", ""Gordon Fream '25"", ""Brendan Doyle '22"", ""Ryan O'Connor '23"", ""Samuel Stephens '25"", ""Christiana Scheibner '23""]"
#18,s22/,Charleston,1,False,south-collegiate-offshore,2,2,"[""Aidan naughton '22"", ""Parker Colantuono '22"", ""Tyler Miller '23"", ""Max Hooker '22"", ""AJ Kozaritz '23"", ""Clare Laroche '23"", ""Elizabeth Taylor '24"", ""Iain Jaeger '23""]","[""Wyatt Dennis '23"", ""Joe Serpa '24"", ""Zachary Beyer '25"", ""Gordon Fream '25"", ""Brendan Doyle '22"", ""Ryan O'Connor '23"", ""Samuel Stephens '25"", ""Christiana Scheibner '23""]"

sailor_dict = {}
venue_dict = {}
for row in racedata[1:]: 
    place = 1
    for sailors in row[10:]:
        sailors = eval(sailors)
        try: 
            predictiondata.append([place, sailors[0], sailors[1]] + row[1:10])
            #predictiondata.append([place, sailors[0], sailors[1], row[1], row[2], row[4], row[5], row[6]])
            place +=1
            sailor_dict[sailors[0]] = "Skipper"
            sailor_dict[sailors[1]] = "Crew"
            venue_dict[row[2]] = "Fun"
        except: 
            print(sailors)


sailor_array = [["name", "position", "year"]]
for key in sailor_dict.keys():
    sailor_array.append([key[:-4], sailor_dict[key], key[-2:]])

venue_array = [["venue", "more"]]
for key in venue_dict.keys():
    venue_array.append([key, venue_dict[key]])

with open("data/races.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(predictiondata)

with open("data/sailors.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(sailor_array)

with open("data/venues.csv", 'w') as racefile:
    race_writer = csv.writer(racefile)
    race_writer.writerows(venue_array)