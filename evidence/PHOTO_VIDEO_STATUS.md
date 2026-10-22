# Physical prototype photo evidence

**Student:** Edryn Clyde Fernandez

**Evidence received:** `IMG_2045.jpeg` supplied in the conversation (October 22, 2026).

## Figure caption for the revised previous-lab paper

*Figure X. ESP32-based light classification proof-of-concept assembly. The ESP32 development board is mounted on a breadboard, with the UV and light-sensing breakout modules connected using jumper wires. The photograph documents the physical prototype used for the on-device classification test.*

## Evidence status

- **Photograph:** Received and visually reviewed. The ESP32 board, breadboard, connected jumper leads and two external sensor boards are visible. Pin-level electrical correctness and individual board model markings cannot be independently confirmed from the photograph alone.
- **GitHub image asset:** The actual JPEG is not yet committed to this repository; it was provided as a conversation attachment. Before submission, add `evidence/IMG_2045.jpeg` to the repository and reference it in the revised paper.
- **30–60 second live demonstration video:** The user mentioned a video, but no video file was available among the received attachments. Do not claim the video was received, reviewed, uploaded, or linked.
- **ESP32 serial results:** The available physical serial evidence is preserved separately in `evidence/device_test_2026-10-16.csv` and its summary; the existing UNKNOWN predictions are retained unchanged.
- **Sunlight:** Sun class was not physically tested during the recorded session because sunlight was unavailable.

## Remaining proof-of-concept requirements

Include the actual image in the revised prior paper, attach a working 30–60 s live-video link, and document the real Arduino flash/SRAM measurements and raw-vs-EMA filtering comparison. The photograph alone does not prove classification accuracy.

**Note:** The current circuit uses the supplied UV and TSL2591 modules; the assignment handout specifies analog IR sensing and instructor approval of the I2C substitution remains a consideration.
