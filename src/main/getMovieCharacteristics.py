"""
Header to be added later
"""

import os
import time
import sys

# append the ROOT directory to the python path so it can search thru subdirs
sys.path.insert(0, os.getcwd())

from src.lib import processMovieCharacteristics as charac

print(charac.get_movie_title)

import json
from pprint import pprint

with open('./src/scrap_specs/MovieCharacteristics.json') as data_file:    
    data = json.load(data_file)

pprint(data)
