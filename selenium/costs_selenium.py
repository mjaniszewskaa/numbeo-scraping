import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm.auto import trange
import time
now_time = time.time()

#### Define your webdriver options ####

url = 'https://www.numbeo.com/cost-of-living/'
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options)

#### To scrape only 100 links, choose limited = True. To scrape all data, choose limit = False ####

limited = True
upper_limit = 100

#### Create empty data frame for results ####

d = pd.DataFrame({'Country':[], 'City':[], 'Category':[],'Name':[], 'Price':[], 'Min':[], 'Max':[] })

#### Run first page ####
 
driver.get(url)

#### Get links to all countries ####
 
field = (By.XPATH,'//table[@class="related_links"]/tbody/tr/td/a')
# wait until element will be visible
WebDriverWait(driver, 30).until(EC.presence_of_element_located(field))
country_names = driver.find_elements_by_xpath(field[1])
country_links = [country.get_attribute('href') for country in country_names]

#### Go to city pages through country links ####
unique_cities = 0
for country_link in country_links:

    # If limit was selected, then code will not continue when number of unique combinations reaches 100.
    if((limited == True and unique_cities < upper_limit) or limited == False):
        
        try:
            # Go to country page
            driver.get(country_link)
        except:
            continue

        # Scrape country name
        field_country = (By.XPATH,'//span[@itemprop = "name"]')
        # wait until element will be visible
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(field_country))
        country = driver.find_elements_by_xpath(field_country[1])[1].text
        
        print('\n'+ country +'\n')

        # Scrape city names
        field_city = (By.XPATH,'//select[@id="city"]/option')
        # wait until element will be visible
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(field_city))
        cities_list = [element.get_attribute("value") for element in driver.find_elements_by_xpath(field_city[1])[1:]]

        # Default GET Request, where country and city will be filled to create city links 
        link = 'https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}&displayCurrency=USD'

        #### Go through all city links in the country ####

        n_cities = len(cities_list)
        for j in trange(n_cities, desc = 'Cities: '):

            # If limit was selected, then code will not continue when number of unique combinations reaches 100.
            if((limited == True and unique_cities < upper_limit) or limited == False):

                # Get link for city website
                direct_link = link.format(country,cities_list[j])

                try:
                    # Go to the city website
                    driver.get(direct_link)
                except:
                    continue

                try:
                    # Gather all rows table
                    field_rows = (By.XPATH,'//html/body/div[2]/table//tr')
                    # wait until element will be visible
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located(field_rows))
                    elements = driver.find_elements_by_xpath(field_rows[1])
                
                except:
                    continue
                
                # Iterate through each row in a table and get items and prizes
                for element in elements:    
                    
                    # Get category, which will be assigned to every item, in case some of them is classified in more than 1 category.
                    try: 
                        category = element.find_element_by_xpath('.//div[@class="category_title"]').text
                    except:
                        pass

                    # Get item name from 1st column. If the row contains only category name (not item name), continue to scrape next row.
                    try:
                        name = element.find_element_by_xpath('./td').text
                    except:
                        continue

                    # Get price name from 2nd column
                    try:
                        price = element.find_elements_by_xpath(".//span")[0].text.replace('$','')
                    except:
                        price = np.nan
                    
                    # Get left boundry from 3rd column
                    try:
                        min = element.find_element_by_xpath('./td/span[@class="barTextLeft"]').text.strip()
                    except:
                        min = np.nan

                    # Get right boundry from 3rd column
                    try:
                        max = element.find_element_by_xpath('./td/span[@class="barTextRight"]').text.strip()
                    except:
                        max = np.nan

                    # Put all data into dataframe
                    df = {'Country': country, 'City': cities_list[j], 'Category':category,'Name':name, 'Price':price, 'Min':min, 'Max':max}
                    d = d.append(df, ignore_index = True)

                    # Unique cities after new data
                    unique_cities = d.groupby(['Country', 'City']).ngroups
                    

driver.quit()

print(d)
d.to_csv('costs.csv')

print('Overall running time:', round(time.time()-now_time,2), 'seconds.')

