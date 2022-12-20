from PIL import Image
import numpy as np
from typing import Tuple
import cv2
import torch
def get_mask(img):
    white_bg = remove_transparent(img)
    mask = invert_mask(white_bg)
    return mask

def remove_transparent(img):
    # Paste transparent background img to a white background
    white_bg = Image.new("RGBA", img.size, "WHITE")
    white_bg.paste(img, mask=img)
    new_img = np.array(white_bg.convert("RGB"))
    return Image.fromarray(new_img)

def invert_mask(img):
    mask = np.invert(img)
    return Image.fromarray(mask)

def resize_and_crop(img):
    """
    Crop the image into size divisible by 8
    """
    width = (img.width // 8) * 8
    height = (img.height // 8) * 8
    left = int((img.width - width) / 2)
    right = left + width
    top = int((img.height - height) / 2)
    bottom = top + height
    image = img.crop((left, top, right, bottom))
    return image

def pad(image: np.array, factor: int = 32, border: int = cv2.BORDER_CONSTANT) -> tuple:
    """Pads the image on the sides, so that it will be divisible by factor for U-Net.
    """
    height, width = image.shape[:2]

    if height % factor == 0:
        y_min_pad = 0
        y_max_pad = 0
    else:
        y_pad = factor - height % factor
        y_min_pad = y_pad // 2
        y_max_pad = y_pad - y_min_pad

    if width % factor == 0:
        x_min_pad = 0
        x_max_pad = 0
    else:
        x_pad = factor - width % factor
        x_min_pad = x_pad // 2
        x_max_pad = x_pad - x_min_pad

    padded_image = cv2.copyMakeBorder(image, y_min_pad, y_max_pad, x_min_pad, x_max_pad, border)

    return padded_image, (x_min_pad, y_min_pad, x_max_pad, y_max_pad)


def unpad(image: np.array, pads: Tuple[int, int, int, int]) -> np.ndarray:
    """Crops patch from the center so that sides are equal to pads.
    """
    x_min_pad, y_min_pad, x_max_pad, y_max_pad = pads
    height, width = image.shape[:2]

    return image[y_min_pad : height - y_max_pad, x_min_pad : width - x_max_pad]


def normalize_cv2(img, mean, denominator):
    if mean.shape and len(mean) != 4 and mean.shape != img.shape:
        mean = np.array(mean.tolist() + [0] * (4 - len(mean)), dtype=np.float64)
    if not denominator.shape:
        denominator = np.array([denominator.tolist()] * 4, dtype=np.float64)
    elif len(denominator) != 4 and denominator.shape != img.shape:
        denominator = np.array(denominator.tolist() + [1] * (4 - len(denominator)), dtype=np.float64)

    img = np.ascontiguousarray(img.astype("float32"))
    cv2.subtract(img, mean.astype(np.float64), img)
    cv2.multiply(img, denominator.astype(np.float64), img)
    return img


def normalize_numpy(img, mean, denominator):
    img = img.astype(np.float32)
    img -= mean
    img *= denominator
    return img


def normalize(img, 
              mean=(0.485, 0.456, 0.406),
              std=(0.229, 0.224, 0.225),
              max_pixel_value=255.0):
    mean = np.array(mean, dtype=np.float32)
    mean *= max_pixel_value

    std = np.array(std, dtype=np.float32)
    std *= max_pixel_value

    denominator = np.reciprocal(std, dtype=np.float32)

    if img.ndim == 3 and img.shape[-1] == 3:
        return normalize_cv2(img, mean, denominator)
    return normalize_numpy(img, mean, denominator)

def tensor_from_rgb_image(image: np.ndarray) -> torch.Tensor:
    image = np.ascontiguousarray(np.transpose(image, (2, 0, 1)))
    return torch.unsqueeze(torch.from_numpy(image),0)

def prepare_unet_img(img):
    padded_img, pads = pad(img, factor=32)
    padded_img = normalize(padded_img)
    padded_img = tensor_from_rgb_image(padded_img)
    return padded_img, pads