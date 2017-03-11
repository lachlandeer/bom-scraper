# Scraping BoM

This repo contains scripts to get information from the BoM website.

Currently we scrape the following information:

* Main Movie Characteristics from the summary page
* Box Office at the daily, weekly and weekend frequencies from USA

## Ways to Execute

### Get Everything:

If you want all information run the following:

```bash
make getEverything
```

### Get Movie Characteristics:

```bash
make getCharacteristics
```

### Get All Box Office information
Collects all box office frequencies for US market
```bash
make getAllBoxOffice
```

### Get Daily Box Office information
Collects all box office frequencies for US market
```bash
make getDailyBoxOffice
```

### Get Weekly Box Office information
Collects all box office frequencies for US market
```bash
make getWeeklyBoxOffice
```

### Get Weekend Box Office information
Collects all box office frequencies for US market
```bash
make getWeekendBoxOffice
```

## To Do:

* Get Foreign Box Office by country - week 

## Other Info:

* Assumes that you have make installed on your machine - default for Unix system
* Tested using Python 3.5.2 (64bit)
