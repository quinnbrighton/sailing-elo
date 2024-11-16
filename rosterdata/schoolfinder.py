import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL to scrape
url = "https://scores.collegesailing.org/schools/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all rows with school data (the <tr> tags)
rows = soup.find_all('tr', class_=['row0', 'row1'])

# Lists to hold the school names, image filenames, roster links, and school tokens
school_names = []
image_tokens = []
roster_links = []
school_tokens = []

# Loop through each row and extract the school name, image filename, roster link, and school token
for row in rows:
    # Find the image URL (inside <img> tag within class 'burgeecell')
    img_tag = row.find('img', src=True)
    if img_tag:
        # Get the image URL (relative URL)
        img_url = img_tag['src']  

        # Extract the last token of the image URL (the image filename)
        image_token = os.path.basename(img_url)

        # Find the school name and roster link (inside <a> tag within class 'schoolname')
        name_tag = row.find('a')
        if name_tag:
            school_name = name_tag.get_text(strip=True)
            roster_link = "https://scores.collegesailing.org" + name_tag['href']  # Construct the full URL for the roster page

            # Extract the school token (last part of the URL in the href attribute)
            school_token = name_tag['href'].split('/')[-2]  # Get the last part before the slash

            # Add the name, image filename, roster link, and school token to the lists
            school_names.append(school_name)
            image_tokens.append(image_token)
            roster_links.append(roster_link)
            school_tokens.append(school_token)

# Create a DataFrame from the lists
data = pd.DataFrame({
    'School Name': school_names,
    'Image Token': image_tokens,  # Storing the last token (filename) of the image URL
    'Roster Link': roster_links,  # Storing the full URL to the school's roster page
    'School Token': school_tokens  # Storing the unique school token
})

try:
    data.to_csv('/home/qbrighto/IdeaProjects/sailing-elo/rosterdata/college_sailing_schools.csv', index=False)
    print("Data successfully saved to CSV.")
except Exception as e:
    print(f"Error saving CSV: {e}")