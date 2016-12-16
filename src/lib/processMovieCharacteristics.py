"""
This collection of functions scrapes most of the important data about movie
observable characteristics from the film's summary page on Box Office Mojo.

Last Run: December, 2016
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

## functions

def get_movie_value(soup, field_name):
    '''Grab a value from boxofficemojo HTML

    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    '''
    obj = soup.find(text=re.compile(field_name))
    if not obj:
        return None
    # this works for most of the values
    next_sibling = obj.findNextSibling()
    if next_sibling:
        return next_sibling.text #.encode('ascii','ignore')
    else:
        return None

def get_movie_title(soup):
    '''
    Get the movie's title from the header table
    '''
    obj = soup.find('title')
    if not obj:
        return None
    # this works for most of the values
    try:
        name = "(".join(obj.text.split('(')[:-1]).strip()
        if name == "":
            name = "".join(obj.text.split('-')[:-1]).strip()
        return name #.encode('ascii','ignore')
    except:
        return None

def get_theaters(soup):
    '''
    Grabs the largest number of theatres that a film was shown over a release cycle
    '''
    nonBreakSpace = u'\xa0'
    obj = soup.find(text=re.compile('Widest'+nonBreakSpace+'Release:'))
    if not obj:
        return None
    next_obj = obj.findNext('td')
    if next_obj.contents[0]:
        return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
    else:
        return None

def get_close(soup):
    '''
    Grabs the last date that the movie was shown in cinemas
    '''
    nonBreakSpace = u'\xa0'
    obj = soup.find(text=re.compile('Close'+nonBreakSpace+'Date:'))
    if not obj:
        return None
    next_obj = obj.findNext('td')
    if next_obj.contents[0]:
        return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
    else:
        return None

def get_inrelease(soup):
    '''
    Grabs the number of days a film was in release
    '''
    #nonBreakSpace = u'\xa0'
    obj = soup.find(text=re.compile('In Release:'))
    if not obj:
        return None
    next_obj = obj.findNext('td')
    if next_obj.contents[0]:
        return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
    else:
        return None


def get_foreigntotal(soup):
    '''
    Grabs the foreign earnings of the film aggregated across markets outside the USA
    '''
    nonBreakSpace = u'\xa0'
    obj = soup.find(text=re.compile('Foreign:'))
    if not obj:
        return None
    next_obj = obj.findNext('td')
    if next_obj.contents[0]:
        return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
    else:
        return None

def get_openingweekend(soup):
    '''
    Grabs the opening weekend box office for a film that was released straight
    to "wide release"
    '''
    try:
        nonBreakSpace = u'\xa0'
        obj = soup.find(text=re.compile('Opening'+nonBreakSpace+'Weekend:'))
        if not obj:
            return None
        next_obj = obj.findNext('td')
        if next_obj.contents[0]:
            return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
        else:
            return None
    except:
        return None

def get_openingweekend_limited(soup):
    '''
    For a film that was first released in limited theatres, gets the opening
    weekend box office of the limited release phase
    '''
    try:
        nonBreakSpace = u'\xa0'
        obj = soup.find(text=re.compile('Limited'+nonBreakSpace+'Opening'+nonBreakSpace+'Weekend:'))
        if not obj:
            return None
        next_obj = obj.findNext('b')
        if next_obj.contents[0]:
            return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
        else:
            return None
    except:
        return None

def get_openingweekend_wide(soup):
    '''
    For a film that was first released in limited theatres, gets the opening
    weekend box office of the wide release phase
    '''
    try:
        nonBreakSpace = u'\xa0'
        obj = soup.find(text=re.compile('Wide'+nonBreakSpace+'Opening'+nonBreakSpace+'Weekend:'))
        if not obj:
            return None
        next_obj = obj.findNext('td')
        if next_obj.contents[0]:
            return next_obj.contents[0].strip().split()[0] #.encode('ascii','ignore')
        else:
            return None
    except:
        return None

def get_all_players(soup, field_name_list):
    '''
    Will return a string containing a list of people who were in a certain role
    within the movie production.

    Currently works for: director, producer, actor, writer, cinematographer
                         composer
    '''
    for item in set(field_name_list):
        my_text = soup.find(text=item)
        if my_text:
            my_td = my_text.findNext('td').getText(separator=u',') #.encode('ascii','ignore')
            return my_td
    return None

def to_date(datestring):
    '''
    A helper function than transforms a date string into a "proper date format"
    '''
    try:
        date = dateutil.parser.parse(datestring)
        return date
    except:
        return datestring

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

def runtime_to_minutes(runtimestring):
    '''
    A helper function that converts the run time of movies posted as hours and
    minutes into minutes
    '''
    try:
        runtime = runtimestring.split()
        try:
            minutes = int(runtime[0])*60 + int(runtime[2])
            return minutes
        except:
            return None
    except:
        return runtimestring

def process_movie(url):
    '''
    Takes a URL to a movie website on Box Office Mojo and collects all the
    relevant observable characteristics from the summary page.
    '''
    headers = ['movie_id','movie_title',
                'domestic_total_gross', 'foreign_total_gross', 'opening_weekend',
                'opening_weekend_limited', 'opening_weekend_wide',
                'release_date', 'close_date' , 'in_release_days' ,
                'runtime_mins',
                'rating', 'genre', 'distributor', 'director', 'producer',
                'production_budget', 'widest_release_theaters',
                'actors', 'writers', 'cinematographers', 'composers'
              ]
    response = sess.get(url)

    if response.status_code != 200:
        return None

    page = response.text
    soup = BeautifulSoup(page,"lxml")

    ## --- Create a movie ID from the URL and get the title
    movie_id = url.rsplit('=', 1)[-1].rsplit('.', 1)[0]
    movie_title = get_movie_title(soup)

    ## --- Date Specific
    raw_release_date = get_movie_value(soup,'Release Date')
    release_date     = to_date(raw_release_date)

    raw_close_date   = get_close(soup)
    close_date       = to_date(raw_close_date)

    in_release       = get_inrelease(soup)

    ## --- Box Office
    raw_domestic_total_gross = get_movie_value(soup,'Domestic Total')
    domestic_total_gross     = money_to_int(raw_domestic_total_gross)

    raw_foreign_total_gross  = get_foreigntotal(soup)
    foreign_total_gross      = money_to_int(raw_foreign_total_gross)

    raw_domestic_opening_weekend    = get_openingweekend(soup)
    domestic_opening_weekend        = money_to_int(raw_domestic_opening_weekend)

    raw_domestic_opening_weekend_limited = get_openingweekend_limited(soup)
    domestic_opening_weekend_limited     = money_to_int(raw_domestic_opening_weekend_limited)

    raw_domestic_opening_weekend_wide    = get_openingweekend_wide(soup)
    domestic_opening_weekend_wide        = money_to_int(raw_domestic_opening_weekend_wide)

    ## -- remaining characteristics
    raw_runtime             = get_movie_value(soup,'Runtime')
    runtime                 = runtime_to_minutes(raw_runtime)
    rating                  = get_movie_value(soup,'MPAA Rating')
    genre                   = get_movie_value(soup,'Genre: ')
    distributor             = get_movie_value(soup,'Distributor: ')
    production_budget       = get_movie_value(soup, 'Production Budget: ')
    widest_release_theaters = get_theaters(soup)

    ## --- People involved in the movie
    director         = get_all_players(soup,['Director:','Director'])
    producer         = get_all_players(soup,['Producer:','Producers:',
                                                'Producer','Producers'])
    actors           = get_all_players(soup,['Actor:','Actors:','Actor','Actors'])
    writers          = get_all_players(soup,['Writer:','Writers:',
                                                'Screenwriter:','Screenwriters:',
                                                'Writer','Writers',
                                                'Screenwriter','Screenwriters'])
    cinematographers = get_all_players(soup, ['Cinematographer:','Cinematographer',
                                              'Cinematographers:','Cinematographers'])
    composers        = get_all_players(soup, ['Composer:','Composers:',
                                                'Composer','Composers'])


    ## --- Put the data collected into a pandas dataframe
    df_movie = pd.DataFrame([[movie_id, movie_title,
                                domestic_total_gross,  foreign_total_gross,
                                domestic_opening_weekend, domestic_opening_weekend_limited,
                                domestic_opening_weekend_wide,
                                release_date, close_date, in_release, runtime,
                                rating, genre, distributor, director, producer,
                                production_budget, widest_release_theaters,
                                actors, writers, cinematographers, composers
                             ]],
                            columns=headers)

    # return a line of data to the object assigned
    return df_movie
