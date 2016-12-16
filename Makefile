include config.mk
include init.mk


.PHONY: getCharacteristics
getCharacteristics:
	python $(SRC_MAIN)/getMovieCharacteristics.py $(YEAR_START) $(YEAR_END) \
	 			$(OUT_LINKS) $(OUT_DATA_CHARAC)

.PHONY: getLinks
getLinks: $(SRC_LIB)/mojoScrapeLinks.py
	python $(SRC_MAIN)/getLinks.py $(YEAR_START) $(YEAR_END) $(OUT_LINKS)

.PHONY: clean
clean:
	rm -rf ./out
