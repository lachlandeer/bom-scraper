# Add paths for this PROJECT_ROOT

#bash mkdir $(OUT)/s{1..50}

init:
	$(shell mkdir -p $(SRC)/lib)
	$(shell mkdir -p $(OUT)/links)
	$(shell mkdir -p $(SRC)/data)
