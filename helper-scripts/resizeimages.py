import os
import argparse
from PIL import Image

def letterbox_image(image, target_size=(640, 640)):
    """
    Resizes an image to a target size while maintaining its aspect ratio and padding the remainder.
    Returns the resized Image object.
    """
    original_width, original_height = image.size
    target_width, target_height = target_size

    # Calculate the scaling factor
    scale_factor = min(target_width / original_width, target_height / original_height)
    
    # Calculate the new dimensions of the image after scaling
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    # Resize the image with high quality
    resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create the new canvas (the 'letterbox')
    letterbox = Image.new('RGB', target_size, (128, 128, 128))  # Gray color
    
    # Calculate the position to paste the resized image
    # The image is now aligned to the upper-left corner
    paste_x = 0
    paste_y = 0   
    
    # Paste the resized image onto the canvas
    letterbox.paste(resized_img, (paste_x, paste_y))
    
    return letterbox

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize all images in a directory using the letterbox method.")
    parser.add_argument('--input-dir', type=str, required=True, help="Path to the directory containing input images.")
    parser.add_argument('--output-dir', type=str, required=True, help="Path to the directory to save the resized images.")
    parser.add_argument('--target-width', type=int, default=640, help="Target width for the output images. (default: 640)")
    parser.add_argument('--target-height', type=int, default=640, help="Target height for the output images. (default: 640)")
    
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get a list of all files in the input directory
    image_files = [f for f in os.listdir(args.input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print(f"No image files found in '{args.input_dir}'.")
    else:
        print(f"Found {len(image_files)} images to process.")
        for filename in image_files:
            try:
                # Construct full paths
                input_path = os.path.join(args.input_dir, filename)
                output_path = os.path.join(args.output_dir, filename)
                
                # Open the image and call the letterbox function
                with Image.open(input_path) as img:
                    resized_image = letterbox_image(img, target_size=(args.target_width, args.target_height))
                    resized_image.save(output_path)
                    print(f"Resized '{filename}' and saved to '{output_path}'")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")