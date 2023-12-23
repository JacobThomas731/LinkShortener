from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import shortening_algo
from dotenv import load_dotenv, dotenv_values

sa = None
test1 = None


def initialize_database():
    load_dotenv()
    env = dotenv_values()
    global test1
    global sa
    global db
    uri = env['URI']

    client = MongoClient(uri, server_api=ServerApi('1'))
    sa = shortening_algo.ShorteningAlgo()
    db = client['Urlshortener']
    test1 = db['Test1']

    return client


def search_db_for_similar_longwebsite(url):
    return test1.find_one({'longweb': url})


def get_last_pattern():
    res = test1.find_one({'name': 'lastpattern'}).get('pattern')
    return res


def get_next_pattern(pattern):
    return sa.next_value(pattern)


def update_last_pattern(pattern):
    filter = {'name': 'lastpattern'}
    newval = {'$set': {'pattern': pattern}}
    test1.update_one(filter, newval)


def shorturl(longurl):
    url_obj = search_db_for_similar_longwebsite(longurl)
    if url_obj is None:
        pattern = get_last_pattern()
        nextpattern = get_next_pattern(pattern)
        test1.insert_one({'longweb': longurl, 'shorturl': nextpattern})
        update_last_pattern(nextpattern)
        return nextpattern
    else:
        return url_obj['shorturl']


def get_long_website(longurl):
    dict = test1.find_one({'shorturl': longurl})
    print(dict)
    if dict:
        return dict.get('longweb')
    else:
        return None
