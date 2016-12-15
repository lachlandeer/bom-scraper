"""
Descriptive header
"""

import os

print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

import time
import sys

print(sys.path)


from src.lib import mojoScrapeLinks




print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

datadir = sys.argv[3]
print(datadir)

STOP
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
