# Guide to Capturing HDR Images of Static Scenes Using a Stationary Camera

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

## 1. Capturing HDR Images for Static Scenes

For a static scene and a stationary camera, the most reliable way to create an HDR image is **exposure bracketing**. Exposure bracketing means capturing several images of the same scene from exactly the same camera position, but with different exposure times.

This is useful because no single exposure can capture every part of a high-contrast scene correctly. A short exposure protects bright regions from becoming fully white, while a long exposure reveals details hidden in the shadows. By combining these images, we can create a final result that contains more detail across the full brightness range of the scene.

For example, consider an indoor scene with a bright window. If the camera exposes for the room, the window may become completely white. If the camera exposes for the window, the room may become too dark. HDR imaging solves this by capturing both exposures and combining their useful information.

The basic idea is:

```text
Short exposure  → preserves highlights
Medium exposure → preserves midtones
Long exposure   → preserves shadows

Combined result → better detail across highlights, midtones, and shadows
```

Because the scene is static, the content does not change between shots. Because the camera is stationary, each pixel location should correspond to the same point in the scene across all exposures. This makes static-scene HDR much easier than HDR for dynamic scenes.

### 1.1 Why the Camera Must Be Stationary

HDR merging assumes that the input images are aligned. If the camera moves between shots, the same object may appear in slightly different pixel locations. This can lead to blur, double edges, or ghosting artifacts in the final image.

A tripod or rigid camera mount is strongly recommended. Even when using a tripod, small vibrations can occur when pressing the shutter button. To reduce this, it is useful to use:

```text
tripod or rigid mount
remote shutter release
timer mode
electronic shutter, if available
mirror lock-up for DSLR cameras, if available
```

OpenCV provides image alignment tools that can correct small shifts, but it is still better to capture the images as cleanly as possible.

### 1.2 Camera Settings

The most important rule is:

```text
Only change the shutter speed.
```

The following settings should remain fixed:

```text
Camera position: fixed
Focus: manual and fixed
White balance: fixed
ISO: fixed
Aperture: fixed
Shutter speed: varied
Image format: RAW preferred
```

### 1.3 Why Only Shutter Speed Should Change

Changing the shutter speed changes the exposure without changing the optical properties of the image. This is ideal for HDR.

Changing aperture is not recommended because it changes the depth of field. This means some parts of the image may become more or less blurred between exposures.

Changing ISO is also not ideal because it changes the noise characteristics of the image. A high-ISO shadow exposure may contain more noise than a low-ISO highlight exposure. This makes merging less consistent.

Changing focus should also be avoided because it changes the sharpness and geometry of the image.

Therefore, for clean HDR capture:

```text
Good:
    fixed aperture
    fixed ISO
    fixed focus
    varied shutter speed

Avoid:
    varied aperture
    varied ISO
    autofocus between shots
    automatic white balance
```

### 1.4 Choosing Exposure Values

A simple three-image bracket can be:

```text
Image 1: underexposed
Image 2: normally exposed
Image 3: overexposed
```

In exposure value terms:

```text
Image 1: -2 EV
Image 2:  0 EV
Image 3: +2 EV
```

A stronger bracket can use five or seven images:

```text
Image 1: -3 EV
Image 2: -2 EV
Image 3: -1 EV
Image 4:  0 EV
Image 5: +1 EV
Image 6: +2 EV
Image 7: +3 EV
```

In shutter speed terms, this could look like:

```text
1/1000 s
1/250 s
1/60 s
1/15 s
1/4 s
```

The exact exposure values depend on the scene. The important goal is to capture the full brightness range.

At least one image should preserve the highlights. This means bright regions such as skies, windows, lamps, or reflections should not be fully saturated.

At least one image should reveal the shadows. This means dark areas should contain visible detail instead of being completely black.

### 1.5 Checking Whether the Bracket Is Good

A good exposure bracket should satisfy the following:

```text
The darkest image has visible highlight detail.
The brightest image has visible shadow detail.
The middle image has natural-looking midtones.
The scene does not move between images.
The camera does not move between images.
```

If the brightest parts of the scene are white in every image, the highlights are clipped and cannot be recovered.

If the darkest parts of the scene are black in every image, the shadows contain no useful information and cannot be recovered.

HDR can combine captured information, but it cannot recover information that was never recorded.

### 1.6 RAW vs JPEG for HDR

RAW images are preferred for HDR because they usually contain more bit depth and less camera processing. A JPEG is normally already compressed, sharpened, white-balanced, tone-mapped, and converted to 8-bit color. This reduces the amount of information available for HDR processing.

