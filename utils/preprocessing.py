from PIL import Image
import numpy as np

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