import pandas as pd

# Load the CSV data
df = pd.read_csv('data/skippers.csv')

# Calculate the new rating
df['Rating'] = (df['Adjusted Estimate'] * 2000) - (df['Std. Error'] * 3000)

# Sort the DataFrame by the new rating (descending)
df = df.sort_values(by='Rating', ascending=False)

# Reset the ID to be sequential
df['id'] = range(1, len(df) + 1)

# Save the updated DataFrame back to CSV
df.to_csv('data/skippers.csv', index=False)
