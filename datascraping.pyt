import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape titles from articles on the site
def scrape_brutalist_report_titles():
    url = 'https://brutalist.report/topic/tech'
    response = requests.get(url)
    
    # Check if the page was retrieved successfully
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return []

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store titles
    titles = []

    # Find article titles (assuming articles are in <a> tags)
    for article in soup.find_all('a', href=True):
        title = article.get_text(strip=True)
        
        # Filter out empty titles
        if title:
            titles.append(title)
    
    return titles

# Get article titles from the site
titles = scrape_brutalist_report_titles()

# Print all scraped titles as a list
print("Scraped Titles:")
for title in titles:
    print(title)

# Write the titles to a CSV file
csv_filename = 'scraped_titles.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title"])  # Writing the header

    for title in titles:
        writer.writerow([title])

print(f"\nAll titles have been written to {csv_filename}")
