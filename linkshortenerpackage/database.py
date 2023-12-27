from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from . import shortening_algo as sa
from dotenv import load_dotenv, dotenv_values

shortening_algo = None
url_shortener_collection = None


def initialize_database():
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
    return url_shortener_collection.find_one({'long_url': url})


def get_last_pattern():
    res = url_shortener_collection.find_one({'name': 'last_pattern'}).get('pattern')
    return res


def get_next_pattern(pattern):
    return shortening_algo.next_value(pattern)


def update_last_pattern(pattern):
    db_filter = {'name': 'last_pattern'}
    new_value = {'$set': {'pattern': pattern}}
    url_shortener_collection.update_one(db_filter, new_value)


def short_url(long_url):
    url_obj = search_db_for_similar_long_url(long_url)
    if url_obj is None:
        pattern = get_last_pattern()
        next_pattern = get_next_pattern(pattern)
        url_shortener_collection.insert_one({'long_url': long_url, 'short_url': next_pattern})
        update_last_pattern(next_pattern)
        return next_pattern
    else:
        return url_obj['short_url']


def get_long_website(long_url):
    dict = url_shortener_collection.find_one({'short_url': long_url})
    if dict:
        return dict.get('long_url')
    else:
        return None
