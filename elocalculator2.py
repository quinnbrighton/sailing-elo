import csv
import trueskill
import mpmath

def update_from_dict(file_path):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                args = list(row)
                elo_dict[args[1]] = eval(args[0])

    # Replace 'test.csv' with the actual path to your CSV file
elo_dict = {}
elo_summary = []
#update_from_dict('testdict.csv')
scorelist = []
new_sailors = []
env = trueskill.TrueSkill(mu=25.0, sigma=8.333333333333334, beta=4.166666666666667, tau=0.28333333333333334, draw_probability=0.0,backend='mpmath')
result_glob = []

for _ in range(0,1):
    def update_elo(result):
        global result_glob
        result_glob = result
        print(result[0])
        if result[0] != "raceid":
            sailor_array = []
            elo_array = []
            for i in range(7,len(result)):
                parts = eval(result[i])
                if(parts != []):
                    sailor_array.append(parts)
            #gets rid of first CSV row
            try:
                if(sailor_array[0] == 1):
                    sailor_array = []
            except:
                sailor_array = []
            for sailors in sailor_array: 
                for sailor in sailors: 
                    if "*" in sailor: 
                        sailor = sailor[:-2]
                    if sailor not in elo_dict:
                        elo_dict[sailor] = [env.create_rating(), "last regatta", 0]
            
            for r in range(len(sailor_array)):
                elo_array.append([])
                for sailor in sailor_array[r]:
                    if "*" in sailor: 
                        sailor = sailor[:-2]
                    if sailor not in new_sailors:
                        new_sailors.append(sailor)
                    if sailor.lower() != "no show":
                        elo_array[r].append([sailor, elo_dict[sailor][0]])
                while(len(elo_array[r]) < len(eval(result_glob[7]))):
                    elo_array[r].append(["fake", env.create_rating()])
                while(len(elo_array[r]) > len(eval(result_glob[7]))):
                    elo_array[r].pop()
            #print(elo_array)
            if(len(eval(result_glob[7])) > 0):
                update_rating(elo_array)

     

    def update_rating(elo_array):
        new_array = []
        ranking_array = [0]
        for teams in elo_array:
            new_dict = {}
            for team in teams:
                new_dict[team[0]] = team[1]                
            new_array.append(new_dict)
            ranking_array.append(ranking_array[-1] + 1)
        ranking_array = ranking_array[:-1]
        #print(new_array)
        if(len(ranking_array) > 1): 
            print(len(ranking_array))
            rated_groups = env.rate(new_array, ranks=ranking_array)
            update_dict(rated_groups)


    def update_dict(rated_groups):
        global elo_dict
        global elo_summary
        global new_sailors
        global result_glob
        for sailor_dict in rated_groups:
            for sailor in sailor_dict.keys():
                try:  
                    elo_dict[sailor][0] = sailor_dict[sailor]
                    elo_dict[sailor][1] = result_glob[4]
                    elo_dict[sailor][2] = result_glob[5]
                except:
                    print(sailor)
        for sailor in new_sailors: 
            elo_summary.append([sailor, env.expose(elo_dict[sailor][0]), elo_dict[sailor][0].mu, elo_dict[sailor][0].sigma, str(result_glob[0]), str(result_glob[4])])
        new_sailors = []

        
        
        
    def process_csv_file(file_path):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                update_elo(list(row))
            # Process each row here

    
    process_csv_file('topracedata.csv')

    dict_list = []
    for key in elo_dict.keys():
        dict_list.append([elo_dict[key], key])

    dict_list.sort(key = lambda x: x[0][0].mu - 3 * x[0][0].sigma)

    #print(dict_list)


    with open('testdict.csv', mode="w") as racefile: 
        race_writer = csv.writer(racefile)
        race_writer.writerows(dict_list)


    with open('testdict2.csv', mode="w") as racefile: 
            race_writer = csv.writer(racefile)
            race_writer.writerows(elo_summary)