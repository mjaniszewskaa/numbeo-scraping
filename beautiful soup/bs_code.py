################################################################################
# PROJECT BS
################################################################################

from urllib import request
from bs4 import BeautifulSoup as BS
import re
from datetime import datetime
import pandas as pd

# If the limit=True then only 100 first cities will be scraped
limit = True
if limit == True:
    number_of_cities = 100
i = 0


# Get names of the country
url = 'https://www.numbeo.com/cost-of-living/'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

# Get cities from dropdown list
tags = bs.find('select', id = "country").find_all("option")
country_names = [tag["value"] for tag in tags]
country_names.remove(country_names[0]) # remove 1 element without a value
country_names = [i.replace(" ", '+') for i in country_names]

# print(*country_names)
################################################################################
# Prepare empty dataframe for data from cities
d = pd.DataFrame({'Country':[],  'City':[],'Name':[], 'Price': [], "Min":[], 'Max':[]})

# Loop for each country
for country in country_names[:]:
    if i<number_of_cities and limit==True:

        link = 'https://www.numbeo.com/cost-of-living/country_result.jsp?country={}&displayCurrency=USD'.format(country)

        # Get names of the cities
        html = request.urlopen(link)
        bs = BS(html.read(), 'html.parser')

        tags = bs.find('select', id = "city").find_all("option")
        cities_names = [tag["value"] for tag in tags]
        cities_names.remove(cities_names[0]) # remove 1 element: --- Select city---
        # cities_names = [i.replace(" ", '-') for i in cities_names]
        print(*cities_names)

        ################################################################################

        # Loop for each city in each country
        tags = bs.find('table', class_= "data_wide_table new_bar_table").find_all("tr")
        for city in cities_names:
            if i<number_of_cities and limit==True:
                i+=1
                # Prepare link for each city
                city_link = "https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}&displayCurrency=USD".format(country, city)
                print(city_link)
                html = request.urlopen(url)
                bs = BS(html.read(), 'html.parser')

                # Get data from each city

                # CITY - from this loop iteration
                # city = city.replace("-"," ")

                # COUNTRY - from country loop iteration
                country = country.replace("+"," ")

                #   NAME & PRICE
                for tag in tags:
                    try:
                        name = tag.find("td").get_text()
                        # Prices are in USD so we cut the $ symbol
                        price = tag.find("span", class_="first_currency").get_text().replace('$','')

                        # Some prices have '/n' in html code so there is a need to use lstrip()
                        try:
                            min = tag.find("span", class_="barTextLeft").get_text().lstrip()
                        except:
                            min = tag.find("span", class_="barTextLeft").get_text()
                        max = tag.find("span", class_="barTextRight").get_text()

                        # Combine all info and add to dataframe
                        info = {'Country':country, 'City':city, 'Name':name,'Price':price, 'Min':min, 'Max': max}
                        d = d.append(info, ignore_index = True)

                    except:pass


print(d)

d.to_csv('prices_bs.csv', encoding='utf-8-sig')
