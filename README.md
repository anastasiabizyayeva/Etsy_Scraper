# Etsy_Scraper: Overview

This is a Python Selenium webscraper that grabs listing and shop information on Etsy for search terms the user inputs. The user can also stipulate how many pages of each search term they want to scrape. 

You can see an example of the results of a scrape in the `raw_data.csv` file. Note that shop names are anonymized for security. 

## Running the Webscraper

#### Pre-Requisites

* **Python Version:** 3.9
* **Package Requirements:** Clone the repo and create a virtual environment with the packages listed in 'requirements.txt' file

There are three files you need to run the webscraper:
* `main_scraper.py` runs the actual scraper
* `scraper_functions.py` is a repository for all of the functions used in the main scraper
* `scraper options.py` is the file that allows for customization - it is here that you can 1) define the path to your webdriver, 2) input your list of search terms into the 'search terms' variable, and 3) input the number of pages your want scraped per search term (to a maximum of 240).

<em>Note that in the main_scraper.py file there's a line of code to anonymize shop names. You can take this out if you need the shop names for your exploration.</em>

Once you've made these adjustments, simply run the script - you'll see printouts for every page that's scraped, as well as an overall summary for each search term. 

## Resources Used

* **Overcoming IP Blocks:**
https://medium.com/swlh/improve-your-web-scraper-with-limited-retry-loops-python-35e21730cbf5

## Data Schema

There are 16 columns pulled by this webscraper:

| Column | Description | Data Type|
| --- | --- | --- |
| Title | Title of the listing | string |
| Shop_Name | Anonymized integer as a standin for shop name | int |
| Is_Ad | 1 if a listing is an ad, 0 otherwise | int |
| Star_Rating | Overall star rating for the shop | float |
| Num_Reviews | Total number of reviews for the shop | int |
| Price | Cost of listing item | float |
| Is_Bestseller | 1 if a listing has the 'bestseller' tag, 0 otherwise | int |
| Num_Sales | Total number of sales for the shop | int |
| Num_Basket | Number of items of this listing in people's baskets - '20' represents 'over 20' | int |
| Description | Description of the listing | string |
| Days_to_Arrival | Number of days from the day of the scrape to the mean arrival time for the listing | int |
| Cost_Delivery | Price of delivery - note this will be in your home currency | float |
| Returns_Accepted | 1 if a shop accepts returns, 0 otherwise | int |
| Dispatched_From | Country of origin for the listing | string |
| Num_Images | Total number of images for the listing | int |
| Category | Search term used for the scrape - drop this column if only searching one term | string |

## Limitations

Please feel free to use this webscraper as a starting point for your exploration and make adjustments to improve it! A couple of options for improvement: 
* The scraper is pretty slow - adjustments can be made to increase the speed while still overcoming the IP Block. It current takes about 24 hours to scrape 15,500 records. Some suggestions are to make the webdriver headless and to think about opening all the links in new tabs at the same time so that the scraping can be done concurrently for each page. 
* Additional columns can be added for things like whether the listing is on sale, whether it can be personalized, whether the item is sold in bulk, etc. 
* Once in the listing page, an individual can choose to scrape some of the top reviews for sentiment analysis 

Have fun and please feel free to reach out if you have any questions!
