from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the WebDriver
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

Coursetitle = []
Description = []

url = f"https://catalog.tamu.edu/undergraduate/course-descriptions/csce/"
driver.get(url)

# Get the HTML content after the page is loaded
time.sleep(2) 

html = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract data
Content_div = soup.find('div', {'id': 'col-content'})
Main_div = Content_div.find('main')
Class_div = Main_div.find('div')

titles = Class_div.find_all('h2', class_='courseblocktitle')
descriptions = Class_div.find_all('p', class_='courseblockdesc')

for title in titles:
    Coursetitle.append(title.text.strip())
#
for desc in descriptions:
    cleaned_desc = desc.text.strip().replace('\n', ' ')
    Description.append(cleaned_desc)

driver.quit()

data = {'Course Title': Coursetitle, 'Description': Description}
df = pd.DataFrame(data)

# print(df)

for index, row in df.iterrows():
    print(f"Course Title: {row['Course Title']}, Description: {row['Description']}")