RAW files preserve more sensor data, which is especially useful when recovering shadows or protecting highlights.

A practical workflow is:

```text
Capture RAW bracketed images
        ↓
Decode RAW files
        ↓
Convert them into arrays
        ↓
Process using OpenCV
        ↓
Merge into HDR or enhance as single images
```

OpenCV is excellent for the image processing part. However, for loading `.dng` RAW files, it is usually better to use `rawpy`, then pass the decoded image to OpenCV.

---

## 2. General HDR Pipeline

The standard multi-exposure HDR pipeline is:

```text
Capture bracketed images
        ↓
Load images
        ↓
Align images
        ↓
Estimate camera response function
        ↓
Merge exposures into HDR radiance map
        ↓
Tone-map HDR image for display
```

The HDR radiance map contains high dynamic range information. However, normal displays cannot directly show the full range of HDR brightness values. Therefore, tone mapping is used to compress the HDR image into a normal image that can be displayed on a standard monitor.

---

## 3. Project Setup

Install the required packages:

```bash
pip install opencv-python numpy rawpy imageio
```

Example folder structure:

```text
hdr-guide/
│
├── README.md
│
├── images/
│   ├── low_exposure.dng
│   ├── mid_exposure.dng
│   ├── high_exposure.dng
│   └── underexposed.dng
│
└── src/
    ├── method_1_hdr_stacking.py
    ├── method_2_shadow_boost.py
    └── method_3_mid_exposure_adjustment.py
```

---

## 4. Loading RAW `.dng` Images

OpenCV does not reliably load all RAW `.dng` files directly. A practical approach is to decode the RAW file using `rawpy`, then convert the result into an OpenCV-compatible image.

`rawpy` returns an RGB image. OpenCV uses BGR by default, so we convert RGB to BGR before processing.

### 4.1 Load a RAW Image as 16-bit BGR

```python
import rawpy
import cv2
import numpy as np


def load_dng_as_16bit_bgr(dng_path):
    """
    Load a .dng RAW image and convert it to a 16-bit OpenCV BGR image.

    rawpy returns RGB.
    OpenCV uses BGR.
    """

    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    bgr_16 = cv2.cvtColor(rgb_16, cv2.COLOR_RGB2BGR)

    return bgr_16
```

### 4.2 Load a RAW Image as Float BGR

For tonal adjustments, it is useful to work with floating-point images in the range `[0, 1]`.

```python
def load_dng_as_float_bgr(dng_path):
    """
    Load a .dng RAW image as a floating-point BGR image in range [0, 1].
    """

    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    rgb_float = rgb_16.astype(np.float32) / 65535.0
    bgr_float = cv2.cvtColor(rgb_float, cv2.COLOR_RGB2BGR)

    return bgr_float
```

### 4.3 Load a RAW Image as 8-bit BGR

Some OpenCV HDR functions are commonly used with standard 8-bit images. For that case, we can convert the decoded RAW image to 8-bit.

```python
def load_dng_as_8bit_bgr(dng_path):
    """
    Load a .dng RAW image and convert it to an 8-bit OpenCV BGR image.
    """

    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    rgb_8 = np.clip(rgb_16 / 256, 0, 255).astype(np.uint8)
    bgr_8 = cv2.cvtColor(rgb_8, cv2.COLOR_RGB2BGR)

    return bgr_8
```

---

# Method 1: True HDR Using Exposure Stacking

The first method is true multi-exposure HDR. It uses a low exposure, mid exposure, and high exposure image of the same static scene.

This method is the most technically correct HDR approach because it captures real scene information at multiple exposure levels.

The input images are:

```text
low_exposure.dng   → protects highlights
mid_exposure.dng   → captures midtones
high_exposure.dng  → reveals shadows
```

Example exposure times:

```text
low exposure:  1/500 s
mid exposure:  1/125 s
high exposure: 1/30 s
```

The order of the exposure times must match the order of the images.

---

## 5. Step-by-Step HDR Stacking Using OpenCV

### Step 1: Import Libraries

```python
import cv2
import rawpy
import numpy as np
from pathlib import Path
```

### Step 2: Load the RAW Images

```python
def load_dng_as_8bit_bgr(dng_path):
    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    rgb_8 = np.clip(rgb_16 / 256, 0, 255).astype(np.uint8)
    bgr_8 = cv2.cvtColor(rgb_8, cv2.COLOR_RGB2BGR)

    return bgr_8
```

