import os
from imagededup.methods import PHash

def find_and_remove_duplicates(dataset_path):
    """
    Detect and optionally remove duplicate images in each category of the dataset.

    Parameters:
    - dataset_path: Path to the dataset containing category folders.
    """
    phasher = PHash()
    
    for category in os.listdir(dataset_path):
        category_path = os.path.join(dataset_path, category)
        
        # Skip non-directory files
        if not os.path.isdir(category_path):
            continue
        
        print(f"Processing category: {category}")
        
        # Generate encodings for images in the category
        encodings = phasher.encode_images(image_dir=category_path)
        
        # Find duplicates based on perceptual hash
        duplicates = phasher.find_duplicates(encoding_map=encodings, min_similarity_threshold=0.9)
        
        # Report duplicates
        for key, duplicate_list in duplicates.items():
            if len(duplicate_list) > 1:
                print(f"Duplicate found in {category}: {key} -> {duplicate_list}")
                
        # Optional: Remove duplicates
        for key, duplicate_list in duplicates.items():
            # Keep the first instance and remove others
            for duplicate in duplicate_list[1:]:
                duplicate_path = os.path.join(category_path, duplicate)
                if os.path.exists(duplicate_path):
                    os.remove(duplicate_path)
                    print(f"Removed duplicate: {duplicate_path}")

# Path to your dataset
dataset_path = r'C:\Users\mailm\Documents\Production-Ready-LeafLogic-Internship-Project\data\augmented_plant_images'

find_and_remove_duplicates(dataset_path)
