import os
import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    """
    Reads and returns EXIF data from an image.
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is None:
            return {}
        decoded_exif = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            decoded_exif[tag] = value
        return decoded_exif
    except (IOError, AttributeError):
        return None

def strip_exif_data(image_path, output_path):
    """
    Strips EXIF data from an image and saves it to a new file.
    """
    try:
        image = Image.open(image_path)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(output_path)
        return True
    except (IOError, AttributeError):
        return False

def display_exif(exif_data, title):
    """
    Prints formatted EXIF data.
    """
    print(f"\n--- {title} ---")
    if not exif_data:
        print("No EXIF data found.")
        return
    for tag, value in exif_data.items():
        if isinstance(value, bytes):
            try:
                value = value.decode('utf-8', 'ignore')
            except UnicodeDecodeError:
                value = str(value)
        print(f"  {tag}: {value}")

def main():
    parser = argparse.ArgumentParser(
        description="Recursively strips EXIF data from images in a directory and saves them to an output directory.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_dir",
        help="The path to the input directory containing images to process."
    )
    parser.add_argument(
        "output_dir",
        help="The path to the output directory where EXIF-stripped images will be saved. The directory structure will be replicated."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose mode to display EXIF data before and after stripping for each image."
    )

    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    verbose_mode = args.verbose

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Processing images from '{input_dir}' and saving to '{output_dir}'...")

    for root, _, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)
        output_path_root = os.path.join(output_dir, relative_path)
        os.makedirs(output_path_root, exist_ok=True)

        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(output_path_root, filename)
                
                if verbose_mode:
                    print(f"\nProcessing '{input_path}'...")
                    original_exif = get_exif_data(input_path)
                    if original_exif is not None:
                        display_exif(original_exif, "EXIF Data Before Stripping")

                if strip_exif_data(input_path, output_path):
                    print(f"Successfully stripped and saved '{filename}'.")
                    if verbose_mode:
                        new_exif = get_exif_data(output_path)
                        display_exif(new_exif, "EXIF Data After Stripping")
                else:
                    print(f"Failed to process '{filename}'.")

if __name__ == "__main__":
    main()