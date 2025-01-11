import os
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

"""
This code identifies and removes duplicate images in the dataset 
by calculating perceptual hashes for the images.
"""

def compute_image_hash(image_path, hash_size=8):
    """
    Compute a perceptual hash for an image.
    
    Parameters:
    - image_path: Path to the image file.
    - hash_size: Size of the hash (default is 8x8).
    
    Returns:
    - Encoded binary hash string for the image.
    """
    try:
        # Open the image and convert to grayscale
        image = Image.open(image_path).convert('L')
        # Resize the image
        resized_image = cv2.resize(np.array(image), (hash_size, hash_size))
        # Calculate the average intensity
        avg_intensity = np.mean(resized_image)
        # Generate hash based on pixel intensity
        hash_str = ''.join('1' if pixel > avg_intensity else '0' for pixel in resized_image.flatten())
        return hash_str.encode('utf-8')
    except UnidentifiedImageError:
        print(f"Unidentified image file: {image_path}. Skipping...")
        return None

def find_duplicates_using_hashes(dataset_path, hash_size=8):
    """
    Find duplicate images in the dataset using perceptual hashing.

    Parameters:
    - dataset_path: Path to the dataset.
    - hash_size: Size of the hash for perceptual hashing.

    Returns:
    - Dictionary containing duplicate image groups.
    """
    hash_map = {}
    for category in os.listdir(dataset_path):
        category_path = os.path.join(dataset_path, category)
        if not os.path.isdir(category_path):
            continue
        print(f"Processing category: {category}")
        
        for filename in os.listdir(category_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(category_path, filename)
                img_hash = compute_image_hash(img_path, hash_size=hash_size)
                if img_hash:
                    if img_hash not in hash_map:
                        hash_map[img_hash] = []
                    hash_map[img_hash].append(img_path)

    # Filter hash_map to only include duplicates
    duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}
    return duplicates

def remove_duplicates(duplicates):
    """
    Remove duplicate images, keeping only the first occurrence.

    Parameters:
    - duplicates: Dictionary containing duplicate image groups.

    Returns:
    - List of removed file paths.
    """
    removed_files = []
    for img_hash, duplicate_paths in duplicates.items():
        for path in duplicate_paths[1:]:
            if os.path.exists(path):
                print(f"Removing duplicate: {path}")
                try:
                    os.remove(path)
                    removed_files.append(path)
                except Exception as e:
                    print(f"Failed to remove {path}: {e}")
            else:
                print(f"File not found: {path}")
    return removed_files

def main(dataset_path):
    """
    Main function to identify and remove duplicates in the dataset.

    Parameters:
    - dataset_path: Path to the dataset.
    """
    duplicates = find_duplicates_using_hashes(dataset_path)
    
    if duplicates:
        print(f"Total duplicate groups found: {len(duplicates)}")
        for img_hash, duplicate_paths in duplicates.items():
            print(f"Hash: {img_hash.decode('utf-8')} -> Files: {duplicate_paths}")
        
        removed_files = remove_duplicates(duplicates)
        print(f"Removed {len(removed_files)} duplicates.")
    else:
        print("No duplicates found.")

# Path to your dataset
dataset_path = r''
main(dataset_path)
