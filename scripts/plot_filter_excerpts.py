"""Replot the actual raw-vs-EMA excerpts from the physical ESP32 logging session.

Run from the assignment repository root:
  python scripts/plot_filter_excerpts.py
Requires matplotlib and pandas (see requirements.txt).
Plots include selected original records, not the full approximately 300-line paste.
Student: Edryn Clyde Fernandez.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

source = Path("evidence/filter_excerpts_2026-10-23.csv")
df = pd.read_csv(source)
dest = Path("outputs")
dest.mkdir(exist_ok=True)
for label in ["LED", "fluorescent", "shade"]:
    section = df[df.label == label].copy()
    if section.empty:
        raise ValueError("Missing data for " + label)
    t = (section.time_ms - section.time_ms.iloc[0]) / 1000.0
    fig, ax = plt.subplots(figsize=(9.4,4.8))
    ax.step(t, section.raw_ir, where="mid", alpha=0.74,
            label="Raw IR (TSL2591)")
    ax.plot(t, section.IR_sensor, linewidth=2.4,
            label="EMA IR (alpha = 0.2)")
    ax.set_xlabel("Time within excerpt (seconds)")
    ax.set_ylabel("IR sensor counts")
    ax.set_title(label.capitalize() + ": raw vs filtered IR (measured subset)")
    ax.grid(alpha=0.22)
    ax.legend()
    fig.tight_layout()
    output = dest / (label.lower() + "_filter_comparison.png")
    fig.savefig(output, dpi=170)
    plt.close(fig)
    print("Saved", output)
