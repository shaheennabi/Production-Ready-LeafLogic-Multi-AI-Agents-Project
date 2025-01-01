import os
import cv2
import numpy as np
from PIL import Image


"""
This code will check the duplicate images in the data, that is going to be annotated on Roboflow platform...
"""



def compute_image_hash(image_path, hash_size=8):
    image = Image.open(image_path).convert('L')
    resized_image = cv2.resize(np.array(image), (hash_size, hash_size))
    avg_intensity = np.mean(resized_image)
    hash_str = ''.join('1' if pixel > avg_intensity else '0' for pixel in resized_image.flatten())
    return hash_str.encode('utf-8')

def find_duplicates_using_hashes(dataset_path, hash_size=8):
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
                
                if img_hash not in hash_map:
                    hash_map[img_hash] = []
                hash_map[img_hash].append(img_path)

    duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}
    return duplicates

def remove_duplicates(image_dir, duplicates):
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
    duplicates = find_duplicates_using_hashes(dataset_path)
    
    if duplicates:
        print(f"Total duplicate groups found: {len(duplicates)}")
        removed_files = remove_duplicates(dataset_path, duplicates)
        print(f"Removed {len(removed_files)} duplicates.")
    else:
        print("No duplicates found.")

# Path to your dataset
dataset_path = r''

main(dataset_path)
