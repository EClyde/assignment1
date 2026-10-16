"""Compare a real ESP32 serial inference log to Python's identical uint8 lookup.
Student: Edryn Clyde Fernandez.

The ESP32 reports CSV rows with:
time_ms,uv_sensor,IR_sensor,prediction,lookup_us

Example:
python scripts/evaluate_device.py --csv outputs/device_predictions.csv
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def predict(filtered, tables, bounds, names, tau):
    transformed = np.log1p(np.maximum(filtered, 0))
    lo, hi = bounds[[0, 2]], bounds[[1, 3]]
    scaled = (transformed - lo) / (hi - lo)
    n = tables.shape[1]
    ij = np.clip(np.floor(scaled * n).astype(int), 0, n - 1)
    values = tables[:, ij[:, 1], ij[:, 0]].T
    selected = np.argmax(values, axis=1)
    return np.array([names[k] if values[i, k] / 255 >= tau else "UNKNOWN"
                     for i, k in enumerate(selected)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    args = parser.parse_args()
    if not Path(args.csv).exists():
        raise SystemExit("No actual ESP32 log at supplied CSV path.")
    frame = pd.read_csv(args.csv, comment="#")
    fields = ["uv_sensor", "IR_sensor", "prediction", "lookup_us"]
    if not set(fields).issubset(frame.columns) or frame.empty:
        raise ValueError(f"Expected nonempty device log with columns: {fields}")
    with np.load("outputs/surfaces.npz") as model:
        tables = model["tables"]
        bounds = model["bounds"]
        names = [str(x) for x in model["class_names"]]
        tau = float(model["reject_tau"])
    desktop = predict(frame[["uv_sensor", "IR_sensor"]].to_numpy(float),
                      tables, bounds, names, tau)
    device = frame["prediction"].astype(str).to_numpy()
    agreement = (desktop == device).mean()
    Path("outputs").mkdir(exist_ok=True)
    pd.crosstab(pd.Series(desktop, name="desktop"),
                pd.Series(device, name="ESP32")).to_csv("outputs/device_vs_desktop.csv")
    print(f"Desktop vs ESP32 agreement on {len(frame)} physical readings: {agreement:.2%}")
    print(f"Measured ESP32 lookup median: {frame.lookup_us.median():.1f} microseconds")
    print(f"Measured ESP32 lookup p95: {frame.lookup_us.quantile(.95):.1f} microseconds")


if __name__ == "__main__":
    main()
