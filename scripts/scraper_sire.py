from pathlib import Path
import requests
from bs4 import BeautifulSoup

# 1. Target URL
url = "https://serb.gov.in/page/sire"

# 2. Fetch the page
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to load page: {response.status_code}")
    exit()

# 3. Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# 4. Extract main content
# We'll pick everything inside <main> if available or fallback to body text
main_content = ""

# Attempt a specific content container if present
container = soup.find("div", class_="content")
if container:
    main_content = container.get_text(separator="\n", strip=True)
else:
    main_content = soup.get_text(separator="\n", strip=True)

# 5. Save to file
output_path = Path(__file__).resolve().parent.parent / "data" / "sire_page.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(main_content)

print("Scraping done — saved to data/sire_page.txt")

"""
okay so
we first call beautiful soup (what is soup tho here) and it has 2 parameters, the response text that is which response will be generated ig? and the html parser which allows to convert html code into interactable text and then we assign this to soup (which the whole website ig)

then we declare a container, which will contain the data that we want the user to get or the user requests
in that container, we assign to it this: soup.find() which will search for stuff in the website. ( in that soup will find a section (division/div) which will contain content (what is content tho? the thing that the user requests ig?))
then the if statement
if container finds the content, we assign the text contained in the container to the main content and display it (using get text we get clean text and remove all the tags and stuff, we seperate text by a new line, and what is strip?)
else:
display everything, by assigning all values of soup (the website) (seperate it by a new line, and what is strip again?)

did i get it right or what 
"""