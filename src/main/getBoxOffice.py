"""
Main file to scrape the Box Office returns of movies.

This file runs the scraper for all years from 'yearStart' to 'yearEnd', for
all movies of 'releaseType.'

Returns Box office of type 'frequency' which must be listed as sys.argv[5]
"""

import os
import time
import sys
from random import randint
import pandas as pd
import csv

# append the ROOT directory to the python path so it can search thru subdirs
sys.path.insert(0, os.getcwd())

from src.lib import processBoxOfficeReturns as boxOffice

#Candidate years and release type
yearStart = int(sys.argv[1])
yearEnd   = int(sys.argv[2])
relevantYears = range(yearStart,yearEnd+1)

#releaseType =['wide', 'limited']
releaseType =['wide']

# directory where the data will be stored
linkdir     = sys.argv[3]
datadirRoot = sys.argv[4]
# frequency of collection
frequency = sys.argv[5]

for iYear in relevantYears:
    for iType in releaseType:
        linkFile = linkdir + '/bom-links-'    + iType + "-" + str(iYear)

        with open(linkFile) as f:
            for row in csv.reader(f):
                currentURL = ''.join(row) # convert list to string
                print("scraping:", currentURL)
                if frequency == 'weekend':
                    movie_id, df_movie = boxOffice.process_weekendBoxOffice(currentURL)

                    outfile = 'boxOffice-weekend-'+ movie_id
                elif frequency == 'weekly':
                    movie_id, df_movie = boxOffice.process_weeklyBoxOffice(currentURL)

                    outfile = 'boxOffice-weekly-'+ movie_id
                elif frequency == 'daily':
                    movie_id, df_movie = boxOffice.process_dailyBoxOffice(currentURL)

                    outfile = 'boxOffice-daily-'+ movie_id
                else:
                    pass
                # save the data
                datadir = datadirRoot + '/' + str(iYear) + '/'
                df_movie.to_csv(datadir + outfile + '.csv', index = False)
                # pause between pages
                time.sleep(randint(5,15))
