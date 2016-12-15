"""
Descriptive header
"""

import os
import time
import sys

# append the ROOT directory to the python path so it can search thru subdirs
sys.path.insert(0, os.getcwd())

from src.lib import mojoScrapeLinks as mojo

# directory where the data will be stored
datadir = sys.argv[3]

# Candidate years
yearStart = int(sys.argv[1])
yearEnd   = int(sys.argv[2])
relevantYears = range(yearStart,yearEnd)

# Candidate Release Types
releaseType =['wide', 'limited']

# Run scraper - Main loop
for iYear in relevantYears:
    print('Getting Links for', iYear)
    for iType in releaseType:
        if iType == 'wide':
            print('Entering wide release mode')
            typeString = 'widedate'
            mojo.scrapeLinks(typeString, iYear, iType, datadir)
        else:
            print('Entering limited release mode')
            typeString = 'limited'
            mojo.scrapeLinks(typeString, iYear, iType, datadir)
    print('pausing for two minutes before starting next year')
    time.sleep(120)
