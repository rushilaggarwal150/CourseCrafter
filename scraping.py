from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


numbers = [470] 

# Set up the WebDriver
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

professors = []
gpas = []
As = []
Bs = []
Cs = []
Ds = []
Es = []
Fs = []
Qs = []

for number in numbers:
    
    url = f"https://anex.us/grades/?dept=CSCE&number={number}"
    driver.get(url)

    # Get the HTML content after the page is loaded
    time.sleep(5) 

    html = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract data from the table
    dataTable_div = soup.find('div', {'id': 'tableDiv'})
    inner_table = dataTable_div.find('table')
    inner_tbody = inner_table.find('tbody')
    
    rows = inner_tbody.find_all('tr')[1:]  # Skip the header row

    for row in rows:
        columns = row.find_all('td')
        professor = columns[2].text.strip()
        gpa = columns[3].text.strip()
        A = columns[5].text.strip()
        B = columns[6].text.strip()
        C = columns[7].text.strip()
        D = columns[8].text.strip()
        E = columns[9].text.strip()
        F = columns[10].text.strip()
        Q = columns[12].text.strip()

        
        professors.append(professor)
        gpas.append(gpa)
        As.append(A)
        Bs.append(B)
        Cs.append(C)
        Ds.append(D)
        Es.append(E)
        Fs.append(F)
        Qs.append(Q)

driver.quit()

data = {'Professor': professors, 'GPA': gpas, "A's": As, "B's": Bs, "C's": Cs, "D's": Ds, "E's": Es, "F's": Fs, "Q's": Qs}
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
