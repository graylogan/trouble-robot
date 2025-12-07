# Simulated Control Panel
This folder contains the simulated arduino and peripherals for the control panel.
## How to Run
1. Install Wokwi for VS Code using [these instructions](https://docs.wokwi.com/vscode/getting-started).
2. Install the Arduino CLI [here](https://arduino.github.io/arduino-cli/1.3/installation/)
3. Install the libraries in `requiments.txt`. This can be done using `$ arduino-cli lib install <lib name>` or in the Arduino IDE
4. Running `make` in the project directory will compile the control panel code before running the main python program
5. Run the simulator using the `Wokwi: Start Simulator` command in VS Code. This can also be done by opening `diagram.json` with Wokwi Diagram Editor

## Alternate method
If you don't want to compile the binary using arduino-cli and make, you can open the .ino file in the Arduino IDE and build the files using Sketch -> Export Compiled Binary