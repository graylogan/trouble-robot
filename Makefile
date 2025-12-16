.PHONY: all clean
all: clean
	$(MAKE) -C simulated-control-panel

clean:
	cd ./main && black *.py
	cd ./main/game && black *.py