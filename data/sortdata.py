import pandas as pd

file = "data/10-24racedata.csv"
# Load the CSV file into a DataFrame
data = pd.read_csv(file)

# Convert the 'Date' column to datetime format (adjust the format as needed)
data['date'] = pd.to_datetime(data['date'], format="%m/%d/%Y")

# Sort the data by the 'Date' column
sorted_data = data.sort_values(by="date")

# Save the sorted data to a new CSV file
sorted_data.to_csv(file, index=False)

# Display the first few rows of the sorted data
print(sorted_data.head())

