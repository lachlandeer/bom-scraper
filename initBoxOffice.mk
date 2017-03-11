SHELL=/bin/bash

# Add new paths for Box Office scraping

initBoxOffice:
	$(shell mkdir -p $(OUT)/data/boxoffice)
	$(shell mkdir -p $(OUT)/data/boxoffice/daily/{$(YEAR_START)..$(YEAR_END)})
	$(shell mkdir -p $(OUT)/data/boxoffice/weekly/{$(YEAR_START)..$(YEAR_END)})
	$(shell mkdir -p $(OUT)/data/boxoffice/weekend/{$(YEAR_START)..$(YEAR_END)})

OUT_DATA_BO_DAILY  = $(OUT)/data/boxoffice/daily
OUT_DATA_BO_WEEKLY  = $(OUT)/data/boxoffice/weekly
OUT_DATA_BO_WEEKEND  = $(OUT)/data/boxoffice/weekend
