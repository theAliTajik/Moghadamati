from PIL import Image
import io

def crop_image(input_image, aspect_ratio, crop_from):
    """
    Crops the given image to the specified aspect ratio from the specified position.

    :param input_image: Image file to be cropped.
    :param aspect_ratio: Desired aspect ratio (width, height) as a tuple.
    :param crop_from: Position to crop from ('top', 'bottom', 'center').
    :return: Cropped image.
    """
    # Open the image
    image = Image.open(input_image)

    # Original dimensions
    orig_width, orig_height = image.size

    # Target dimensions
    target_ratio = aspect_ratio[0] / aspect_ratio[1]
    target_width, target_height = orig_width, int(orig_width / target_ratio)

    # Adjust dimensions if needed
    if target_height > orig_height:
        target_height = orig_height
        target_width = int(target_height * target_ratio)

    # Calculate cropping coordinates
    if crop_from == 'top':
        left = (orig_width - target_width) // 2
        top = 0
        right = left + target_width
        bottom = top + target_height
    elif crop_from == 'bottom':
        left = (orig_width - target_width) // 2
        bottom = orig_height
        right = left + target_width
        top = bottom - target_height
    else:  # center
        left = (orig_width - target_width) // 2
        top = (orig_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

    # Crop and return image
    return image.crop((left, top, right, bottom))

# Example usage (this will be removed in the final code snippet):
cropped_image = crop_image("M:\Python\Moghadamati\\telegram_bot\ComfyUI_temp_jkaph_00009_.png", (1, 1), "center")
cropped_image.show()
