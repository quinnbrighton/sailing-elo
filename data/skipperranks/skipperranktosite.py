import pandas as pd

# Load the data from the CSV file
df = pd.read_csv('data/skipperranks/f24w10.csv')

# Step 1: Filter out rows where year is 21, 22, or 23 (class of 2024 and below)
df_filtered = df[~df['year'].isin([21, 22, 23])]

# Step 2: Calculate the median of the 'Estimate' column from the filtered data
median_estimate = df_filtered['Estimate'].median()

# Step 3: Subtract the median from the 'Estimate' column to adjust the estimates
df_filtered['Adjusted Estimate'] = df_filtered['Estimate'] - median_estimate


df_filtered['id'] = range(1, len(df_filtered) + 1)
# Step 4: Select the necessary columns: id, name, position, year, Adjusted Estimate, Std. Error, z value, Pr(>|z|)
df_result = df_filtered[['id', 'name', 'position', 'year', 'Adjusted Estimate', 'Std. Error', 'z value', 'Pr(>|z|)']]

# Step 5: Write the processed DataFrame back to the same CSV file
df_result.to_csv('website/skipperrank.csv', index=False)

# Optional: Print the result to verify
print(df_result)