### Step 3: Define Image Paths and Exposure Times

```python
image_paths = [
    Path("images/low_exposure.dng"),
    Path("images/mid_exposure.dng"),
    Path("images/high_exposure.dng"),
]

exposure_times = np.array([
    1 / 500,
    1 / 125,
    1 / 30,
], dtype=np.float32)
```

### Step 4: Align the Images

Even with a stationary camera, small shifts can happen. OpenCV's `createAlignMTB()` can help align the images before merging.

```python
images = [load_dng_as_8bit_bgr(path) for path in image_paths]

align = cv2.createAlignMTB()
align.process(images, images)
```

### Step 5: Estimate Camera Response Function

The camera response function describes how real scene brightness is mapped to pixel intensity.

```python
calibrate = cv2.createCalibrateDebevec()
response = calibrate.process(images, exposure_times)
```

### Step 6: Merge Images into HDR Radiance Map

```python
merge_debevec = cv2.createMergeDebevec()
hdr = merge_debevec.process(images, exposure_times, response)

cv2.imwrite("method_1_stacked_hdr.hdr", hdr)
```

The `.hdr` file contains the HDR radiance map.

### Step 7: Tone-Map for Display

Normal screens cannot display raw HDR radiance values directly, so we tone-map the result.

```python
tonemap = cv2.createTonemapReinhard(
    gamma=1.5,
    intensity=0.0,
    light_adapt=0.8,
    color_adapt=0.0
)

ldr = tonemap.process(hdr)

ldr_8bit = np.clip(ldr * 255, 0, 255).astype(np.uint8)

cv2.imwrite("method_1_stacked_hdr_tonemapped.jpg", ldr_8bit)
```

---

## 6. Full Code for Method 1

```python
import cv2
import rawpy
import numpy as np
from pathlib import Path


def load_dng_as_8bit_bgr(dng_path):
    """
    Load a DNG image and convert it to an 8-bit BGR image for OpenCV HDR merging.
    """

    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    rgb_8 = np.clip(rgb_16 / 256, 0, 255).astype(np.uint8)
    bgr_8 = cv2.cvtColor(rgb_8, cv2.COLOR_RGB2BGR)

    return bgr_8


def hdr_stack_dng_images(image_paths, exposure_times, output_prefix="method_1"):
    """
    Create a true HDR image from bracketed DNG exposures.
    """

    images = [load_dng_as_8bit_bgr(path) for path in image_paths]

    if len(images) != len(exposure_times):
        raise ValueError("Number of images and exposure times must match.")

    # Align images.
    align = cv2.createAlignMTB()
    align.process(images, images)

    # Estimate camera response.
    calibrate = cv2.createCalibrateDebevec()
    response = calibrate.process(images, exposure_times)

    # Merge into HDR radiance map.
    merge_debevec = cv2.createMergeDebevec()
    hdr = merge_debevec.process(images, exposure_times, response)

    cv2.imwrite(f"{output_prefix}_stacked_hdr.hdr", hdr)

    # Tone-map HDR result for display.
    tonemap = cv2.createTonemapReinhard(
        gamma=1.5,
        intensity=0.0,
        light_adapt=0.8,
        color_adapt=0.0
    )

    ldr = tonemap.process(hdr)
    ldr_8bit = np.clip(ldr * 255, 0, 255).astype(np.uint8)

    cv2.imwrite(f"{output_prefix}_stacked_hdr_tonemapped.jpg", ldr_8bit)

    return hdr, ldr_8bit


if __name__ == "__main__":
    image_paths = [
        Path("images/low_exposure.dng"),
        Path("images/mid_exposure.dng"),
        Path("images/high_exposure.dng"),
    ]

    exposure_times = np.array([
        1 / 500,
        1 / 125,
        1 / 30,
    ], dtype=np.float32)

    hdr_stack_dng_images(
        image_paths=image_paths,
        exposure_times=exposure_times,
        output_prefix="method_1"
    )
```

---

# Method 2: Boosting Shadows in an Underexposed Image

The second method uses only one image: an underexposed image.

This is useful when the scene contains important bright regions that must not be clipped. For example, if there is a bright sky or window, we can intentionally underexpose the image to preserve those highlights. Then we digitally boost the shadows.

This is not true HDR because no additional exposure information is being captured. It is a single-image enhancement method.

The advantage is that it avoids alignment problems and motion artifacts.

The disadvantage is that shadows may become noisy, especially if they were very dark in the original image.

The idea is:

```text
Capture underexposed image
        ↓
Preserve highlights
        ↓
Boost shadows digitally
        ↓
Improve local contrast
```

