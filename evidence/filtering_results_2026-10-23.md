# Raw-versus-EMA filtering test — ESP32

**Student:** Edryn Clyde Fernandez

## Provenance and measurement

This report uses serial readings supplied directly by the student after uploading `data_collection_with_raw.ino`. The filter uses exponential moving average (EMA), alpha = 0.2, independently applied to the raw GUVA-S12SD UV ADC channel and the TSL2591 IR channel.

The user posted approximately **300 consecutive readings** from this run: **88 LED**, **94 fluorescent**, and **118 shade** (timestamps from 14007 ms through 50485 ms). The source paste was supplied as conversation text, not a committed raw log file. The repository CSV `evidence/filter_excerpts_2026-10-23.csv` contains **87 individually transcribed, directly recorded sample rows** (20 LED, 21 fluorescent and 46 shade); **do not describe this excerpt file as the complete 300-row recording**. All excerpt rows preserve the user's originally posted raw and filtered readings.

## Findings

- **UV:** The raw GUVA-S12SD value and filtered UV were **zero** for the recorded indoor lighting. This means the signal did not provide useful variation for evaluating smoothing under those test conditions; the untested sunlight class remains out of scope.
- **LED:** Raw TSL2591 IR was generally 2–3 counts in this segment. The filtered readings changed more gradually, illustrating suppression of one-count fluctuations.
- **Fluorescent:** Raw IR was generally 2–3 counts. At the beginning of the labelled interval it changed from 2 to 3, and the EMA responded with 2.000, 2.200, 2.360 and 2.488 counts. This is consistent with `EMA[n] = 0.2 × raw[n] + 0.8 × EMA[n−1]`.
- **Shade:** Raw IR increased from 1 to 7 and then 20–26 counts before decreasing. The filtered output rose slowly (for instance: at raw IR 20, filtered 6.114; at raw IR 24, filtered 9.691), visibly smoothing the step change but introducing lag.
- The reported sample interval in these excerpts was about **122 ms** (8.2 Hz). The firmware's `100 ms` constant is a minimum polling interval, not the measured completed conversion interval.

## Interpretation

The EMA filter successfully reduces immediate changes caused by sample-to-sample variations, but follows genuine lighting changes with lag. Lower alpha values emphasize smoothing; higher alpha values react more quickly but retain more short-term variation. This is the **filtering plot evidence**, not ground-truth classification accuracy, and the original trained classification model has not been changed.

The LED and fluorescent IR values **overlap heavily** in the new excerpts. These conditions were manually labelled at collection time. This log does not establish that the existing learned lookup table can distinguish them in this new geometry. The earlier actual classifier log remains separate in `evidence/device_test_2026-10-16.csv`.

## Reproduce the plots

Run `python scripts/plot_filter_excerpts.py` from the project root. Output files appear under `outputs/`: `led_filter_comparison.png`, `fluorescent_filter_comparison.png`, and `shade_filter_comparison.png`. The supplied example excerpts are sufficient to demonstrate filter behavior, while any assignment demand for full raw data may require separately exporting and committing the complete serial log.
