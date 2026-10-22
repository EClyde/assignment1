# Project I — Assignment 1: On-Device Classification

**Student:** Edryn Clyde Fernandez

## Current status
The original labelled dataset has **2,400 existing sensor measurements** (600 per class: sun, shade, LED, fluorescent). Python training has successfully run on GitHub Actions and the output artifacts are committed:

- `outputs/dbscan_vs_ground_truth.csv`
- `outputs/heldout_confusion.csv`
- `outputs/surfaces.npz`
- `firmware/inference/model.h`

Automated training reported 4 DBSCAN clusters, 0 noise, 100% validation accuracy and 100% test accuracy on a **random split of the original recordings**. This is not independent new-session hardware validation; sequential time-series data can be correlated. The uint8 lookup table contains 4 × 16 × 16 = **1024 bytes**, plus **16 bytes** for scaling bounds. Actual flash and SRAM consumption have not been measured.

## Sensor setup
The project uses the student's two original sensor modules:
- GUVA-S12SD UV analog output to ESP32 **GPIO34**; V+ to 3.3V; GND to GND.
- Adafruit TSL2591 light sensor (IR channel) via I²C: **SDA GPIO21**, **SCL GPIO22**, GND to GND and appropriate module VIN.
- Install Arduino libraries **Adafruit TSL2591** and **Adafruit Unified Sensor**, and ESP32 board support.

**Assignment hardware difference:** The handout specifies a plain analog IR photodiode/phototransistor on GPIO35, not the I²C TSL2591. Verify the instructor accepts this substitution.

## Step 1: First ESP32 live test
Open `firmware/inference/inference.ino` in Arduino IDE. **Keep the generated `model.h` in the same inference directory.** Select your actual ESP32 board and serial port, compile and upload. Open Serial Monitor at **115200 baud**. The ESP32 prints:

`time_ms,uv_sensor,IR_sensor,prediction,lookup_us`

Class predictions are **sun, shade, LED, fluorescent, or UNKNOWN**. Test repeatable lighting conditions, including changing lighting while the device runs. Report any sensor saturation and compare results to the actual light source.

To collect a device CSV, close Arduino Serial Monitor so the port is free, and run:

```bash
python -m pip install -r requirements.txt
python scripts/capture_serial.py --port COM4 --mode inference --output outputs/device_predictions.csv
```
Press Enter to stop recording. Change COM4 to your actual serial port. Then run:

```bash
python scripts/evaluate_device.py --csv outputs/device_predictions.csv
```

This evaluates **real device predictions versus desktop table inference on the same UV/IR pairs**, and computes median/p95 on-device inference latency. Measure **flash and SRAM** using actual Arduino compile output, and compare with the predicted table + bounds. Record the board model, IDE/core/library versions.

## Step 2: Raw vs filtered evidence
The original CSV stores **already filtered readings only**, so there is no defensible raw-vs-filtered plot from that file. For the required plot, flash `firmware/data_collection_with_raw/data_collection_with_raw.ino` instead and run:

```bash
python scripts/capture_serial.py --port COM4 --mode collect --output data/raw/new_samples.csv
```

In the terminal, type a lighting class (`sun`, `shade`, `LED`, `fluorescent`), press Enter to start it, and use blank input to pause. To finish, type `quit`. Capture a representative run of 150+ readings per class and then generate:

```bash
python scripts/plot_filter.py --csv data/raw/new_samples.csv --label LED
```

This plots measured raw sensor readings alongside EMA-filtered measurements (alpha = 0.2). If collecting an entirely new labelled dataset, use **at least 500 readings per class**, and keep consistent sensor-to-source distance.

## Step 3: Reproducible desktop training
From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/train_model.py
python scripts/generate_model_header.py
```

The training flow performs DBSCAN on sensor values alone, fits per-cluster KDEs, selects bandwidth using validation labels, quantizes to uint8 lookup tables, evaluates the held-out test set, then generates `model.h`. Both Python and ESP32 apply **log1p** feature transforms using the model's training bounds. GitHub Actions also reruns training on source changes.

## Step 4: Complete the report and final submission
The assignment requires you to **revise the previous lab paper**; it should contain the real DBSCAN confusion table, held-out test agreement, fresh ESP32-vs-desktop agreement, raw vs EMA plot, measured flash/SRAM/latency versus prediction, limitations, wired prototype photo, and a **30–60 second demonstration video**. Commit the paper and evidence to this repository.

Only create the graded GitHub release tag (e.g. `v2.0`) after all evidence is committed. Do not invent hardware measurement results or mark the project fully complete before the on-device tests and report are finished.


## Proof-of-concept media

A photo of the physical ESP32 breadboard prototype was supplied and reviewed; see [photo/video evidence status](evidence/PHOTO_VIDEO_STATUS.md). The original JPEG still needs to be added to `evidence/IMG_2045.jpeg`, and the 30–60 second demonstration video has not yet been received. Recorded ESP32 classifications and the 702/702 desktop lookup agreement remain in `evidence/`.
