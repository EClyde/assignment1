# Physical prototype photo and demonstration video evidence

**Student:** Edryn Clyde Fernandez

**Evidence received:** `IMG_2045.jpeg` photo and `IMG_0649.mp4` video supplied in the conversation (October 22, 2026).

## Figure caption for the revised previous-lab paper

*Figure X. ESP32-based light classification proof-of-concept assembly. The ESP32 development board is mounted on a breadboard, with the UV and light-sensing breakout modules connected using jumper wires. The photograph documents the physical prototype used for the on-device classification test.*

## Evidence status

- **Photograph:** Received and visually reviewed. The ESP32 board, breadboard, connected jumper leads and two external sensor boards are visible. Pin-level electrical correctness and individual board model markings cannot be independently confirmed from the photograph alone.
- **GitHub image asset:** The actual JPEG is not yet committed to this repository; it was provided as a conversation attachment. Before submission, add `evidence/IMG_2045.jpeg` to the repository and reference it in the revised paper.
- **Live demonstration video:** `IMG_0649.mp4` was received and visually reviewed. Technical metadata: **25.0 seconds**, 512×910 portrait, H.264 video at 30 fps, AAC audio. It shows the ESP32 prototype, sensor interaction, and live Arduino serial-monitor classifications on the laptop; frames show **LED** and **shade** labels. The visible demonstration supports operation, but it is **five seconds shorter than the handout's 30–60 second requirement**. Request a slightly longer demonstration (30–60 seconds) for strict compliance; do not alter the existing classification code or the UNKNOWN rejection behavior. The MP4 has not been uploaded to GitHub and has no public video link yet.
- **ESP32 serial results:** The available physical serial evidence is preserved separately in `evidence/device_test_2026-10-16.csv` and its summary; the existing UNKNOWN predictions are retained unchanged.
- **Sunlight:** Sun class was not physically tested during the recorded session because sunlight was unavailable.

## Suggested video caption

*Video 1. ESP32 light-classification proof-of-concept demonstration. The breadboard prototype is shown alongside live classification results on the computer's serial monitor. The footage includes LED and shade predictions. Recorded duration: 25 seconds (submission requirement: 30–60 seconds).*

## Remaining proof-of-concept requirements

Include the actual image in the revised prior paper, upload an accessible 30–60 s live-video demonstration and link it, and document the real Arduino flash/SRAM measurements and raw-vs-EMA filtering comparison. The photograph alone does not prove classification accuracy.

**Note:** The current circuit uses the supplied UV and TSL2591 modules; the assignment handout specifies analog IR sensing and instructor approval of the I2C substitution remains a consideration.
