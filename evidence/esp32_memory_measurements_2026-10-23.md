# Measured ESP32 build memory — Assignment 1

**Student:** Edryn Clyde Fernandez

## Original Arduino IDE compilation output

```text
Sketch uses 308028 bytes (23%) of program storage space. Maximum is 1310720 bytes.
Global variables use 23724 bytes (7%) of dynamic memory, leaving 303956 bytes for local variables. Maximum is 327680 bytes.
```

## Predicted model storage versus actual compiled firmware

| Metric | Bytes | Source/meaning |
|---|---:|---|
| Quantized KDE table | 1,024 | Four 16 × 16 uint8 lookup tables, stored in PROGMEM |
| Scaling bounds | 16 | Four float32 numbers |
| **Predicted principal model data** | **1,040** | Table plus scaling bounds; excludes class names and program code |
| **Actual sketch flash usage** | **308,028** | Arduino IDE compiler output (23% of 1,310,720-byte app partition) |
| **Actual global SRAM usage** | **23,724** | Arduino IDE compiler output (7% of 327,680 bytes) |
| Reported global SRAM headroom | 303,956 | Reported as remaining for local variables by Arduino IDE |

## Interpretation

The 1,040-byte prediction is for the compact learned data representation, **not** an estimate of the entire compiled sketch. The measured flash count additionally includes ESP32 runtime code, sensor/Arduino libraries, device interface code, classifier and other constants. The SRAM number includes all statically allocated globals and supporting framework/libraries; it should not be compared as if all 1,040 bytes of model data were stored in RAM. The table is explicitly declared `PROGMEM`.

Measurements are from the user's actual **compiled inference sketch**, provided October 23, 2026. Runtime high-watermark heap/stack usage was **not** measured here. The memory output alone does not prove the model or board will classify sunlight correctly.

## Remaining report evidence

- Raw-versus-EMA signal plot requires fresh raw sensor readings (previous dataset only contains filtered values).
- Photograph received; original media still needs adding to the repository if the instructor expects files in GitHub.
- 25-second demonstration video received and retained unchanged at the student's request (the handout requests 30–60 seconds).
- Sunlight classification was not tested in the logged session.
- The final report still needs integration into the user's previous lab paper and a submission release tag when it is actually ready.
