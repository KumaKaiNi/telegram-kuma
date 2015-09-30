import json, os

DIR = os.path.dirname(os.path.realpath(__file__))
FOLDER = DIR + '/__cache__/'
CACHE = {
   'img': FOLDER + 'img/',
   'subreddits': FOLDER + 'subreddits/',
   'wordlogs': FOLDER + 'wordlogs/',
}