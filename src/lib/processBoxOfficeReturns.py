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

sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=10)
sess.mount('http://', adapter)

# First Information about dates
def extract_year(anchorString):
    '''
    Find the year the current data belongs to
    '''
    try:
        year=re.findall(r'20[0-9][0-9]', anchorString)[0]
        return year
    except:
        return None

def extract_calendarWeek(anchorString):
    '''
    Find the calendar week the current data belongs to
    '''
    try:
        calendarWeek=re.findall(r'wk\=(.[0-9]{1})', anchorString)[0]
        return calendarWeek
    except:
        pass
    try:
        calendarWeek=re.findall(r'wknd\=(.[0-9]{1})', anchorString)[0]
        return calendarWeek
    except:
        return None


def extract_date(anchorString):
    '''
    Find the start and end date of the Calendar Week
    '''
    try:
        date = re.findall(r'<b>(.+?)<', anchorString)[0]
        # clean out any badly parsed symbols
        date = re.sub('\x96', '-', date)
        return date
    except:
        return None

def find_dateInfo(anchorString):
    '''
    Returns all relevant date information contained in the Box Office mojo href string
    '''
    #obj = str(anchor)
    year=extract_year(anchorString)
    calendarWeek=extract_calendarWeek(anchorString)
    date=extract_date(anchorString)

    return year, calendarWeek, date

# Now Box Office Relevant information
def money_to_int(moneystring):
    '''
    A helper function to strip out dollar signs ($) and commas leaving any
    dollar value as a integer
    '''
    try:
        moneystring = moneystring.replace('$', '').replace(',', '')
        return int(moneystring)
    except:
        return moneystring

def get_weekly_movieRank(anchor):
    '''
    Return the Rank of the movie over a given time period.
    Rank compares a movie's Box Office takings to other movies currently in cinemas
    '''
    try:
        rank_tag = anchor.find_next("td")
        rank = rank_tag.get_text()
        return rank
    except:
        return None

def get_boxOffice(anchor):
    '''
    Return the Rank of the movie over a given week or weekend.
    '''
    try:
        boxOffice_tag = anchor.find_next("td").find_next("td")
        boxOffice = boxOffice_tag.get_text()
        boxOffice = money_to_int(boxOffice)
        return boxOffice
    except:
        return None

def get_theatres(anchor):
    '''
    Return the number of theatres the movie was showing in over a given
    week/weekend
    The data are always reported as constant over a week, using the
    weekend number as the number of theatres.
    '''
    try:
        theatres_tag = anchor.find_next("td").find_next("td").find_next("td").find_next("td")
        theatres = theatres_tag.get_text()
        theatres = int(theatres.replace(',' , ''))
        return theatres
    except:
        return None

def get_totalBoxOfficeToDate(anchor):
    '''
    Return the the total box office returns of a film upto (and including)
    that week/weekend
    '''
    try:
        totalBoxOffice_tag = anchor.find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").find_next("td")
        totalBoxOffice = totalBoxOffice_tag.get_text()
        totalBoxOffice = money_to_int(totalBoxOffice)
        return totalBoxOffice
    except:
        return None

def identify_longWeekend(df):
    '''
    Identifies long weekends by a leading <i> on the date column.
    Creates Dummy variable for long weekends, and then cleans up the date column
    and passes data frame back to user
    '''
    df['longWeekend'] = df.date.str.contains('<i>')
    df['date'] = df.date.str.replace('<i>', '')

    return df


def scrape_BoxOfficeInfo(href_pattern, soup, movie_id):
    '''
    Scrape the necessary Box Office information from the webpage
    '''
    df_movie = pd.DataFrame()

    for iAnchor in soup.findAll('a', href=href_pattern):

        ## convert to string for regular expression parsing
        anchorString = str(iAnchor)

        ## Get date information from stripping info from inside the href link
        year, calendarWeek, date = find_dateInfo(anchorString)

        ## Get Box Office Information etc
        rank = get_weekly_movieRank(iAnchor)
        boxOffice = get_boxOffice(iAnchor)
        theatres = get_theatres(iAnchor)
        grossBoxOffice = get_totalBoxOfficeToDate(iAnchor)


        ## Put data into a weekly data-frame
        df_week = pd.DataFrame([[movie_id, year, calendarWeek, date,
                                  rank, boxOffice, theatres, grossBoxOffice
                             ]]
                            )
        ## append that week to existing data
        df_movie = df_movie.append(df_week, ignore_index=True)

        ## end for loop

    # label the columns
    if not df_movie.empty:
        df_movie.columns = ["movie_id", "year", "calendarWeek", "date", "rank",
                            "boxOffice", "theatres", "grossBoxOffice"]

        return df_movie
    else:
        pass

