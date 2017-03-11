include config.mk
include init.mk
include initBoxOffice.mk

## getBoxOffice: scrapes daily box office
.PHONY: getDailyBoxOffice
getDailyBoxOffice: $(SRC_LIB)/processBoxOfficeReturns.py \
			initBoxOffice #getLinks
	python $(SRC_MAIN)/getBoxOffice.py 2014 2015 \
	 			$(OUT_LINKS) $(OUT_DATA_BO_DAILY) daily

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
