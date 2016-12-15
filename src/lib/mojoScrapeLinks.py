def harvestMovieLinks(candidateURL, iYear, iType, pattern):
    from bs4 import BeautifulSoup as bs
    import urllib.request

    # scrape:
    links = []

    soup = bs(urllib.request.urlopen(candidateURL).read(), "lxml")
    allTables = soup.findChildren('table')

    linksTable = allTables[6]

    nEntries = 0

    for link in linksTable.find_all('a', href=pattern):
        links.append("http://www.boxofficemojo.com" + link['href'])
        nEntries +=1


    return links

def writeLinksToCSV(iYear, iType, movieLinks, datadir):
    import csv
    print('All links found, writing csv with', len(movieLinks),  ' links...')


    # Write the csv file here
    csvBaseName = datadir + "bom-links-" + iType
    csvfile = csvBaseName + "-" + str(iYear)

    # Assuming a flat list
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for iFullLink in movieLinks:
            writer.writerow([iFullLink])

    print('Saved to', csvfile, '...Done!')
    return

def scrapeLinks(typeString, iYear, iType, datadir):
    import re
    import os
    import time
    from random import randint

    # starting point for search, can be any year
    baseURL="http://www.boxofficemojo.com/yearly/chart/"

    ## wide releases need to obey the structure
    # http://www.boxofficemojo.com/yearly/chart/?page=1&view=widedate&view2=domestic&yr=2016&p=.htm

    ## limited need to obey
    ## http://www.boxofficemojo.com/yearly/chart/?view=limited&view2=domestic&page=1&yr=2016&p=.htm

    # pattern to search for
    pattern = re.compile("/movies")

    # initialize as an empty list
    movieLinks=[]

    for iPageNum in range(1,10):
        candidateURL = baseURL + '?page=' + str(iPageNum) + '&view=' + typeString + '&view2=domestic&yr=' + str(iYear) + '&p=.htm'
        print('point to:', candidateURL)

        try:
            newMovieLinks = harvestMovieLinks(candidateURL, iYear, iType, pattern)
            movieLinks.extend(newMovieLinks)
            time.sleep(randint(5,15))

        except IndexError:
            pass
            print("there is not a page", iPageNum)

        continue

    writeLinksToCSV(iYear, iType, movieLinks, datadir)