---

## 7. Step-by-Step Shadow Boosting

### Step 1: Load the Underexposed RAW Image

```python
img = load_dng_as_float_bgr("images/underexposed.dng")
```

### Step 2: Apply Gamma Correction

Gamma correction can brighten darker regions. A gamma value below `1.0` lifts shadows.

```text
gamma = 1.0  → unchanged
gamma = 0.8  → mild shadow lift
gamma = 0.6  → stronger shadow lift
gamma = 0.5  → very strong shadow lift
```

```python
def gamma_correct(img_float, gamma=0.6):
    corrected = np.power(img_float, gamma)
    return np.clip(corrected, 0.0, 1.0)
```

### Step 3: Apply Local Contrast Enhancement

CLAHE improves local contrast. It is better to apply CLAHE to the luminance channel instead of directly applying it to the color channels.

```python
def apply_clahe_to_float_bgr(img_float):
    img_8bit = np.clip(img_float * 255, 0, 255).astype(np.uint8)

    lab = cv2.cvtColor(img_8bit, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge([l_enhanced, a, b])
    result = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    return result.astype(np.float32) / 255.0
```

---

## 8. Full Code for Method 2

```python
import cv2
import rawpy
import numpy as np


def load_dng_as_float_bgr(dng_path):
    """
    Load a DNG image as a floating-point BGR image in range [0, 1].
    """

    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    rgb_float = rgb_16.astype(np.float32) / 65535.0
    bgr_float = cv2.cvtColor(rgb_float, cv2.COLOR_RGB2BGR)

    return bgr_float


def gamma_correct(img_float, gamma=0.6):
    """
    Apply gamma correction.
    Gamma below 1 brightens the image.
    """

    corrected = np.power(img_float, gamma)
    return np.clip(corrected, 0.0, 1.0)


def apply_clahe_to_float_bgr(img_float):
    """
    Apply CLAHE to luminance channel.
    """

    img_8bit = np.clip(img_float * 255, 0, 255).astype(np.uint8)

    lab = cv2.cvtColor(img_8bit, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge([l_enhanced, a, b])
    result = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    return result.astype(np.float32) / 255.0


def shadow_boost_underexposed_image(input_path, output_path):
    """
    Boost shadows in an underexposed image.
    """

    img = load_dng_as_float_bgr(input_path)

    # Lift shadows.
    boosted = gamma_correct(img, gamma=0.6)

    # Improve local contrast.
    enhanced = apply_clahe_to_float_bgr(boosted)

    output_8bit = np.clip(enhanced * 255, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, output_8bit)

    return output_8bit


if __name__ == "__main__":
    shadow_boost_underexposed_image(
        input_path="images/underexposed.dng",
        output_path="method_2_shadow_boosted.jpg"
    )
```

---

# Method 3: Reducing Highlights and Boosting Shadows in a Mid-Exposed Image

The third method starts from a normally exposed image. Instead of using multiple exposures, we process the mid-exposed image to make the result look more balanced.

The idea is:

```text
Start with mid-exposed image
        ↓
Reduce highlights
        ↓
Boost shadows
        ↓
Preserve midtones
        ↓
Improve local contrast
```

This is similar to what happens when using the "highlights" and "shadows" sliders in photo editing software.

This method is also not true HDR. It cannot recover detail from clipped highlights or completely black shadows. However, it can make a normal image look more balanced and more readable.

---

## 9. Step-by-Step Mid-Exposure Adjustment

### Step 1: Load the Mid-Exposed RAW Image

```python
img = load_dng_as_float_bgr("images/mid_exposure.dng")
```

### Step 2: Convert to LAB Color Space

LAB color space separates luminance from color. This lets us adjust brightness without strongly changing color.

```python
img_8bit = np.clip(img * 255, 0, 255).astype(np.uint8)

lab = cv2.cvtColor(img_8bit, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
```

### Step 3: Create Shadow and Highlight Masks

```python
l_float = l.astype(np.float32) / 255.0

shadow_mask = 1.0 - l_float
highlight_mask = l_float
```

Dark pixels receive a stronger shadow mask. Bright pixels receive a stronger highlight mask.

### Step 4: Boost Shadows and Reduce Highlights

```python
shadow_boost = 0.35
highlight_reduction = 0.25

adjusted_l = l_float.copy()

adjusted_l = adjusted_l + shadow_boost * shadow_mask * (1.0 - adjusted_l)
adjusted_l = adjusted_l - highlight_reduction * highlight_mask * adjusted_l

adjusted_l = np.clip(adjusted_l, 0.0, 1.0)
```

