from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
from io import BytesIO

# Replace 'YOUR_TOKEN' with your bot's token
TOKEN = '6325359867:AAFH_O3CTONMbQ3SPwlKm3aC8is_UefE_hg'

def crop_image(image, aspect_ratio, crop_from):
    """
    Crops the given image to the specified aspect ratio from the specified position.

    :param input_image: Image file to be cropped.
    :param aspect_ratio: Desired aspect ratio (width, height) as a tuple.
    :param crop_from: Position to crop from ('top', 'bottom', 'center').
    :return: Cropped image.
    """
    # Open the image

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
# cropped_image = crop_image("path_to_image.jpg", (16, 9), "center")
# cropped_image.show()


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me an image.')

def handle_image(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.photo[-1].file_id)
    f = BytesIO(file.download_as_bytearray())
    image = Image.open(f)

    update.message.reply_text('Please send the aspect ratio in the format width:height (e.g., 16:9).')
    context.user_data['image'] = image

def handle_ratio(update: Update, context: CallbackContext) -> None:
    try:
        width_ratio, height_ratio = map(int, update.message.text.split(':'))
        context.user_data['aspect_ratio'] = (width_ratio, height_ratio)
        update.message.reply_text('Please send the crop position (top, bottom, center).')
    except ValueError:
        update.message.reply_text('Invalid ratio. Please send the aspect ratio in the format width:height (e.g., 16:9).')

def handle_crop_position(update: Update, context: CallbackContext) -> None:
    crop_from = update.message.text.lower()
    if crop_from not in ['top', 'bottom', 'center']:
        update.message.reply_text('Invalid position. Please send either top, bottom, or center.')
        return

    try:
        aspect_ratio = context.user_data['aspect_ratio']
        cropped_image = crop_image(context.user_data['image'], aspect_ratio, crop_from)
        
        bio = BytesIO()
        cropped_image.save(bio, 'JPEG')
        bio.seek(0)

        update.message.reply_photo(photo=bio)
    except KeyError:
        update.message.reply_text('Please send an image first.')


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_ratio))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_crop_position))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
