import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#### Define your webdriver options ####

url = 'https://www.numbeo.com/cost-of-living/'
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options)

#### To scrape only 100 links, choose limited = True. To scrape all data, choose limit = False ####

limited = True
upper_limit = 100

#### Create empty data frame for results ####

d = pd.DataFrame({'country':[], 'city':[], 'item':[], 'prize':[], 'left':[], 'right':[] })

#### Run first page ####
 
driver.get(url)

#### Get links to all countries ####
 
field = (By.XPATH,'//table[@class="related_links"]/tbody/tr/td/a')
# wait until element will be visible
WebDriverWait(driver, 1).until(EC.presence_of_element_located(field))
country_names = driver.find_elements_by_xpath(field[1])
country_links = [country.get_attribute('href') for country in country_names]

#### Go to city pages through country links ####
unique_cities = 0
for href in country_links:

    # If limit was selected, then code will not continue when number of unique combinations reaches 100.
    if((limited == True and unique_cities < upper_limit) or limited == False):
        
        # Go to country page
        driver.get(href)

        # Scrape country name
        field_country = (By.XPATH,'//span[@itemprop = "name"]')
        # wait until element will be visible
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(field_country))
        country = driver.find_elements_by_xpath(field_country[1])[1].text

        # Scrape city names
        field_city = (By.XPATH,'//select[@id="city"]/option')
        # wait until element will be visible
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(field_city))
        cities_list = [element.get_attribute("value") for element in driver.find_elements_by_xpath(field_city[1])[1:]]

        # Default GET Request, where country and city will be filled to create city links 
        link = "https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}&displayCurrency=USD"

        #### Go through all city links in the country ####

        for city in cities_list:

            # If limit was selected, then code will not continue when number of unique combinations reaches 100.
            if((limited == True and unique_cities < upper_limit) or limited == False):

                print(d.groupby(['country', 'city']).ngroups)
                # Get link for city website
                direct_link = link.format(country,city)

                # Go to the city website
                driver.get(direct_link)
                
                # Gather all rows table
                field_rows = (By.XPATH,'//html/body/div[2]/table//tr')
                # wait until element will be visible
                WebDriverWait(driver, 1).until(EC.presence_of_element_located(field_rows))
                elements = driver.find_elements_by_xpath(field_rows[1])
                # Iterate through each row in a table and get items and prizes
                for element in elements:    
                    
                    # get item name from 1st column
                    try:
                        item = element.find_element_by_xpath('./td').text
                    except:
                        continue
                    
                    # get prize name from 2nd column
                    try:
                        prize = element.find_elements_by_xpath(".//span")[0].text.replace('$','')
                    except:
                        prize = np.nan
                    
                    # get left boundry from 3rd column
                    try:
                        left = element.find_element_by_xpath('./td/span[@class="barTextLeft"]').text.strip()
                    except:
                        left = np.nan

                    # get right boundry from 3rd column
                    try:
                        right = element.find_element_by_xpath('./td/span[@class="barTextRight"]').text.strip()
                    except:
                        right = np.nan

                    # put all data into dataframe
                    df = {'country': country, 'city': city, 'item':item, 'prize':prize, 'left':left, 'right':right}
                    d = d.append(df, ignore_index = True)

                    # unique cities after new data
                    unique_cities = d.groupby(['country', 'city']).ngroups

driver.quit()

print(d)

d.to_csv('costs.csv')


