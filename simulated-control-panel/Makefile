ARDUINO_CLI ?= arduino-cli
BOARD ?= arduino:avr:uno
INO := simulated-control-panel.ino
SKETCH := $(basename $(INO))
BUILD_DIR := build

.PHONY: all compile clean rebuild

all: compile

compile: $(INO)
	clang-format -i *.ino
	@echo "Compiling $(INO) for $(BOARD)..."
	@$(ARDUINO_CLI) compile -b $(BOARD) -e $(INO)

rebuild: clean compile

clean:
	@echo "Removing build directory $(BUILD_DIR)"
	@rm -rf $(BUILD_DIR)