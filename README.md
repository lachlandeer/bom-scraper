# Scraping BoM

This repo contains scripts to get information from the BoM website.

Currently we only harvest the links we are looking to get data from.

Run script to get all links using

```bash
make getLinks
```

**TO DO:**

1. Use the links to get the summary data on movies
2. Use links to get box office data

**Currently Working On:** scraping the summary data

* *have* written the functions to collect the data
* *have not* written a script that runs the scraper on against the csvs that contain
 the links

Assumes that you have make installed on your machine.
