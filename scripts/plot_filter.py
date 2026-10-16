"""Plot raw and EMA-filtered UV/IR readings for one lighting class.

Requires fresh CSV from firmware/data_collection_with_raw/data_collection_with_raw.ino:
time_ms,raw_uv,raw_ir,uv_sensor,IR_sensor,label
Usage:
python scripts/plot_filter.py --csv data/raw/new_samples.csv --label LED
"""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--output", default="outputs/filter_comparison.png")
    args = p.parse_args()
    df = pd.read_csv(args.csv)
    needed = {"time_ms", "raw_uv", "raw_ir", "uv_sensor", "IR_sensor", "label"}
    if not needed.issubset(df.columns):
        raise ValueError(f"CSV must contain {sorted(needed)}. The original filtered-only CSV cannot be used.")
    selected = df[df["label"] == args.label].head(250)
    if selected.empty:
        raise ValueError("No readings for that lighting class.")
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for axis, raw, filtered, title in zip(
            axes,
            ["raw_uv", "raw_ir"],
            ["uv_sensor", "IR_sensor"],
            ["UV (GUVA-S12SD)", "IR (TSL2591)"]):
        axis.plot(range(len(selected)), selected[raw].to_numpy(), label="Raw", alpha=0.55)
        axis.plot(range(len(selected)), selected[filtered].to_numpy(), label="EMA (alpha=0.2)")
        axis.set_ylabel(title)
        axis.legend()
    axes[-1].set_xlabel("Sample index")
    fig.suptitle("Raw vs EMA-filtered sensor signal: " + args.label)
    fig.tight_layout()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print("Saved", path)


if __name__ == "__main__":
    main()
