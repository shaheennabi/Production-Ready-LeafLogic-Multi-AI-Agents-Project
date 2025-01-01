import os
import shutil
from collections import defaultdict
"""
This python code will combine the augmented images saved in different folder with original dataset, that will later be annotated 
on Roboflow platform by contributors of this project...
"""
def combine_images(src_augmented_dir, src_plant_dir, dest_combined_dir):
    if not os.path.exists(dest_combined_dir):
        os.makedirs(dest_combined_dir)

    for category in os.listdir(src_plant_dir):
        augmented_category_dir = os.path.join(src_augmented_dir, category)
        plant_category_dir = os.path.join(src_plant_dir, category)

        if not os.path.isdir(augmented_category_dir) or not os.path.isdir(plant_category_dir):
            continue
        
        print(f"Combining images for category: {category}")
        
        combined_category_dir = os.path.join(dest_combined_dir, category)
        if not os.path.exists(combined_category_dir):
            os.makedirs(combined_category_dir)

        augmented_images = set(os.listdir(augmented_category_dir))
        plant_images = set(os.listdir(plant_category_dir))
        
        for image_name in augmented_images.union(plant_images):
            src_augmented_image = os.path.join(augmented_category_dir, image_name)
            src_plant_image = os.path.join(plant_category_dir, image_name)
            dest_image = os.path.join(combined_category_dir, image_name)
            
            if image_name in plant_images and image_name in augmented_images:
                # Choose the plant image since we want plant images to be prioritized.
                shutil.copy2(src_plant_image, dest_image)
            elif image_name in plant_images:
                shutil.copy2(src_plant_image, dest_image)
            elif image_name in augmented_images:
                shutil.copy2(src_augmented_image, dest_image)

def main(src_augmented_dir, src_plant_dir, dest_combined_dir):
    combine_images(src_augmented_dir, src_plant_dir, dest_combined_dir)

# Paths to your directories
src_augmented_dir = r''
src_plant_dir = r''
dest_combined_dir = r''

main(src_augmented_dir, src_plant_dir, dest_combined_dir)
