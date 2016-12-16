"""
Header to be added later
"""

import os
import time
import sys
from random import randint
import pandas as pd
import csv

# append the ROOT directory to the python path so it can search thru subdirs
sys.path.insert(0, os.getcwd())

from src.lib import processMovieCharacteristics as charac

# Candidate years and release type
yearStart = int(sys.argv[1])
yearEnd   = int(sys.argv[2])
relevantYears = range(yearStart,yearEnd+1)

releaseType =['wide', 'limited']

# directory where the data will be stored
linkdir = sys.argv[3]
datadir = sys.argv[4]

#linkFile = linkdir + '/bom-links-'    + releaseType + "-" + year
#outfile  = datadir + '/movie-charac-' + releaseType + "-" + year

for iYear in relevantYears:
    for iType in releaseType:
        linkFile = linkdir + '/bom-links-'    + iType + "-" + str(iYear)
        outfile  = datadir + '/movie-charac-' + iType + "-" + str(iYear)

        with open(linkFile) as f:
            df = pd.DataFrame()
            for row in csv.reader(f):
                currentURL = ''.join(row) # convert list to string
                print("scraping:", currentURL)
                df_movie = charac.process_movie(currentURL)
                if df_movie is not None:
                    df = df.append(df_movie, ignore_index=True)
                time.sleep(randint(5,15))

            df.to_csv(outfile + '.csv', index = False)
