from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from . import shortening_algo as sa
from dotenv import load_dotenv, dotenv_values

shortening_algo = None
url_shortener_collection = None


def initialize_database():
    """
    Initializes the database. This function is called at the start of the application.
    :return: Returns the MondoDB client
    """
    global url_shortener_collection
    global shortening_algo
    global database

    load_dotenv()
    env = dotenv_values()
    uri = env['URI']
    db_name = env['DATABASE_NAME']
    db_collection_name = env['DB_COLLECTION_NAME']

    client = MongoClient(uri, server_api=ServerApi('1'))
    shortening_algo = sa.ShorteningAlgo()
    database = client[db_name]
    url_shortener_collection = database[db_collection_name]

    return client


def search_db_for_similar_long_url(url):
    """
    This function is used to check if a similar long url exists on the database
    :param url: the long url that needs to be checked
    :return: The corresponding short url is it exists or else null
    """
    return url_shortener_collection.find_one({'long_url': url})


def get_last_pattern():
    """
    This function checks the database for the last sequential short url pattern that has been generated yet
    :return: the last short url pattern that is stored
    """
    return url_shortener_collection.find_one({'name': 'last_pattern'}).get('pattern')


def get_next_pattern(pattern):
    """
    This function is used to generate the next short url pattern based on the previous pattern
    :param pattern: currently used short url pattern
    :return: the next short url pattern
    """
    return shortening_algo.next_value(pattern)


def update_last_pattern(pattern):
    """
    This function updates the last short url pattern stored in the Database with the lastest generated pattern
    :param pattern: the latest generated short url pattern
    :return: returns confirmation message
    """
    db_filter = {'name': 'last_pattern'}
    new_value = {'$set': {'pattern': pattern}}
    return url_shortener_collection.update_one(db_filter, new_value)


def short_url(long_url):
    """
    This function takes the long url and returns the short url. It uses a bunch of other function to do the job.
    Checks the database for similar long url.
    :param long_url: the long url that needs to be shortened
    :return: short url pattern.
    """
    url_obj = search_db_for_similar_long_url(long_url)
    if url_obj is None:
        pattern = get_last_pattern()
        next_pattern = get_next_pattern(pattern)
        url_shortener_collection.insert_one({'long_url': long_url, 'short_url': next_pattern})
        update_last_pattern(next_pattern)
        return next_pattern
    else:
        return url_obj['short_url']


def get_long_website(short_url):
    """
    This function accepts a short url and returns the corresponding long url if it exists
    :param short_url: the short url pattern
    :return: long url if it exists or else none
    """
    dict = url_shortener_collection.find_one({'short_url': short_url})
    if dict:
        return dict.get('long_url')
    else:
        return None
