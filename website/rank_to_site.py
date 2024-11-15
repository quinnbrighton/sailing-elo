import csv

def create_name_to_website_csv(input_file, output_file):
    # Read the names from the input CSV
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        names = [row['name'] for row in reader]

    # Create the name-to-website CSV
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name', 'url'])  # Write the header

        # Generate URLs and write them to the file
        base_url = "https://example.com/sailor/"  # Base URL to be customized
        for name in names:
            # Convert name to a URL-friendly version (replace spaces with hyphens, lowercase)
            name_slug = name.lower().replace(' ', '-')
            writer.writerow([name, base_url + name_slug])

# Usage
create_name_to_website_csv('data/skipperrank.csv', 'website/name_to_website.csv')