from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import *
import time
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd



service_obj = Service()
driver = webdriver.Chrome(service=service_obj)

driver.get( "https://www.mcxindia.com/market-data/spot-market-price")
driver.maximize_window()


## click on recent button
recent_button = driver.find_element(By.XPATH , "//div[@class='today']")
recent_button.click()
time.sleep(2)

### 

# gold input dropdown
gold_drop = driver.find_element(By.ID , "ctl00_cph_InnerContainerRight_C004_ddlSymbols_Input")
gold_drop.click()
gold_drop.send_keys('GOLD')
gold_drop.send_keys(Keys.ENTER) 
time.sleep(2)


## all  input dropdown button
all_drop = driver.find_element(By.ID , "ctl00_cph_InnerContainerRight_C004_ddlLocationArchive_Input")
all_drop.click()
all_drop.send_keys('ALL')
all_drop.send_keys(Keys.ENTER)
time.sleep(2)  


## session 2  select dropdown button
session_drop = Select(driver.find_element(By.ID , "cph_InnerContainerRight_C004_ddlSession"))
session_drop.select_by_visible_text("Session 2")
time.sleep(2)  


## from date 

from_date = driver.find_element(By.ID , "txtFromDate")
from_date.click()
time.sleep(1)

target_month = "November"  
target_year = "2023"

# Locate the month and year dropdowns
month_element = driver.find_element(By.XPATH, "//select[@title='Change the month']")
year_element = driver.find_element(By.XPATH, "//select[@title='Change the year']")

# Loop until the desired month and year are selected
while not (month_element.find_element(By.CSS_SELECTOR, 'option:checked').text == target_month and year_element.find_element(By.CSS_SELECTOR, 'option:checked').text == target_year):
    driver.find_element(By.XPATH, "//a[@title='Show the previous month']").click()
    month_element = driver.find_element(By.XPATH, "//select[@title='Change the month']")
    year_element = driver.find_element(By.XPATH, "//select[@title='Change the year']")

# Select the specific day
driver.find_element(By.XPATH, "//a[@title='Select Wednesday, Nov 1, 2023']").click()
time.sleep(1)  


### to date 
to_date = driver.find_element(By.ID , "txtToDate")
to_date.click()
time.sleep(1)

target_month = "January"  
target_year = "2024"

# Locate the month and year dropdowns
month_element = driver.find_element(By.XPATH, "//select[@title='Change the month']")
year_element = driver.find_element(By.XPATH, "//select[@title='Change the year']")

# Loop until the desired month and year are selected
while not (month_element.find_element(By.CSS_SELECTOR, 'option:checked').text == target_month and year_element.find_element(By.CSS_SELECTOR, 'option:checked').text == target_year):
    driver.find_element(By.XPATH, "//a[@title='Show the previous month']").click()
    month_element = driver.find_element(By.XPATH, "//select[@title='Change the month']")
    year_element = driver.find_element(By.XPATH, "//select[@title='Change the year']")

# Select the specific day
driver.find_element(By.XPATH, "//a[@title='Select Wednesday, Jan 24, 2024']").click()
time.sleep(1)  



### Show button
show_button =driver.find_element(By.ID , "btnShowArchive")
show_button.click()
time.sleep(5)  



### fetch data from url 
soup = BeautifulSoup(driver.page_source, 'html.parser')

## column header 
header = soup.find_all('th')
title = [t.text.strip() for t in header  ]
title = title[:5]



# fetch row data
row_data = []
table = soup.find('table', {'id': 'tblSMP'})
for tr in table.tbody.find_all('tr'):
    row = [td.text for td in tr.find_all('td')]
    row_data.append(row)

df = pd.DataFrame(row_data , columns= title)
print(df)     



### Total no of Rows 
total_row = len(df)
print("total no of rows   " ,  total_row)

### another method to find total row 
print( "another method by shape" , df.shape[0])

## highest spot price
max_spot_price = df['Spot Price (Rs.)'].max()
print("highest spot price " , max_spot_price)


## to save in excel 
df.to_excel(r"/Users/manavbaisoya/Desktop/Assignment_IMARC/Raw Data.xlsx",index=False)

driver.quit()