def scrape_dailyBoxOfficeInfo(href_pattern, soup, movie_id):
    '''
    Scrape the necessary daily Box Office information from the webpage.
    Daily Box Office returns are stored in a different pattern than weekly and
    weekend returns, so need a separate scraper
    '''
    df_movie = pd.DataFrame()

    for iAnchor in soup.findAll('a', href=href_pattern):

        ## convert to string for regular expression parsing
        anchorString = str(iAnchor)

        # date Information
        try:
            year=re.findall(r'20[0-9][0-9]', anchorString)[0]
        except:
            year = None

        try:
            date = re.findall(r'<b>(.+?)<', anchorString)[0]
            date = re.sub('\x96', '-', date)
        except:
            date = None

        # Get Box Office Information etc
        try:
            rank_tag = iAnchor.find_next("td")
            rank = rank_tag.get_text()
        except:
            rank = None

        # here is box office
        try:
            boxOffice_tag = rank_tag.find_next("td")
            boxOffice = boxOffice_tag.get_text()
            boxOffice = money_to_int(boxOffice)
        except:
            boxOffice = None

        # find theatres
        try:
            theatres_tag = boxOffice_tag.find_next("td").find_next("td").find_next("td").contents[0]
            theatres = theatres_tag.get_text()
            theatres = int(theatres.replace(',' , ''))
        except:
            theatres = None

        # find gross to date
        try:
            grossBO_tag = theatres_tag.find_next("td").find_next("td").contents[0]
            grossBoxOffice = grossBO_tag.get_text()
            grossBoxOffice = money_to_int(grossBoxOffice)
        except:
            grossBoxOffice = None

        # get day of release
        try:
            dayOfRelease_tag = grossBO_tag.find_next("td").contents[0]
            dayOfRelease     = dayOfRelease_tag.get_text()
        except:
            dayOfRelease = None

        # package it up
        df_week = pd.DataFrame([[movie_id, year, date,
                                  rank, boxOffice, theatres, grossBoxOffice, dayOfRelease
                             ]]
                            )
        df_movie = df_movie.append(df_week, ignore_index=True)

    ## label the columns
    if not df_movie.empty:
        df_movie.columns = ["movie_id", "year", "date", "rank", "boxOffice",
                            "theatres", "grossBoxOffice", "dayOfRelease"]
        return df_movie
    else:
        pass

def process_weekendBoxOffice(currentURL):
    '''
    Takes a URL to a movie website on Box Office Mojo and collects weekend
    Box Office information.
    '''
    href_pattern = re.compile('^/weekend/chart/\?yr')

    # Get the movie ID and direct to the page storing weekend Box Office takings
    movie_id = currentURL.rsplit('=', 1)[-1].rsplit('.', 1)[0]
    print('Getting Weekend Box Office for', movie_id)
    boxOffice_url = 'http://www.boxofficemojo.com/movies/?page=weekend&id=' + movie_id + '.htm'

    response = sess.get(boxOffice_url)

    if response.status_code != 200:
        return None

    page = response.text
    soup = BeautifulSoup(page,"lxml")

    df_movie = scrape_BoxOfficeInfo(href_pattern, soup, movie_id)

    # clean up long weekend information
    if df_movie is not None:
        df_movie = identify_longWeekend(df_movie)
    else:
        pass

    return movie_id, df_movie

def process_weeklyBoxOffice(currentURL):
    '''
    Takes a URL to a movie website on Box Office Mojo and collects weekly
    Box Office information.
    '''
    href_pattern = re.compile('^/weekly/chart/')

    # Get the movie ID and direct to the page storing weekend Box Office takings
    movie_id = currentURL.rsplit('=', 1)[-1].rsplit('.', 1)[0]
    print('Getting Weekly Box Office for', movie_id)
    boxOffice_url = 'http://www.boxofficemojo.com/movies/?page=weekly&id=' + movie_id + '.htm'

    response = sess.get(boxOffice_url)

    if response.status_code != 200:
        return None

    page = response.text
    soup = BeautifulSoup(page,"lxml")

    df_movie = scrape_BoxOfficeInfo(href_pattern, soup, movie_id)

    return movie_id, df_movie

def process_dailyBoxOffice(currentURL):
    '''
    Takes a URL to a movie website on Box Office Mojo and collects daily
    Box Office information.
    '''
    href_pattern = re.compile('^/daily/chart/\?sortdate=')

    # Get the movie ID and direct to the page storing weekend Box Office takings
    movie_id = currentURL.rsplit('=', 1)[-1].rsplit('.', 1)[0]
    print('Getting Daily Box Office for', movie_id)
    boxOffice_url = 'http://www.boxofficemojo.com/movies/?page=daily&view=chart&id=' + movie_id + '.htm'

    response = sess.get(boxOffice_url)

    if response.status_code != 200:
        return None

    page = response.text
    soup = BeautifulSoup(page,"lxml")

    df_movie = scrape_dailyBoxOfficeInfo(href_pattern, soup, movie_id)

    return movie_id, df_movie