### Step 5: Improve Local Contrast

```python
adjusted_l_8bit = np.clip(adjusted_l * 255, 0, 255).astype(np.uint8)

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

adjusted_l_8bit = clahe.apply(adjusted_l_8bit)
```

---

## 10. Full Code for Method 3

```python
import cv2
import rawpy
import numpy as np


def load_dng_as_float_bgr(dng_path):
    """
    Load a DNG image as a floating-point BGR image in range [0, 1].
    """

    with rawpy.imread(str(dng_path)) as raw:
        rgb_16 = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=True,
            output_bps=16
        )

    rgb_float = rgb_16.astype(np.float32) / 65535.0
    bgr_float = cv2.cvtColor(rgb_float, cv2.COLOR_RGB2BGR)

    return bgr_float


def adjust_mid_exposure_image(
    input_path,
    output_path,
    shadow_boost=0.35,
    highlight_reduction=0.25
):
    """
    Reduce highlights and boost shadows in a mid-exposed image.
    """

    img = load_dng_as_float_bgr(input_path)

    img_8bit = np.clip(img * 255, 0, 255).astype(np.uint8)

    lab = cv2.cvtColor(img_8bit, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    l_float = l.astype(np.float32) / 255.0

    # Stronger in dark regions.
    shadow_mask = 1.0 - l_float

    # Stronger in bright regions.
    highlight_mask = l_float

    adjusted_l = l_float.copy()

    # Lift shadows.
    adjusted_l = adjusted_l + shadow_boost * shadow_mask * (1.0 - adjusted_l)

    # Pull down highlights.
    adjusted_l = adjusted_l - highlight_reduction * highlight_mask * adjusted_l

    adjusted_l = np.clip(adjusted_l, 0.0, 1.0)

    adjusted_l_8bit = np.clip(adjusted_l * 255, 0, 255).astype(np.uint8)

    # Improve local contrast.
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    adjusted_l_8bit = clahe.apply(adjusted_l_8bit)

    lab_adjusted = cv2.merge([adjusted_l_8bit, a, b])
    result = cv2.cvtColor(lab_adjusted, cv2.COLOR_LAB2BGR)

    cv2.imwrite(output_path, result)

    return result


if __name__ == "__main__":
    adjust_mid_exposure_image(
        input_path="images/mid_exposure.dng",
        output_path="method_3_mid_exposure_adjusted.jpg",
        shadow_boost=0.35,
        highlight_reduction=0.25
    )
```

---

# 11. Comparison of the Three Approaches

The three methods have different purposes.

| Method | Input Required | True HDR? | Best For | Main Advantage | Main Limitation |
|---|---:|---:|---|---|---|
| Exposure stacking | Multiple exposures | Yes | Static scenes | Best highlight and shadow recovery | Requires static scene and stationary camera |
| Shadow boosting from underexposed image | One underexposed image | No | Preserving highlights | Avoids clipped highlights and motion artifacts | Shadows may become noisy |
| Mid-exposure adjustment | One normal image | No | Quick visual improvement | Simple and convenient | Cannot recover clipped highlights or black shadows |

---

## 11.1 Method 1: Exposure Stacking

Exposure stacking is the best method when the scene is static and the camera is stationary. It captures real image information at different exposure levels and combines the useful parts.

This method should be used when the goal is:

```text
maximum dynamic range
best image quality
best highlight recovery
best shadow recovery
controlled imaging setup
static scenes
```

This is the only method in this guide that produces a true HDR radiance map.

---

## 11.2 Method 2: Shadow Boosting from an Underexposed Image

This method is useful when highlight preservation is the priority. By underexposing the image, bright regions are less likely to clip. Then shadows can be boosted afterwards.

This method should be used when the goal is:

```text
preserve bright regions
avoid overexposed skies or windows
work with a single image
avoid motion artifacts
```

The main downside is noise. If the shadows were very dark in the original image, boosting them will also boost noise.

---

## 11.3 Method 3: Mid-Exposure Highlight and Shadow Adjustment

This method is useful when only a normal exposure is available. It can improve the visual balance of an image by compressing the brightness range.

This method should be used when the goal is:

```text
quick image enhancement
balanced-looking image
simple single-image workflow
no exposure bracket available
```

This method is convenient, but it should not be described as true HDR. It is better described as tone adjustment or dynamic range compression.

---

# 12. Final Recommendation for Static Scenes

