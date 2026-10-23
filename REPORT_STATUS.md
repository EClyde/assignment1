# Assignment 1 — Edryn Clyde Fernandez

## Current evidence
Existing labelled data: 2,400 samples (600 per lighting class: sun, shade, LED, fluorescent). Two sensors used: GUVA-S12SD UV (ADC GPIO34) and TSL2591 IR channel (I2C GPIO21/22). The assignment PDF explicitly specifies an **analog IR photodiode on GPIO35**, so the TSL2591 substitution needs instructor approval.

The original dataset contains **already filtered** sensor values. Raw-vs-filtered plot is not possible without collecting additional unfiltered samples. Do not fabricate it.

## To obtain final evidence
- [x] Train and generate model via GitHub Actions; actual files are committed.
- [x] Commit `outputs/surfaces.npz`, confusion tables, and generated `model.h`.
- [x] Flash inference sketch and capture real serial output; 702/702 device predictions matched desktop lookup (not independent true-label accuracy).
- [x] Document measured flash, SRAM, and time per query, alongside predicted table bytes = K*16*16 + 16. See evidence/esp32_memory_measurements_2026-10-23.md (flash 308,028 bytes, global SRAM 23,724 bytes) and evidence/device_test_2026-10-16_summary.md (measured lookup times).
- [x] Receive physical prototype photograph and video; the student's final video is 25 seconds, which is short of the stated 30–60 second requirement. Media themselves still need an accessible upload/link.
- Revise your previous lab **paper** with evidence, plots, methodology and limitations.
- Create release tag only on completed submission commit.

The ESP32 has been physically tested for live inference; available UV/IR readings were replayed through the desktop lookup with 702/702 matching predictions. Sunlight has not been tested and the existing dataset's random-split 100% test score is not evidence of new-session generalization. Raw-vs-filtered plot, prior paper revision, and final release remain pending.
