import pandas as pd

# Load the original CSV file
input_file = 'data/testrdataskipper.csv'  # Your input CSV file
output_file = 'data/plackett_luce_input.csv'  # Your output CSV file

# Read the data
df = pd.read_csv(input_file)

# Ensure data is sorted by 'race' and then 'ranking' within each race
df = df.sort_values(by=['race', 'ranking'])

# Group by race and aggregate the sorted competitor IDs for each race
pl_data = df.groupby('race')['id'].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Rename columns for clarity, if needed
pl_data.columns = ['race', 'competitor_order']

# Save to a new CSV file in Plackett-Luce format
pl_data.to_csv(output_file, index=False)

print(f"Data has been transformed and saved to {output_file}")