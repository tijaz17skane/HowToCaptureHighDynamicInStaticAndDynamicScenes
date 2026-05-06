# Guide to Capturing HDR Images of Static and Dynamic Scenes

High Dynamic Range, or HDR, is an imaging technique used to represent scenes that contain both very bright and very dark regions. A normal camera image has a limited dynamic range, so when a scene contains strong contrast, such as a bright window inside a dark room, the camera often has to choose between preserving highlight detail or shadow detail.

In a standard low dynamic range image, bright regions may become saturated and appear completely white, while dark regions may become clipped and lose texture. HDR imaging solves this problem by capturing or reconstructing more brightness information than a single standard image can normally store.

A common HDR example might include:

- an underexposed image where the sky, lamp, or window is visible,
- a normally exposed image where midtones look natural,
- an overexposed image where shadows contain more detail,
- and a final HDR or tone-mapped result where both bright and dark areas are visible.

---

<div align="center">

<img width="900" alt="HDR before and after example" src="https://github.com/user-attachments/assets/9b605366-b629-4c9b-a33d-4b1814ceb985" />

<p><em>Example of an HDR-style before/after comparison.</em></p>

<img width="600" alt="HDR exposure bracketing example" src="https://github.com/user-attachments/assets/3b32de08-29c5-4e4a-a2bc-f75b561b7de3" />

<p><em>Exposure bracketing captures information from both bright and dark regions.</em></p>

<img width="600" alt="HDR tone mapping example" src="https://github.com/user-attachments/assets/828b055a-df1d-46c8-ac64-ef9b8b68330a" />

<p><em>Tone mapping compresses HDR data into a displayable image.</em></p>

</div>

---

## Repository Structure

```text
.
├── dng_analysis.ipynb
├── hdr_methods.ipynb
├── images/
│   ├── high_exposure.dng
│   ├── low_exposure.dng
│   └── mid_exposure.dng
├── outputs/
├── requirements.txt
└── utils.py