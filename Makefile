include config.mk
include init.mk
include initBoxOffice.mk

## getEverything:     : scrapes all information from Box Office Mojo
.PHONY: getEverything
getEverything: getAllBoxOffice getCharacteristics

## getAllBoxOffice    : scrapes all frequencies of box office
.PHONY: getAllBoxOffice
getAllBoxOffice: getDailyBoxOffice getWeekendBoxOffice getWeeklyBoxOffice

## getDailyBoxOffice  : scrapes daily box office
.PHONY: getDailyBoxOffice
getDailyBoxOffice: $(SRC_LIB)/processBoxOfficeReturns.py \
			initBoxOffice #getLinks
	python $(SRC_MAIN)/getBoxOffice.py 2014 2015 \
	 			$(OUT_LINKS) $(OUT_DATA_BO_DAILY) daily

## getWeekendBoxOffice: scrapes weekend box office
.PHONY: getWeekendBoxOffice
getWeekendBoxOffice: $(SRC_LIB)/processBoxOfficeReturns.py \
			initBoxOffice #getLinks
	python $(SRC_MAIN)/getBoxOffice.py 2014 2015 \
	 			$(OUT_LINKS) $(OUT_DATA_BO_WEEKEND) weekend

## getWeeklyBoxOffice : scrapes weekly box office
.PHONY: getWeeklyBoxOffice
getWeeklyBoxOffice: $(SRC_LIB)/processBoxOfficeReturns.py \
			initBoxOffice #getLinks
	python $(SRC_MAIN)/getBoxOffice.py 2014 2015 \
	 			$(OUT_LINKS) $(OUT_DATA_BO_WEEKLY) weekly

## getCharacteristics : scrapes the summary information from a movie's page
.PHONY: getCharacteristics
getCharacteristics: $(SRC_LIB)/processMovieCharacteristics.py \
					getLinks
	python $(SRC_MAIN)/getMovieCharacteristics.py $(YEAR_START) $(YEAR_END) \
	 			$(OUT_LINKS) $(OUT_DATA_CHARAC)

## getLinks           : scrapes weblinks to movie's pages by year and release type = [wide, limited]
.PHONY: getLinks
getLinks: $(SRC_LIB)/mojoScrapeLinks.py init
	python $(SRC_MAIN)/getLinks.py $(YEAR_START) $(YEAR_END) $(OUT_LINKS)

.PHONY: clean
clean:
	rm -rf ./out

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
