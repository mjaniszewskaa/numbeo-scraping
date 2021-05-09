###########################################################################################################
# PROJECT BeautifulSoup
# numbeo-scraping
###########################################################################################################

from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd
import numpy as np
import urllib.parse
import time
from tqdm import tqdm
start = time.time()

# If the limit = True then only 100 first cities will be scraped
limit = True
cities_scraped = 100 if limit else float('inf')

# If export = True then the data will be exported to csv file
export_to_csv = True

##################### 1. Get names of the country #######################################################
url = 'https://www.numbeo.com/cost-of-living/'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

# Countries from dropdown list
tags = bs.find('select', id='country').find_all('option')
country_names = [tag['value'] for tag in tags]
country_names.remove(country_names[0])  # remove 1 element with value: ---Select country---


##################### 2. Extract links to cities in each country ########################################
d = pd.DataFrame({'Country': [], 'City': [], 'Category': [], 'Name': [], 'Price': [], 'Min': [], 'Max': []})

cities_links = []
for country in country_names:

    # Limit of cities that will be scraped
    if len(cities_links) < cities_scraped:
        params = {'country': country, 'displayCurrency': 'USD'}
        link = url + 'country_result.jsp?' + urllib.parse.urlencode(params)
        html = request.urlopen(link)
        bs = BS(html.read(), 'html.parser')

        # Countries from dropdown list
        tags = bs.find('select', id='city').find_all('option')
        cities_names = [tag['value'] for tag in tags]
        cities_names.remove(cities_names[0])  # remove 1 element with value: ---Select country---

        # Extract links for each city
        link_temp_list = []
        for city in cities_names:
            params = {'country': country, 'city': city, 'displayCurrency': 'USD'}
            link_template = url + 'city_result.jsp?' + urllib.parse.urlencode(params)
            link_temp_list.append(link_template)

            # Limit of cities that will be scraped
            if len(cities_links + link_temp_list) == cities_scraped: break


        # Limit of cities that will be scraped
        cities_links.extend(link_temp_list)

        if len(cities_links) >= cities_scraped: break


##################### 3. Get data for each city #######################################################

for link in tqdm(cities_links):

    html = request.urlopen(link)
    bs = BS(html.read(), 'html.parser')

    ## CITY & COUNTRY
    b = bs.find('nav', class_='breadcrumb')

    # If links are not available to reach
    if not b:
        continue

    tags_1 = b.find_all('a', class_='breadcrumb_link')

    country = tags_1[1].get_text().strip() if len(tags_1) > 1 else ''
    city = tags_1[2].get_text().strip() if len(tags_1) > 2 else ''

    ##  CATEGORY & NAME & PRICE
    tags_2 = bs.find('table', class_='data_wide_table new_bar_table').find_all('tr')
    category = ''

    for tag in tags_2:
        td = tag.find('td')
        if td:
            name = td.get_text()
        else:
            # If tag above does not work it means that it is a category of products
            category = tag.find('div', class_='category_title').get_text()
            continue

        # Prices are in USD so we cut the $ symbol
        price_tag = tag.find('span', class_='first_currency')
        price = price_tag.text.replace('$', '') if price_tag else np.nan

        # Some prices have '/n' in html code so there is a need to use strip()
        min_tag = tag.find('span', class_='barTextLeft')
        min_price = min_tag.text.strip() if min_tag else np.nan

        max_tag = tag.find('span', class_='barTextRight')
        max_price = max_tag.text.strip() if max_tag else np.nan

        # Combine all info and add to dataframe
        info = {'Country': country, 'City': city, 'Category': category,
                'Name': name, 'Price': price, 'Min': min_price, 'Max': max_price}
        d = d.append(info, ignore_index=True)


print(d)
print('It took', time.time()-start, 'seconds.')

if export_to_csv:
    d.to_csv('prices_bs.csv', encoding='utf-8-sig')
