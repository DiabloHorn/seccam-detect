import os
import random
import shutil
import argparse

def split_dataset(images_path, labels_path, output_dir, train_ratio, val_ratio, test_ratio):
    """
    Splits an image dataset and its corresponding labels into train, val, and test sets.
    """
    # Check that ratios sum to 1.0
    if not (train_ratio + val_ratio + test_ratio) == 1.0:
        raise ValueError("The sum of train, val, and test ratios must be 1.0.")

    # Create the new directories
    os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'test'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'test'), exist_ok=True)

    # Get all image and label files
    image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(image_files)
    
    # Calculate the number of files for each split
    num_images = len(image_files)
    num_train = int(num_images * train_ratio)
    num_val = int(num_images * val_ratio)
    
    # Slice the file list to get the sets
    train_files = image_files[:num_train]
    val_files = image_files[num_train:num_train + num_val]
    test_files = image_files[num_train + num_val:]

    def copy_files(file_list, folder):
        for f in file_list:
            label_file = f.rsplit('.', 1)[0] + '.txt'
            shutil.copy(os.path.join(images_path, f), os.path.join(output_dir, 'images', folder, f))
            if os.path.exists(os.path.join(labels_path, label_file)):
                shutil.copy(os.path.join(labels_path, label_file), os.path.join(output_dir, 'labels', folder, label_file))
            else:
                print(f"Warning: Label file for {f} not found.")

    print(f"Splitting {num_images} images with ratios: {train_ratio}, {val_ratio}, {test_ratio}")
    copy_files(train_files, 'train')
    print(f"Copied {len(train_files)} files to the training set.")
    copy_files(val_files, 'val')
    print(f"Copied {len(val_files)} files to the validation set.")
    copy_files(test_files, 'test')
    print(f"Copied {len(test_files)} files to the test set.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Splits an image dataset for YOLO training.")
    parser.add_argument('--images-path', type=str, required=True, help="Path to the directory containing all images.")
    parser.add_argument('--labels-path', type=str, required=True, help="Path to the directory containing all label files.")
    parser.add_argument('--output-dir', type=str, required=True, help="Path for the output directory to store the split dataset.")
    parser.add_argument('--train-ratio', type=float, default=0.8, help="Ratio for the training set. (default: 0.8)")
    parser.add_argument('--val-ratio', type=float, default=0.1, help="Ratio for the validation set. (default: 0.1)")
    parser.add_argument('--test-ratio', type=float, default=0.1, help="Ratio for the test set. (default: 0.1)")

    args = parser.parse_args()
    
    split_dataset(
        args.images_path,
        args.labels_path,
        args.output_dir,
        args.train_ratio,
        args.val_ratio,
        args.test_ratio
    )