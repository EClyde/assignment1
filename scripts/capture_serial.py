"""Collect real data from the ESP32 by serial, retaining raw/filtered readings.

Example:
  python scripts/capture_serial.py --port COM4 --mode collect --output data/raw/new_samples.csv
  python scripts/capture_serial.py --port COM4 --mode inference --output outputs/device_predictions.csv

In collect mode, enter sun, shade, LED, fluorescent, or empty to pause, and
quit to stop. Serial lines beginning with # are ignored.
Student: Edryn Clyde Fernandez.
"""
import argparse
import csv
import threading
from pathlib import Path
import serial

LABELS = {"sun", "shade", "LED", "fluorescent"}
HEADERS = {
    "collect": ["time_ms", "raw_uv", "raw_ir", "uv_sensor", "IR_sensor", "label"],
    "inference": ["time_ms", "uv_sensor", "IR_sensor", "prediction", "lookup_us"],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", required=True, help="ESP32 COM port, e.g. COM4")
    p.add_argument("--mode", choices=["collect", "inference"], default="inference")
    p.add_argument("--output", default=None)
    args = p.parse_args()
    target = Path(args.output or (
        "data/raw/new_samples.csv" if args.mode == "collect"
        else "outputs/device_predictions.csv"))
    target.parent.mkdir(parents=True, exist_ok=True)
    header = HEADERS[args.mode]
    stopping = threading.Event()
    with serial.Serial(args.port, 115200, timeout=0.5) as port, target.open(
        "a", newline="", encoding="utf-8"
    ) as out:
        writer = csv.writer(out)
        if out.tell() == 0:
            writer.writerow(header)

        def user_input():
            if args.mode == "collect":
                print("Type sun, shade, LED, fluorescent to start, Enter to pause, quit to stop.")
                while not stopping.is_set():
                    try:
                        cmd = input("label> ").strip()
                    except EOFError:
                        break
                    if cmd.lower() == "quit":
                        stopping.set()
                        return
                    if not cmd or cmd in LABELS:
                        port.write(("L:" + cmd + "\n").encode())
                    else:
                        print("Allowed labels:", sorted(LABELS))
            else:
                print("Recording live classifications. Press Enter to stop.")
                try:
                    input()
                except EOFError:
                    pass
                stopping.set()

        threading.Thread(target=user_input, daemon=True).start()
        count = 0
        try:
            while not stopping.is_set():
                line = port.readline().decode(errors="replace").strip()
                if not line or line.startswith("#"):
                    continue
                fields = line.split(",")
                if len(fields) != len(header):
                    continue
                try:
                    [float(x) for x in fields[:5 if args.mode == "collect" else 3]]
                    if args.mode == "inference":
                        float(fields[-1])
                except ValueError:
                    continue
                if args.mode == "collect" and fields[-1] not in LABELS:
                    continue
                writer.writerow(fields)
                count += 1
                if count % 25 == 0:
                    out.flush()
                    print(f"{count} recorded to {target}")
        except KeyboardInterrupt:
            pass
        out.flush()
        print(f"Saved {count} rows to {target}")


if __name__ == "__main__":
    main()
