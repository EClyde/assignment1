# Project I — Assignment 1: On-Device Classification

**Student: Edryn Clyde Fernandez**

This repository contains the student's existing labelled light-sensor data and collection firmware, plus the initial DBSCAN → KDE → uint8 lookup pipeline and ESP32 inference sketch.

### Hardware
- GUVA-S12SD UV module output to ESP32 GPIO34 (ADC1)
- Adafruit TSL2591 module via I2C SDA GPIO21 / SCL GPIO22 (IR-only channel)

**Important:** The assignment specification names an analog IR photodiode on GPIO35, not the I2C TSL2591. Confirm instructor permission for this sensor substitution.

### Data
`data/raw/data_complete.csv` has 2,400 labelled rows, 600 each for shade, LED, fluorescent and sun, collected using the student's second GitHub account. The readings are EMA-filtered, not the unfiltered raw readings required for the filtering comparison figure.

### Train
```bash
pip install -r requirements.txt
python scripts/train_model.py
python scripts/generate_model_header.py
```
Requires numpy, pandas, scikit-learn. Training uses log1p on UV/IR readings before scaling, train-only DBSCAN, validation bandwidth selection, quantized 16×16 KDE tables, and held-out test split. The ESP32 applies the same log1p transformation to filtered readings.

### Firmware
Arduino IDE with ESP32 core + Adafruit TSL2591 + Adafruit Unified Sensor libraries. `firmware/data_collection/data_collection.ino` is the original data logger. `firmware/inference/inference.ino` depends on generated `model.h` placed in the same directory.

### Submission
See [REPORT_STATUS.md](REPORT_STATUS.md) for pending actual device evidence, missing raw-vs-filtered plot, updated prior lab paper, and the final tagged GitHub release.
