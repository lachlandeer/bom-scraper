# User must set this

datadir = '../links/'

# Import packages

import os
import time
import mojoScrapeLinks as mojo

# check directories
print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

if not os.path.exists(datadir):
    os.makedirs(datadir)

# Candidate Release Types
releaseType =['wide', 'limited']

# Candidate years
relevantYears = range(2010,2017)


# Run scraper
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
