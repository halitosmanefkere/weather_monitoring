"""
Weather Monitoring Application with SPL06-007
Author: Halit Osman Efkere
Date: August 24, 2024

Description: This Python GUI application reads data from an Arduino connected to an SPL06-007 sensor
via serial port and displays the temperature, pressure, and altitude in a user-friendly interface.
"""

import sys
import serial
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

class WeatherApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("SPL06-007 Weather Monitoring Dashboard")
        self.geometry("600x400")
        self.configure(bg='black')

        # Initialize serial port
        self.serial_port = self.connect_serial()

        # Create a frame for dashboard layout
        self.create_dashboard()

        # Start a thread to read data from the serial port
        self.serial_thread = Thread(target=self.read_serial_data)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def create_dashboard(self):
        """Create and arrange widgets for the GUI in a dashboard layout."""
        style = ttk.Style(self)
        style.configure('TLabel', background='black', foreground='white', font=('Arial', 14), padding=10)
        style.configure('TFrame', background='black')

        # Create frames for each sensor data category
        temp_frame = ttk.Frame(self, style='TFrame')
        temp_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        pressure_frame = ttk.Frame(self, style='TFrame')
        pressure_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        sea_level_pressure_frame = ttk.Frame(self, style='TFrame')
        sea_level_pressure_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        altitude_frame = ttk.Frame(self, style='TFrame')
        altitude_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        atmosphere_layer_frame = ttk.Frame(self, style='TFrame')
        atmosphere_layer_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        weather_estimation_frame = ttk.Frame(self, style='TFrame')
        weather_estimation_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

        pressure_condition_frame = ttk.Frame(self, style='TFrame')
        pressure_condition_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Create labels inside each frame
        self.temp_label = ttk.Label(temp_frame, text="Temperature: N/A", style='TLabel')
        self.temp_label.pack()

        self.pressure_label = ttk.Label(pressure_frame, text="Pressure: N/A", style='TLabel')
        self.pressure_label.pack()

        self.sea_level_pressure_label = ttk.Label(sea_level_pressure_frame, text="Sea Level Pressure: N/A", style='TLabel')
        self.sea_level_pressure_label.pack()

        self.altitude_label = ttk.Label(altitude_frame, text="Altitude: N/A", style='TLabel')
        self.altitude_label.pack()

        self.atmosphere_layer_label = ttk.Label(atmosphere_layer_frame, text="Atmosphere Layer: N/A", style='TLabel')
        self.atmosphere_layer_label.pack()

        self.weather_estimation_label = ttk.Label(weather_estimation_frame, text="Weather Estimation: N/A", style='TLabel')
        self.weather_estimation_label.pack()

        self.pressure_condition_label = ttk.Label(pressure_condition_frame, text="Pressure Condition: N/A", style='TLabel')
        self.pressure_condition_label.pack()

    def connect_serial(self):
        """Attempt to connect to the serial port."""
        attempts = 3
        for i in range(attempts):
            try:
                # Replace 'COM6' with your actual Arduino COM port
                print(f"Attempting to connect to serial port (Attempt {i + 1})...")
                return serial.Serial('COM6', 115200, timeout=1)
            except serial.SerialException as e:
                print(f"Error connecting to serial port: {e}")
                if i < attempts - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    print("Failed to connect after multiple attempts.")
                    return None
            except PermissionError as e:
                print(f"Permission error: {e}")
                if i < attempts - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    print("Failed to connect due to permission issues.")
                    return None

    def read_serial_data(self):
        """Read serial data from Arduino."""
        while True:
            if self.serial_port and self.serial_port.is_open:
                try:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    self.update_display(line)
                    time.sleep(2)  # Update every 2 seconds
                except serial.SerialException as e:
                    print(f"Serial error: {e}")
                except UnicodeDecodeError as e:
                    print(f"Decoding error: {e}")

    def update_display(self, line):
        """Update the GUI display with sensor data."""
        if "Temperature:" in line:
            self.temp_label.config(text=line)
        elif "Pressure:" in line and "Sea Level" not in line:
            self.pressure_label.config(text=line)
            self.update_pressure_condition(float(line.split(":")[1].strip().split()[0]))
        elif "Sea Level Pressure:" in line:
            self.sea_level_pressure_label.config(text=line)
        elif "Altitude:" in line and "ft" not in line:
            self.altitude_label.config(text=line)
            self.update_atmosphere_layer(float(line.split(":")[1].strip().split()[0]))
        elif "Weather Estimation:" in line:
            self.weather_estimation_label.config(text=line)

    def update_atmosphere_layer(self, altitude):
        """Determine the atmospheric layer based on altitude."""
        if altitude < 11000:
            self.atmosphere_layer_label.config(text="Atmosphere Layer: Troposphere")
        elif 11000 <= altitude < 25000:
            self.atmosphere_layer_label.config(text="Atmosphere Layer: Lower Stratosphere")
        elif 25000 <= altitude < 50000:
            self.atmosphere_layer_label.config(text="Atmosphere Layer: Mid Stratosphere")
        elif 50000 <= altitude < 85000:
            self.atmosphere_layer_label.config(text="Atmosphere Layer: Mesosphere")
        else:
            self.atmosphere_layer_label.config(text="Atmosphere Layer: Thermosphere")

    def update_pressure_condition(self, pressure):
        """Update the pressure condition label based on the pressure value."""
        if pressure > 1013.25:
            self.pressure_condition_label.config(text="Pressure Condition: High (Clear skies expected)", foreground="green")
        elif pressure < 1000.0:
            self.pressure_condition_label.config(text="Pressure Condition: Low (Possible storm)", foreground="red")
        else:
            self.pressure_condition_label.config(text="Pressure Condition: Normal (Stable conditions)", foreground="orange")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
