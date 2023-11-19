from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


numbers = [402, 410, 412, 413, 416, 420, 421, 426, 429, 430, 431, 432, 433, 434, 435, 436, 438, 439, 440, 441, 442, 443, 444, 445, 446,
           447, 448, 449, 450, 451, 452, 456, 461, 462, 463, 464, 465, 469, 470, 477, 485, 489, 491]  

# Set up the WebDriver
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

CourseNum = []
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
    time.sleep(2) 

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

        CourseNum.append(number)
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

data = {'Course Number': CourseNum, 'Professor': professors, 'GPA': gpas, "As": As, "Bs": Bs, "Cs": Cs, "Ds": Ds, "Es": Es, "Fs": Fs, "Qs": Qs}
df = pd.DataFrame(data)

# Display the DataFrame
#print(df)

for index, row in df.iterrows():
    print(f"Course Number: {row['Course Number']}, Professor: {row['Professor']}, GPA: {row['GPA']}, A's: {row['As']}, B's: {row['Bs']}, C's: {row['Cs']}, D's: {row['Ds']}, E's: {row['Es']}, F's: {row['Fs']}, Q's: {row['Qs']}")

