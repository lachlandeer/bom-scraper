"""
Main file to scrape the Box Office returns of movies.

This file runs the scraper for all years from 'yearStart' to 'yearEnd', for
all movies of 'releaseType'
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

# Candidate years and release type
# yearStart = int(sys.argv[1])
# yearEnd   = int(sys.argv[2])
# relevantYears = range(yearStart,yearEnd+1)
#
# #releaseType =['wide', 'limited']
# releaseType =['wide']
#
# # directory where the data will be stored
# linkdir = sys.argv[3]
# datadir = sys.argv[4]

# for iYear in relevantYears:
#     for iType in releaseType:
#         linkFile = linkdir + '/bom-links-'    + iType + "-" + str(iYear)

        # with open(linkFile) as f:
        #     df = pd.DataFrame()
        #     for row in csv.reader(f):
        #         currentURL = ''.join(row) # convert list to string
        #         print("scraping:", currentURL)
        #         movie_id, df_movie = boxOffice.process_weekendBoxOffice(currentURL)
        #         # save as a data set
        #         outfile = 'boxOffice-weekend-'+ movie_id
        #         df_movie.to_csv(outfile + '.csv', index = False)

currentURL = 'http://www.boxofficemojo.com/movies/?id=intothewoods.htm'

movie_id, df_movie = boxOffice.process_weekendBoxOffice(currentURL)

outfile = 'boxOffice-weekend-'+ movie_id
df_movie.to_csv(outfile + '.csv', index = False)