For static scenes and a stationary camera, the recommended method is:

```text
Method 1: true HDR using exposure stacking
```

This method captures actual information from multiple exposure levels and gives the best chance of recovering both highlight and shadow detail.

The single-image approaches are useful fallback methods:

```text
Method 2:
    Best when highlights must be protected and only one image can be used.

Method 3:
    Best when a normal image already exists and only visual improvement is needed.
```

For a controlled imaging systems task, exposure stacking should be the primary method. The other two methods are better described as single-image enhancement techniques.

---

# 13. HDR for Dynamic Scenes

Dynamic scenes are more difficult than static scenes because objects may move between exposures. Examples include:

```text
people walking
cars moving
trees moving in wind
water waves
rain
changing lights
handheld camera motion
```

In a static HDR pipeline, the algorithm assumes that the same pixel location corresponds to the same scene point in every exposure. Motion breaks this assumption.

This can create artifacts such as:

```text
ghosting
double edges
blurred moving objects
incorrect colors around motion boundaries
misaligned object edges
```

For example, if a person walks through the frame while three images are captured, they may appear in different positions in each exposure. When the images are merged, the person may appear multiple times or look transparent.

---

## 13.1 Practical Options for Dynamic Scenes

For dynamic scenes, there are three practical options.

### Option 1: Single-Frame Enhancement

For strongly dynamic scenes, a single image is often safer than multi-exposure HDR. This avoids ghosting because there is only one frame.

Single-frame methods include:

```text
shoot RAW
expose for highlights
boost shadows afterwards
apply local contrast enhancement
use tone adjustment
```

This does not create true HDR, but it is often more reliable for moving scenes.

### Option 2: Exposure Fusion for Slight Motion

If the scene has only slight motion, exposure fusion may produce a usable result. OpenCV provides `createMergeMertens()` for exposure fusion.

Exposure fusion does not require exposure times. It directly combines well-exposed regions from each image into a normal displayable image.

```python
import cv2
import numpy as np
from pathlib import Path


def exposure_fusion(image_paths, output_path):
    images = []

    for path in image_paths:
        img = cv2.imread(str(path))

        if img is None:
            raise FileNotFoundError(f"Could not read image: {path}")

        images.append(img)

    align = cv2.createAlignMTB()
    align.process(images, images)

    merge_mertens = cv2.createMergeMertens()
    fusion = merge_mertens.process(images)

    fusion_8bit = np.clip(fusion * 255, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, fusion_8bit)

    return fusion_8bit


if __name__ == "__main__":
    image_paths = [
        Path("dynamic/low.jpg"),
        Path("dynamic/mid.jpg"),
        Path("dynamic/high.jpg"),
    ]

    exposure_fusion(
        image_paths=image_paths,
        output_path="dynamic_exposure_fusion.jpg"
    )
```

This may work for minor movement, but the result should always be checked for ghosting.

### Option 3: Hardware HDR

For truly dynamic scenes, the best solution is often hardware-based HDR or single-shot HDR.

Examples include:

```text
high dynamic range sensors
dual-gain sensors
log video profiles
RAW video
computational HDR pipelines in phones or cameras
```

These approaches reduce or remove the time gap between exposures, which helps avoid motion artifacts.

---

# 14. Dynamic Scene Summary

For static scenes:

```text
Use exposure bracketing and true HDR stacking.
```

For scenes with slight motion:

```text
Try exposure fusion and inspect the result carefully.
```

For strongly dynamic scenes:

```text
Use single-frame RAW recovery, single-frame enhancement, or hardware HDR.
```

Multi-exposure HDR is most reliable when nothing moves. Once motion is introduced, the problem becomes harder because the images no longer represent the same scene at the same moment.

---

# 15. Conclusion

HDR imaging is most reliable when the camera is stationary and the scene is static. In this setup, multiple exposures can be captured and merged to recover detail from both shadows and highlights.

The best technical method is true HDR exposure stacking. This combines low, mid, and high exposure images into an HDR radiance map, which can then be tone-mapped for display.

Single-image methods such as shadow boosting or mid-exposure adjustment can improve the appearance of an image, but they are not true HDR. They are useful when only one image is available or when motion makes exposure stacking unreliable.

In summary:

```text
Best overall HDR quality:
    Multi-exposure HDR stacking

Best single-image highlight protection:
    Underexpose and boost shadows

Best quick visual improvement:
    Adjust highlights and shadows in a mid-exposed image

Best for dynamic scenes:
    Single-frame enhancement or hardware HDR
```
