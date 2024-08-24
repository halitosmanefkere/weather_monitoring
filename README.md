# Weather Monitoring App with SPL06-007

This project provides a real-time weather monitoring application using the SPL06-007 sensor and an Arduino board. 
The sensor data (temperature, pressure, altitude) is read by the Arduino and sent over a serial connection to a Python GUI application, 
which displays the data in a dashboard format.

## Author

This project was created by **Halit Osman Efkere**.

## Features

- **Temperature Monitoring**: Real-time display of ambient temperature.
- **Pressure Monitoring**: Real-time display of atmospheric pressure.
- **Altitude Monitoring**: Calculate and display altitude based on pressure data.
- **Atmosphere Layer Detection**: Determine the atmospheric layer based on altitude.
- **Weather Estimation**: Basic weather estimation based on pressure trends.
- **Energy Efficient**: Designed with a dark theme for low energy consumption.

## Requirements

### Hardware

- Arduino board (e.g., Arduino Uno)
- SPL06-007 sensor module
- USB cable for Arduino

### Software

- Arduino IDE (for uploading code to the Arduino)
- Python 3.x
- PySerial (Python library for serial communication)
- Tkinter (Python standard GUI library)
- PyInstaller (for creating executable files)

## Sensor Connections

To connect the SPL06-007 sensor to the Arduino, use the following pin connections:

- **3.3V**: Connect to the 3.3V pin on the Arduino.
- **GND**: Connect to a GND pin on the Arduino.
- **SDA**: Connect to the SDA (A4 on most Arduino boards like Uno).
- **SCL**: Connect to the SCL (A5 on most Arduino boards like Uno).

Ensure that the connections are secure and that the sensor is oriented correctly.

## Installation

1. **Arduino Setup**:
   - Open the Arduino IDE and upload the `weather_monitoring.ino` file located in the `arduino_code` folder to your Arduino board.

2. **Python Environment**:
   - Install Python 3.x from [python.org](https://www.python.org).
   - Install the required Python libraries:
     ```bash
     pip install pyserial
     ```
   
3. **Run the Python Script**:
   - Run `weather_monitoring.py` located in the `python_code` folder to start the GUI application.

4. **Create Executable (Optional)**:
   - To create a standalone executable, run:
     ```bash
     pyinstaller --onefile --windowed weather_monitoring.py
     ```

## Usage

1. **Flash the Arduino with the Provided Code**:
   - Open the Arduino IDE on your computer.
   - Connect your Arduino board to your computer using a USB cable.
   - Open the `weather_monitoring.ino` file located in the `arduino_code` folder.
   - Select the correct board type and port under `Tools` in the Arduino IDE.
   - Click the **Upload** button to flash the Arduino with the code.

2. **Connect the SPL06-007 Sensor to the Arduino Using I2C**:
   - Ensure the SPL06-007 sensor is properly connected to the Arduino's I2C pins (SDA and SCL).

3. **Run the Arduino Code**:
   - Once the code is uploaded, the Arduino will start executing it immediately. 
   It will read data from the SPL06-007 sensor and send the data over the serial port to your computer.

4. **Run the Python Application**:
   - Open a terminal or command prompt in the `python_code` directory.
   - Run the Python script `weather_monitoring.py` to launch the GUI application.
   - The application will display the sensor data in real-time as it is received from the Arduino.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Arduino community for the inspiration and guidance.
- [PySerial](https://pyserial.readthedocs.io/) for serial communication support.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.
