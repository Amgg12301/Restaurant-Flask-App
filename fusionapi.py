from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

try:
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    from urllib import HTTPError
    from urllib import quote
    from urllib import urlencode

API_KEY = 'MLr3UDZ5PA4ZJOlKk0RsNvFDYwhARImGCXT0NF2zjcGZv1NsIsYtwRODsiURFyx75huuGJFe6T8RbTkExwAS2bMlxmeIa8TXMGfc545sAbMegzkboU6i7WziJTBkXnYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, latitude, longitude, price, number):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'price': price,
        'limit': number
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, latitude, longitude, price, number):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, latitude, longitude, price, number)
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} {2} found for {3}.'.format(term, latitude, longitude, price))
        return

    business_id = businesses[0]['id']

    for business in businesses:
        print(business)

    return businesses
        
