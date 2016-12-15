"""
This script harvests the links from Box Office Mojo that we will scrape data from.
Collection of links happens by year - release type. So a typical output would be
2015-wide-release.csv

It takes as inputs:
    1. The first year you want to scrape
    2. The last year you want to scrape
    3. The directory where the links will be saved to. Links saved as a csv

File produces a csv of links for each year / release type combination.

Example usage:
    python getlinks.py 2010 2012 outputDirectory

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
relevantYears = range(yearStart,yearEnd+1)

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
