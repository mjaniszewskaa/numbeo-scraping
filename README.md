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

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
