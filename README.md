# Guide to Capturing HDR Images of Static Scenes Using a Stationary Camera

High Dynamic Range, or HDR, is an imaging technique used to represent scenes that contain both very bright and very dark regions. A normal camera image has a limited dynamic range, so when a scene contains strong contrast, such as a bright window inside a dark room, the camera often has to choose between preserving highlight detail or shadow detail.

In a standard low dynamic range image, bright regions may become saturated and appear completely white, while dark regions may become clipped and lose texture. HDR imaging solves this by combining information from multiple exposures of the same scene. Short exposures preserve bright areas, while long exposures reveal details in darker areas.

<!-- Insert your own HDR comparison image here -->
<!-- Example: ![HDR comparison](images/hdr_comparison.jpg) -->

A typical HDR example might include:

- an underexposed image where the sky or bright window is visible,
- a normally exposed image where midtones look natural,
- an overexposed image where shadows contain more detail,
- and a final HDR or tone-mapped result where both bright and dark areas are visible.

---
<img width="1280" height="808" alt="bode-museum-berlin-germany-before-and-after-0012" src="https://github.com/user-attachments/assets/9b605366-b629-4c9b-a33d-4b1814ceb985" />

---

## 1. Capturing HDR Images for Static Scenes

For a static scene and a stationary camera, the most reliable way to create an HDR image is exposure bracketing. This means taking multiple photographs from the same camera position while changing only the exposure time.

The scene and camera should remain fixed throughout the sequence. This is important because HDR algorithms assume that corresponding pixels in different images represent the same point in the scene.

### Recommended Camera Setup

Use the following settings:

```text
Camera: stationary or tripod-mounted
Scene: static
Focus: manual and fixed
White balance: fixed
ISO: fixed
Aperture: fixed
Exposure: varied using shutter speed only
Image format: RAW preferred, high-quality JPEG acceptable
