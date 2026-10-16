# Assignment 1 — Edryn Clyde Fernandez

## Current evidence
Existing labelled data: 2,400 samples (600 per lighting class: sun, shade, LED, fluorescent). Two sensors used: GUVA-S12SD UV (ADC GPIO34) and TSL2591 IR channel (I2C GPIO21/22). The assignment PDF explicitly specifies an **analog IR photodiode on GPIO35**, so the TSL2591 substitution needs instructor approval.

The original dataset contains **already filtered** sensor values. Raw-vs-filtered plot is not possible without collecting additional unfiltered samples. Do not fabricate it.

## To obtain final evidence
- Run `pip install -r requirements.txt`, `python scripts/train_model.py`, then `python scripts/generate_model_header.py`.
- Commit `outputs/surfaces.npz`, confusion tables, and generated `model.h`.
- Flash inference sketch and capture real serial output; compare against desktop.
- Document measured flash, SRAM, and time per query, alongside predicted table bytes = K*16*16 + 16.
- Take proof-of-concept photo and 30–60 second live demonstration video.
- Revise your previous lab **paper** with evidence, plots, methodology and limitations.
- Create release tag only on completed submission commit.

The code is a starting implementation and has not yet been hardware-validated.
