"""Python file to scrap list of countries from CIA archived website."""
import os

from bs4 import BeautifulSoup

# Load the HTML file
file_path = "src/replication_ppr/data/countrylisting.html"
if os.path.isfile(file_path):
    with open(file_path) as f:
        html_content = f.read()


# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
soup
# Find the HTML element that contains the list of countries
a_tags = soup.find_all("a")

# Extract the country names from the <a> tags
countries = [a_tag.text for a_tag in a_tags]
countries = [i for i in countries if not i.isupper() or len(i) > 1]
