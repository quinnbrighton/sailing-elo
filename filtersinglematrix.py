# Open the CSV file and read it row by row
with open("data/testrdata.csv", 'r') as file:
    lines = file.readlines()

for i in range(0,10):
    # Create a list of all the valid IDs (added if not first or last)
    valid_ids = set()

    # First pass: Identify IDs that appear in middle positions (not first or last)
    for line in lines:
        row = line.strip().split(',')
        
        # Get the first and last ID in the row
        first_id = row[0]
        last_id = row[-1]
        
        # Add all IDs from the middle positions to the valid_ids set
        for id_ in row[0:]:
            valid_ids.add(id_)

    # Second pass: Remove only the ID numbers of the elements not in the set from the row
    filtered_lines = []

    for line in lines:
        row = line.strip().split(',')
        
        # Filter out IDs that are not in the valid_ids set
        filtered_row = [id_ for id_ in row if id_ in valid_ids]
        
        # Only add rows with remaining valid IDs
        if filtered_row:
            filtered_lines.append(','.join(filtered_row))

# Save the filtered data to a new file
with open("filtered_race_results.csv", 'w') as output_file:
    output_file.write("\n".join(filtered_lines))

print("Filtered data has been saved to 'filtered_race_results.csv'.")