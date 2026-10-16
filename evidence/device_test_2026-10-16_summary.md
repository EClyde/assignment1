# ESP32 live light-classification test — 2026-10-16

Student: Edryn Clyde Fernandez

Source: User-supplied ESP32 serial output. The raw paste included one garbled startup line, omitted from the clean CSV.

- Valid inference lines: 702
- Predicted labels (not accuracy): LED 146, fluorescent 240, shade 68, UNKNOWN 248, sun 0
- Recording span: 85.507 s, timestamps 1319 to 86826 ms
- Sample cadence: 8.20 Hz
- Reported filtered UV: 0.000 for all readings; sunlight not tested.
- Reported IR range: 14.402 to 11612.856
- On-device lookup: 8 to 17 microseconds; median 10 microseconds, p95 13 microseconds.
- UNKNOWN is allowed. Existing classifier, model, and rejection threshold were not modified.
- Class labels are classifier output, not independently labelled test ground truth.
- Pending: sun test, paired desktop-vs-device agreement, Arduino flash/SRAM, raw-vs-EMA plot, board photo/video, and revision of original report.

## Desktop versus on-device agreement

The 702 physical ESP32 records were replayed through a desktop implementation using the **same committed model.h** lookup table, log1p scaling, grid-cell clipping, class order, and REJECT_TAU. All **702/702** predicted classes matched (100% agreement), including UNKNOWN. This is an on-device-versus-desktop implementation parity check on shared input values, **not** 100% true-label classification accuracy on independently labelled lighting conditions.
