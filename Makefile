.PHONY: all
all:
	$(MAKE) -C simulated-control-panel
	cd ./main && black *.py
	cd ./main/game && black *.py