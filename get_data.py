import json
import pandas as pd
import re
import requests

from bs4 import BeautifulSoup

SEARCH_URL = 'https://www.hemnet.se/salda/bostader?housing_form_groups%%5B%%5D=apartments&location_ids%%5B%%5D=925958&page=%d'

def extract_listing_links_from_search_results(search_url):
    index = 1
    links = []
    while True:
        print(f'trying {search_url % index}...')
        resp = requests.get(search_url % index)
        if resp.status_code != 200:
            print(f'stopping extraction due to status code {resp.status_code}')
            break
        soup = BeautifulSoup(resp.text, 'html.parser')
        ls = soup.find_all('div', {'class': 'sold-property-listing'})
        print(f'got {len(ls)} results from page {index}')
        if len(ls) == 0:
            print('stopping extraction due to empty results page')
            break
        links.extend([get_listing_link(l) for l in ls])
        index += 1
    return links

def get_listing_link(listing):
    return listing.find('a').attrs['href']

def search_result_to_tuple(l):
    price = digits(l.find('span', {'class': 'sold-property-listing__subheading'}).text)
    ppm2  = digits(l.find('div', {'class': 'sold-property-listing__price-per-m2'}).text)
    fee   = digits(l.find('div', {'class': 'sold-property-listing__fee'}).text)
    date  = l.find('div', {'class': 'sold-property-listing__sold-date'}).text
    link = l.find('a').attrs['href']
    return (price, ppm2, fee, date, link)

def json_from_full_listing(listing_url):
    resp    = requests.get(listing_url)
    soup    = BeautifulSoup(resp.text, 'html.parser')
    script  = [s for s in soup.body('script') if s.string is not None and 'dataLayer' in s.string][0]
    match   = re.search('dataLayer = (.*);', script.string)
    jsonstr = match.groups()[0]
    dicts   = json.loads(jsonstr)
    listing = dicts[-1]['sold_property']
    listing['link'] = listing_url
    return pd.json_normalize(listing).to_dict(orient='records')[0]

def digits(string):
    return ''.join(filter(str.isdecimal, string))

# url = 'https://www.hemnet.se/salda/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D=925958&page=1'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# listings = soup.find_all('div', {'class': 'sold-property-listing'})
# links = [get_listing_link(l) for l in listings]
# table = [listing_html_to_tuple(l) for l in listings]
