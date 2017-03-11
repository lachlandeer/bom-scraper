"""
This collection of functions scrapes Box Office Returns at the
weekly, weekend, and daily levels from a film's page on Box Office Mojo.

Last Edit: March, 2017
"""

import requests
from bs4 import BeautifulSoup
import re
import dateutil.parser
from string import ascii_uppercase
import pandas as pd
# import pickle
import time
import urllib.request
import csv

import requests
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=10)
sess.mount('http://', adapter)
