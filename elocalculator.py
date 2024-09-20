import csv

def update_from_dict(file_path):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                args = list(row)
                elo_dict[args[1]] = float(args[0])

    # Replace 'test.csv' with the actual path to your CSV file
elo_dict = {}
update_from_dict('dict.csv')
scorelist = []

for _ in range(0,50):
    def update_elo(result):
        sailor_array = []
        elo_array = []
        for i in range(6,len(result)):
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
                if sailor not in elo_dict:
                    elo_dict[sailor] = 1000
        
        for r in range(len(sailor_array)):
            elo_array.append([])
            for sailor in sailor_array[r]:
                try:
                    elo_array[r].append([sailor, elo_dict[sailor]])
                except: 
                    elo_array[r].append([sailor, 1000])
        #print(elo_array)
        if result[4] not in ["shields", "2023-mcmillan-cup", "2018-great-lakes-intercollegiate-offshore", "pine", "kennedy-cup", "2022-pine","2022-mcmillan-cup", "2023-pine", "2022-kennedy-cup", "2021-kennedy-cup", "2024-pine", "mcsa-sloop"]:
            new_position_elos = knockout_update(elo_array)
            #print(new_position_elos)
            update_dict(new_position_elos, elo_array)

    def knockout_update(elo_array):
        position_elos = []
        for r in range(len(elo_array)):
            if(len(elo_array[r]) >= 2):
                position_elos.append(0.5*elo_array[r][0][1] + 0.5*elo_array[r][1][1])
            else:
                position_elos.append(elo_array[r][0][1])
        new_elos = []
        for _ in range(len(position_elos)):
            new_elos.append(0)
        return update_position_elos(position_elos, new_elos)

    def update_position_elos(position_elos, new_elos):
        K = 1
        if(position_elos == []):
            return position_elos
        for i in range(len(position_elos) - 1):
            expected_score = 1 / (1 + 10**((position_elos[i] - position_elos[-1])/100))
            scorelist.append(expected_score)
            new_elos[i] += K * expected_score
            new_elos[-1] -= K * expected_score
        
        return update_position_elos(position_elos[0:-1], new_elos[0:-1]) + [new_elos[-1]]

    def update_dict(positions, elo_array):
        global elo_dict
        for index in range(len(elo_array)):
            for sailor in elo_array[index]: 
                elo = elo_dict[sailor[0]]
                elo_dict[sailor[0]] = positions[index] + elo
            

        
        
        
    def process_csv_file(file_path):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                update_elo(list(row))
            # Process each row here

    
    process_csv_file('18to24races.csv')

    dict_list = []
    for key in elo_dict.keys():
        try: 
            dict_list.append([elo_dict[key], key])
        except: 
            print(elo_dict[key])
    dict_list.sort(key = lambda x: x[0])

    #print(dict_list)


    with open('dict.csv', mode="w") as racefile: 
        race_writer = csv.writer(racefile)
        race_writer.writerows(dict_list)
