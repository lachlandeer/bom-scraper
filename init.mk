# Add paths for sub directories for source and output

init:
	# createing src subdirectories
	$(shell mkdir -p $(SRC)/lib)
	$(shell mkdir -p $(SRC)/main)
	$(shell mkdir -p $(SRC)/scrape_specs)

	# out sub-directories
	$(shell mkdir -p $(OUT)/links)
	$(shell mkdir -p $(OUT)/data)
	$(shell mkdir -p $(OUT)/data/charac)

# declare sub directores
SRC_LIB  = $(SRC)/lib
SRC_MAIN = $(SRC)/main
SRC_SPEC = $(SRC)/scrape_specs

OUT_LINKS = $(OUT)/links
OUT_DATA  = $(OUT)/data

OUT_DATA_CHARAC  = $(OUT)/data/charac
