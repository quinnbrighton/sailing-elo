import pandas as pd

def reformat_race_data(input_csv, output_csv):
    # Read the data from the input CSV
    df = pd.read_csv(input_csv)
    
    # Define a helper function to compute the new raceid
    def calculate_raceid(year_str, season, week):
        # Extract the year from the shortened string (e.g., "f10" -> 2010, "s24" -> 2024)
        year = int(year_str[1:3])  # Convert "f10" to 2010, "s24" to 2024
        
        # Initialize raceid with the year * 100
        raceid = year * 100
        
        # Check the season: add 50 if it's Fall (f), otherwise it's Spring (s)
        if year_str[0] == "f":  # Fall season
            raceid += 50
        
        # Add the week number extracted from the "Week X" format
        week_number = int(week.split()[-1])  # Extract the number from "Week 1", "Week 2", etc.
        raceid += week_number
        
        return raceid
    
    # Apply the function to compute the new raceid
    df['raceid'] = df.apply(lambda row: calculate_raceid(row['year'], row['year'], row['week']), axis=1)
    
    # Write the updated dataframe back to a new CSV
    df.to_csv(output_csv, index=False)

# Example usage:
input_csv = 'data/10-24racedata.csv'  # Path to your input CSV

# Call the function to reformat the race data and save it to the output CSV
reformat_race_data(input_csv, input_csv)