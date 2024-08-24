/*
 * Weather Monitoring Application with SPL06-007
 * Author: Halit Osman Efkere
 * Date: August 24, 2024
 *
 * Description: Reads temperature, pressure, and altitude from the SPL06-007 sensor
 * and sends the data to a Python GUI application for display.
 */

#include <SPL06-007.h>
#include <Wire.h>

// Declare global variables to store previous values
double prev_temp_c = 0.0;
double prev_pressure = 0.0;
double prev_altitude_m = 0.0;
double prev_altitude_ft = 0.0;

// Variables to store pressure trends
double pressure_trend = 0.0;
double last_pressure = 0.0;

void setup() {
  // Initialize I2C communication
  Wire.begin();
  
  // Initialize serial communication
  Serial.begin(115200);
  
  // Print initial message
  Serial.println("Goertek-SPL06-007 Environmental Monitoring and Weather Estimation");
  
  // Initialize the SPL06-007 sensor
  SPL_init(); // Assuming SPL_init() initializes the sensor with default settings
}

void loop() {
  // Read current sensor values
  double current_temp_c = get_temp_c();
  double current_pressure = get_pressure();
  double local_pressure = 1011.3; // Example local sea level pressure
  double current_altitude_m = get_altitude(current_pressure, local_pressure);
  double current_altitude_ft = get_altitude_f(current_pressure, local_pressure);

  // Calculate pressure trend
  pressure_trend = current_pressure - last_pressure;
  last_pressure = current_pressure;

  // Check if values have changed by more than 0.5 units
  if (abs(current_temp_c - prev_temp_c) >= 0.5 || abs(current_pressure - prev_pressure) >= 0.5 || 
      abs(current_altitude_m - prev_altitude_m) >= 0.5 || abs(current_altitude_ft - prev_altitude_ft) >= 0.5) {

    // Update previous values
    prev_temp_c = current_temp_c;
    prev_pressure = current_pressure;
    prev_altitude_m = current_altitude_m;
    prev_altitude_ft = current_altitude_ft;

    // Print updated values
    Serial.println("\nUpdated Values:");
    
    Serial.print("Temperature: ");
    Serial.print(current_temp_c);
    Serial.println(" C");

    Serial.print("Measured Air Pressure: ");
    Serial.print(current_pressure, 2);
    Serial.println(" mb");

    Serial.print("Local Airport Sea Level Pressure: ");
    Serial.print(local_pressure, 2);
    Serial.println(" mb");
    
    Serial.print("Altitude: ");
    Serial.print(current_altitude_m, 1);
    Serial.println(" m");

    Serial.print("Altitude: ");
    Serial.print(current_altitude_ft, 1);
    Serial.println(" ft");

    // Basic Weather Estimation
    if (pressure_trend > 0.5) {
      Serial.println("Weather Estimation: Improving weather conditions (Clear skies expected).");
    } else if (pressure_trend < -0.5) {
      Serial.println("Weather Estimation: Deteriorating weather conditions (Possible rain or storm).");
    } else {
      Serial.println("Weather Estimation: Stable conditions.");
    }
  }

  delay(2000); // Wait for 2 seconds before reading again
}
