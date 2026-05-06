"""
utils.py

Utility functions for loading, converting, displaying, and saving images
for the HDR OpenCV notebook.

Recommended workflow for unsupported RAW .dng files:

    DNG files
        -> convert to 16-bit TIFF using Darktable / Lightroom / RawTherapee
        -> load TIFF files using load_image_as_8bit_bgr or load_image_as_float_bgr
        -> process using OpenCV

OpenCV cannot reliably read RAW sensor DNG files directly because many DNG
files contain Bayer/CFA sensor data rather than normal RGB image data.
"""

from pathlib import Path

import cv2
import numpy as np


# -------------------------------------------------------------------------
# General image loading using OpenCV
# Use these for TIFF, PNG, JPG, and other already-decoded image formats.
# -------------------------------------------------------------------------

def load_image_as_8bit_bgr(image_path):
    """
    Load an image using OpenCV and return an 8-bit BGR image.

    This is recommended for converted TIFF/PNG/JPG files.

    Args:
        image_path: Path to image file.

    Returns:
        img_8bit_bgr: uint8 BGR image in range [0, 255].
    """

    image_path = Path(image_path)

    img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)

    if img is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}\n"
            "If this is a RAW .dng file, convert it to TIFF first."
        )

    # Grayscale -> BGR
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # BGRA -> BGR
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # 16-bit -> 8-bit
    if img.dtype == np.uint16:
        img = np.clip(img / 256, 0, 255).astype(np.uint8)

    # float -> 8-bit
    elif img.dtype in [np.float32, np.float64]:
        # If image is already in [0, 1], scale directly.
        # Otherwise normalize safely.
        if img.max() <= 1.0:
            img = np.clip(img * 255, 0, 255).astype(np.uint8)
        else:
            img = cv2.normalize(
                img,
                None,
                0,
                255,
                cv2.NORM_MINMAX
            ).astype(np.uint8)

    # Any other integer type -> normalize to 8-bit
    elif img.dtype != np.uint8:
        img = cv2.normalize(
            img,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)

    return img


def load_image_as_float_bgr(image_path):
    """
    Load an image using OpenCV and return a float32 BGR image in range [0, 1].

    This is recommended for single-image tone adjustment methods.

    Args:
        image_path: Path to image file.

    Returns:
        img_float_bgr: float32 BGR image in range [0, 1].
    """

    image_path = Path(image_path)

    img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)

    if img is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}\n"
            "If this is a RAW .dng file, convert it to TIFF first."
        )

    # Grayscale -> BGR
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # BGRA -> BGR
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Convert to float [0, 1]
    if img.dtype == np.uint8:
        img_float = img.astype(np.float32) / 255.0

    elif img.dtype == np.uint16:
        img_float = img.astype(np.float32) / 65535.0

    elif img.dtype in [np.float32, np.float64]:
        img_float = img.astype(np.float32)

        if img_float.max() > 1.0:
            img_float = cv2.normalize(
                img_float,
                None,
                0.0,
                1.0,
                cv2.NORM_MINMAX
            )

    else:
        img_float = cv2.normalize(
            img.astype(np.float32),
            None,
            0.0,
            1.0,
            cv2.NORM_MINMAX
        )

    img_float = np.clip(img_float, 0.0, 1.0).astype(np.float32)

    return img_float


# -------------------------------------------------------------------------
# Optional RAW/DNG loading using rawpy
# These only work if rawpy/LibRaw supports your camera's DNG format.
# -------------------------------------------------------------------------

