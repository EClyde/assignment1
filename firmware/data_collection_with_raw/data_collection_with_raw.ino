// Project I — Assignment 1
// Student: Edryn Clyde Fernandez
// GUVA-S12SD UV analog output -> ESP32 GPIO34
// TSL2591 IR only (I2C SDA=21, SCL=22)
// Includes raw and EMA-filtered values for the required filter plot.
// Serial CSV: time_ms,raw_uv,raw_ir,uv_sensor,IR_sensor,label
// Enter L:sun / L:shade / L:LED / L:fluorescent; L: to pause.
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2591.h>

Adafruit_TSL2591 tsl(2591);
const int UV_PIN = 34;
const float ALPHA = 0.2f;
const unsigned long SAMPLE_INTERVAL_MS = 100;
float uvEMA=0, irEMA=0;
bool ready=false;
String label="";
unsigned long previous=0;
unsigned long readings=0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(40);
  analogReadResolution(12);
  Wire.begin(21, 22);
  if (!tsl.begin()) {
    Serial.println("# ERROR: TSL2591 not found; check SDA/SCL.");
    while (true) delay(1000);
  }
  tsl.setGain(TSL2591_GAIN_MED);
  tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);
  Serial.println("# time_ms,raw_uv,raw_ir,uv_sensor,IR_sensor,label");
}
void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command.startsWith("L:")) {
      label = command.substring(2);
      label.trim();
      ready = false;
      readings = 0;
      Serial.println(label.length() ? "# Started " + label : "# Paused");
    }
  }
  if (millis() - previous < SAMPLE_INTERVAL_MS) return;
  previous = millis();
  int rawUV = analogRead(UV_PIN);
  uint32_t data = tsl.getFullLuminosity();
  uint16_t rawIR = uint16_t(data >> 16);
  uint16_t full = uint16_t(data & 0xffff);
  if (rawIR == 0xffff || full == 0xffff) {
    Serial.println("# WARNING: saturation detected, sample skipped");
    return;
  }
  if (!ready) {
    uvEMA = rawUV;
    irEMA = rawIR;
    ready = true;
  } else {
    uvEMA = ALPHA * rawUV + (1.0f - ALPHA) * uvEMA;
    irEMA = ALPHA * rawIR + (1.0f - ALPHA) * irEMA;
  }
  if (label.length() == 0) return;
  Serial.printf("%lu,%d,%u,%.3f,%.3f,%s\n", millis(), rawUV, rawIR,
                uvEMA, irEMA, label.c_str());
  if (++readings % 100 == 0) {
    Serial.printf("# %s: %lu samples\n", label.c_str(), readings);
  }
}
