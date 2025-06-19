# XYZ Data Visualization

This project is a Python-based application for visualizing XYZ data from multiple sensors in real-time. It provides a graphical interface with 3D grid visualization, oscilloscope view, and sensor management capabilities.
This tool was created to help in the design of an educational Brain Health Test Dummy project for the Mac Parkman Foundation.

## Devices
- SparkFun OpenLog Artemis (without IMU)
- SparkFun Qwiic Cable Kit
- SparkFun Tripple Axis Accelerometer Breakout - KW134 (Qwiic)

## Features

- Real-time 3D visualization of XYZ data
- Oscilloscope view with adjustable thresholds
- Support for multiple sensors (up to 8 COM ports)
- Sensor management interface
- Switchable views: 3D Grid, Oscilloscope, and Sensor Management

## Requirements

- Python 3.x
- Pygame
- PySerial

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

```
pip install pygame pyserial
```

## Usage

Run the main script to start the application:

```
python display.py
```

## Components

The project consists of several Python files:

1. `display.py`: Main script that runs the application and handles the GUI.
2. `components.py`: Contains UI component classes used in the main display.
3. `grid3d.py`: Implements the 3D grid visualization.
4. `oscilloscope.py`: Implements the oscilloscope visualization.
5. `sensors_logic.py`: Handles sensor connections and data processing.

## How to Use

1. Connect your sensors to the COM ports.
2. Run the application.
3. Use the bottom menu to switch between different views:
   - Grid: Shows 3D visualization of XYZ data.
   - Oscilloscope: Displays magnitude of XYZ data over time.
   - Sensors: Allows you to manage and configure connected sensors.
4. In the Sensors view, you can:
   - Connect/disconnect sensors
   - Activate/deactivate sensors
   - Drag sensors between "External" and "Internal" columns
      - NOTE: Sensors must be classified as "External" or "Internal" to display data
5. In the Oscilloscope view, you can adjust green and yellow thresholds using the sliders on the right.

## Customization

You can modify the following parameters in the code:

- `MAX_SENSORS`: Change the maximum number of supported sensors (in `sensors_logic.py`).
- `BAUD_RATE`: Adjust the baud rate for serial communication (in `sensors_logic.py`).
- `scale`: Modify the scale of the 3D grid (in `grid3d.py`).
- `max_threshold_value`: Change the maximum value for oscilloscope thresholds (in `display.py`).

## Troubleshooting

If you encounter issues with sensor connections, ensure that:

1. The correct COM ports are being used.
2. The baud rate (default: 115200) matches your sensor's specifications.
3. You have the necessary permissions to access the COM ports.
4. Ensure the SparkFun OpenLog Artemis has the latest firmware.
   - Use the Artemis Firmware Upload GUI to flash the board
      (https://github.com/sparkfun/Artemis-Firmware-Upload-GUI)
   - Recommended firmware version: OpenLog_Artemis-V10-v29.bin
      (https://github.com/sparkfun/OpenLog_Artemis/blob/main/Binaries/OpenLog_Artemis-V10-v29.bin)
5. Confirm detection of the KX134 (Qwiic) accelerometer.
   - Power the board with the sensor connected via a Qwiic cable.
   - Use a serial terminal like PuTTY to connect at 115200 baud.
   - Press any key to open the configuration menu.

## Thanks
Thank you Dr. John Templeton, Ethan Sklar, Malique Gillings, Liam Maloney, Eamon Conners, Stephanie Carey, Nathan Schilaty, and Suzanne Lines for this opportunity!