def load_dng_as_16bit_bgr(dng_path):
    """
    Load a .dng RAW image using rawpy and return a 16-bit BGR image.

    This only works if rawpy/LibRaw supports the DNG format.

    Args:
        dng_path: Path to .dng file.

    Returns:
        bgr_16: uint16 BGR image.
    """

    try:
        import rawpy
    except ImportError as exc:
        raise ImportError(
            "rawpy is not installed. Install it with:\n\n"
            "    pip install rawpy\n"
        ) from exc

    dng_path = Path(dng_path)

    try:
        with rawpy.imread(str(dng_path)) as raw:
            rgb_16 = raw.postprocess(
                use_camera_wb=True,
                no_auto_bright=True,
                output_bps=16
            )

    except Exception as exc:
        raise RuntimeError(
            f"rawpy could not read this DNG file: {dng_path}\n\n"
            "This usually means the DNG is unsupported by LibRaw or is not "
            "a standard RAW file. Convert it to 16-bit TIFF first using "
            "Darktable, RawTherapee, Lightroom, or another RAW converter."
        ) from exc

    bgr_16 = cv2.cvtColor(rgb_16, cv2.COLOR_RGB2BGR)

    return bgr_16


def load_dng_as_8bit_bgr(dng_path):
    """
    Load a .dng RAW image using rawpy and return an 8-bit BGR image.

    This is useful for OpenCV HDR functions if rawpy supports the file.

    Args:
        dng_path: Path to .dng file.

    Returns:
        bgr_8: uint8 BGR image.
    """

    bgr_16 = load_dng_as_16bit_bgr(dng_path)
    bgr_8 = np.clip(bgr_16 / 256, 0, 255).astype(np.uint8)

    return bgr_8


def load_dng_as_float_bgr(dng_path):
    """
    Load a .dng RAW image using rawpy and return a float32 BGR image in [0, 1].

    This only works if rawpy/LibRaw supports the DNG format.

    Args:
        dng_path: Path to .dng file.

    Returns:
        bgr_float: float32 BGR image in range [0, 1].
    """

    bgr_16 = load_dng_as_16bit_bgr(dng_path)
    bgr_float = bgr_16.astype(np.float32) / 65535.0
    bgr_float = np.clip(bgr_float, 0.0, 1.0)

    return bgr_float


# -------------------------------------------------------------------------
# Automatic loader
# Use this if you want the function to decide between DNG and normal images.
# For your current unsupported DNG files, convert to TIFF first.
# -------------------------------------------------------------------------

def load_any_image_as_8bit_bgr(image_path):
    """
    Load either a normal image or a supported DNG as an 8-bit BGR image.

    For .dng files, this tries rawpy first.
    For all other files, it uses OpenCV.

    Args:
        image_path: Path to image.

    Returns:
        uint8 BGR image.
    """

    image_path = Path(image_path)

    if image_path.suffix.lower() == ".dng":
        return load_dng_as_8bit_bgr(image_path)

    return load_image_as_8bit_bgr(image_path)


def load_any_image_as_float_bgr(image_path):
    """
    Load either a normal image or a supported DNG as a float32 BGR image.

    For .dng files, this tries rawpy first.
    For all other files, it uses OpenCV.

    Args:
        image_path: Path to image.

    Returns:
        float32 BGR image in range [0, 1].
    """

    image_path = Path(image_path)

    if image_path.suffix.lower() == ".dng":
        return load_dng_as_float_bgr(image_path)

    return load_image_as_float_bgr(image_path)


# -------------------------------------------------------------------------
# Display helpers
# -------------------------------------------------------------------------

def bgr_to_rgb_for_display(img_bgr):
    """
    Convert an OpenCV BGR image to RGB for matplotlib display.

    Args:
        img_bgr: BGR image.

    Returns:
        RGB image.
    """

    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def float_bgr_to_rgb_for_display(img_bgr_float):
    """
    Convert a float BGR image in range [0, 1] to uint8 RGB for matplotlib.

    Args:
        img_bgr_float: float32 BGR image in range [0, 1].

    Returns:
        uint8 RGB image.
    """

    img_bgr_8bit = np.clip(img_bgr_float * 255, 0, 255).astype(np.uint8)
    img_rgb_8bit = cv2.cvtColor(img_bgr_8bit, cv2.COLOR_BGR2RGB)

    return img_rgb_8bit


