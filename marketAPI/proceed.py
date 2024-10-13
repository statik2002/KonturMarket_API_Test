from pprint import pprint
from environs import Env
from utils import get_shops, get_today_proceed

env = Env()
env.read_env()

api_key = env('API_KEY')

shops = get_shops(api_key)

today_proceed = get_today_proceed(api_key, shops[0]['id'])

pprint(today_proceed)




