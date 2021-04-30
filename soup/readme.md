

### Beautiful Soup

Prerequisites:

* Python 3.6 or later
* Libraries installed:  
    - pandas~=1.0.3
    - numpy~=1.18.2
    - beautifulsoup4~=4.9.3

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