# -------------------------------------------------------------------------
# Saving helpers
# -------------------------------------------------------------------------

def save_float_image_as_8bit(img_float, output_path):
    """
    Save a floating-point image in range [0, 1] as an 8-bit image.

    Args:
        img_float: float image in range [0, 1].
        output_path: Output file path.

    Returns:
        img_8bit: saved uint8 image.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img_8bit = np.clip(img_float * 255, 0, 255).astype(np.uint8)

    success = cv2.imwrite(str(output_path), img_8bit)

    if not success:
        raise IOError(f"Could not save image: {output_path}")

    return img_8bit


def save_bgr_image(img_bgr, output_path):
    """
    Save a BGR image using OpenCV.

    Args:
        img_bgr: BGR image.
        output_path: Output file path.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = cv2.imwrite(str(output_path), img_bgr)

    if not success:
        raise IOError(f"Could not save image: {output_path}")


# -------------------------------------------------------------------------
# Small diagnostic helper
# -------------------------------------------------------------------------

def inspect_image_file(image_path):
    """
    Print basic information about an image path and whether OpenCV can read it.

    Args:
        image_path: Path to image.
    """

    image_path = Path(image_path)

    print(f"Path: {image_path}")
    print(f"Exists: {image_path.exists()}")

    if image_path.exists():
        print(f"Size MB: {image_path.stat().st_size / (1024 * 1024):.2f}")

    img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)

    if img is None:
        print("OpenCV read: failed")
    else:
        print("OpenCV read: success")
        print(f"Shape: {img.shape}")
        print(f"Dtype: {img.dtype}")
        print(f"Min: {img.min()}")
        print(f"Max: {img.max()}")
        
        
import tifffile as tiff


def load_dng_with_tifffile_as_float_bgr(image_path):
    """
    Load a Samsung Expert RAW / Linear DNG file using tifffile
    and return a float32 BGR image in range [0, 1].
    """

    image_path = Path(image_path)

    img = tiff.imread(str(image_path))
    img = np.asarray(img)
    img = np.squeeze(img)

    # If channel-first, convert to channel-last.
    # Example: (3, H, W) -> (H, W, 3)
    if img.ndim == 3 and img.shape[0] in [3, 4] and img.shape[-1] not in [3, 4]:
        img = np.moveaxis(img, 0, -1)

    # If grayscale/single channel, make it 3-channel.
    if img.ndim == 2:
        img = np.stack([img, img, img], axis=-1)

    # Remove alpha if present.
    if img.ndim == 3 and img.shape[-1] == 4:
        img = img[..., :3]

    # Convert to float [0, 1].
    if img.dtype == np.uint8:
        img_float = img.astype(np.float32) / 255.0

    elif img.dtype == np.uint16:
        img_float = img.astype(np.float32) / 65535.0

    elif img.dtype in [np.float32, np.float64]:
        img_float = img.astype(np.float32)
        if img_float.max() > 1.0:
            img_float = img_float / img_float.max()

    else:
        img_float = img.astype(np.float32)
        img_float = img_float - img_float.min()
        img_float = img_float / max(img_float.max(), 1e-8)

    img_float = np.clip(img_float, 0.0, 1.0).astype(np.float32)

    # tifffile usually returns RGB-like data.
    # OpenCV uses BGR.
    img_bgr = cv2.cvtColor(img_float, cv2.COLOR_RGB2BGR)

    return img_bgr


def load_dng_with_tifffile_as_8bit_bgr(image_path):
    """
    Load a Samsung Expert RAW / Linear DNG file using tifffile
    and return an 8-bit BGR image for OpenCV HDR functions.
    """

    img_float = load_dng_with_tifffile_as_float_bgr(image_path)
    img_8bit = np.clip(img_float * 255, 0, 255).astype(np.uint8)

    return img_8bit