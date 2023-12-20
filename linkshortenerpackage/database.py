from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from linkshortenerpackage import shortening_algo
from dotenv import load_dotenv, dotenv_values


load_dotenv()
env = dotenv_values()

uri = env['URI']

client = MongoClient(uri, server_api=ServerApi('1'))
sa = shortening_algo.ShorteningAlgo()
db = client['Urlshortener']
test1 = db['Test1']


def search_db_for_similar_longwebsite(url):
    res = test1.find_one({'longweb': url})
    if res is None:
        return False
    else:
        return True


def get_last_pattern():
    res = test1.find_one({'name': 'lastpattern'}).get('pattern')
    return res


def get_next_pattern(pattern):
    return sa.next_value(pattern)


def update_last_pattern(pattern):
    filter = {'name':'lastpattern'}
    newval = {'$set': {'pattern': pattern}}
    test1.update_one(filter, newval)


def shorturl(longurl):
    if search_db_for_similar_longwebsite(longurl) is False:
        pattern = get_last_pattern()
        nextpattern = get_next_pattern(pattern)
        test1.insert_one({'longweb': longurl, 'shorturl': nextpattern})
        update_last_pattern(nextpattern)
        return nextpattern

