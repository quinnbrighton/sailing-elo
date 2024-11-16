import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Load the schools CSV file
schools_df = pd.read_csv('rosterdata/college_sailing_schools.csv')

# Prepare a list to hold all sailor data
sailors_data = []

# Function to scrape sailor roster from a school's roster page
def scrape_roster(school_token, school_name, image_token):
    # Build the roster URL (assuming the URL format is: https://scores.collegesailing.org/schools/{school_token}/{f24}/roster/)
    roster_link = f"https://scores.collegesailing.org/schools/{school_token}/f24/roster/"
    
    # Send a GET request to fetch the school's roster page
    response = requests.get(roster_link)
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the roster table (assuming it's inside a <div class="port"> and class "roster-table")
    roster_table = soup.find('table', class_='roster-table')  # Adjust if the class is different
    
    if roster_table:
        rows = roster_table.find_all('tr')[1:]  # Skip the header row
        
        for row in rows:
            # Extract sailor name and year
            sailor_name_tag = row.find('td', class_='sailor-name')
            sailor_year_tag = row.find('td', class_='sailor-year')
            
            if sailor_name_tag and sailor_year_tag:
                sailor_name = sailor_name_tag.get_text(strip=True)
                sailor_year = sailor_year_tag.get_text(strip=True)
                
                print(sailor_name)
                # Append the sailor's data along with school details
                sailors_data.append({
                    'Sailor Name': sailor_name,
                    'Year': sailor_year,
                    'School Name': school_name,
                    'Image Token': image_token,
                    'School Token': school_token
                })

# Loop through each school in the CSV and scrape its roster
for _, row in schools_df.iterrows():
    school_name = row['School Name']
    image_token = row['Image Token']
    school_token = row['School Token']
    
    # Scrape the roster for this school
    scrape_roster(school_token, school_name, image_token)

# Convert the sailors' data to a DataFrame
sailors_df = pd.DataFrame(sailors_data)

# Save the DataFrame to a CSV file
sailors_df.to_csv('rosterdata/sailors_roster.csv', index=False)

print("Sailors' roster data successfully scraped and saved to 'rosterdata/sailors_roster.csv'")
