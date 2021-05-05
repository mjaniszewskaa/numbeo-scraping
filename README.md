# numbeo-scraping

The aim of the project is to gather data about the cost of living in various cities around the world from the webpage:

<p align="center"> https://www.numbeo.com/cost-of-living/ </p>

Three scraping methods are being compared:

* Beautiful soup
* Scrapy
* Selenium

There are over 7000 cities available on the webpage.

### Disclaimer

Project was created only for educational purposes.

## Usage

### Scrapy

Prerequisites:

* Python 3.6 or later
* Scrapy

Just navigate to the scrapy folder and run the command:

``python3 run.py``

It calls sequentially three spiders:

``countries.py``
``cities.py``
``costs.py``

The first gathers the list of all countries present at the website. The second one uses this list to crawl through the pages of these countries and extracts all possible city names. Finally the last one uses this list to crawl through all possible cities and gathers the required data.

By default this will gather the links from the top 100 countries and attempt to collect price information from the top 100 cities from the list. One can eliminate this restriction by changing the value of the ``limit`` variable to ``false`` or change the limit size by manipulating the value of the ``max_size`` parameter - both are declared on top of the ``run.py`` script.



### Beautiful Soup

Prerequisites:

* Python 3.6 or later
* Libraries installed:  
    - pandas~=1.0.3
    - numpy~=1.18.2
    - beautifulsoup4~=4.9.3
    - tqdm~=4.42.0

To run a program use your python interpreter and run a file `soup_script.py` located in **soup** folder. 


By default, only 100 first cities will be scraped. 
To modify limit find the limit variable and change to `False` 
or change value for `cities_scraped = 100` variable.  
Additionally, you can export it to `prices_bs.csv` file by changing `export` variable to `True`.

The script is divided in 3 parts: 

1. Get names of the country - where countries are extracted from the dropdown list.

2. Extract links to cities in each country - where for each country the program will find cities (from dropdown list) and prepare links for them. In here you can find a limit condition. 

3. Get data for each city - as soon as the links are prepared program gets data for selected variables: country, city, category, price, minimum  and maximum price. 

After it's done there will be a data frame `d` with the data and will be exported to `.csv` depending on your decision. 



### Selenium

Prerequisites:

* Python 3.6 or later
* Firefox and GeckoDriver on the PATH.
* Libraries installed:  
    - pandas~=1.0.3
    - numpy~=1.18.2
    - selenium~=3.141.0

The file `costs_selenium.py` is responsible for selenium web scraping, and is located in selenium folder.
Before running the code, make sure that GeckoDriver is on the PATH for code to work. In case it is undesired, please add GeckoDriver path location while defining webdriver options in the following way:

```
gecko_path = 'path/to/geckodriver' # here add your webdriver path

url = 'https://www.numbeo.com/cost-of-living/'
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options, executable_path = gecko_path) # geckodriver executable path is defined
```

Code structue:

1. Define your webdriver options.
2. Choose if number of links scraped should be limited. By default, variable `limited` is set to **True**, and program will only scrape 100 links. To scrape all data, set variable `limited` to False. To change the limit, set variable `upper_limit` to the required value.
3. Gather links to all countries from homepage.
4. Get to each country page and extraxt city names from the dropdown list.
5. Use GET request to be redirected to each city page, and scrape all data regarding prices there.
6. Put all data into collective dataframe, which will be extracted to .csv file at the very end.

**Disclaimer**: In order to improve tracking the webscraping progress, progress bars were added for cities scraped in each country.


## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
