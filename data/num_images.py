import os
from collections import defaultdict
"""
This python script was written to check the number of images in each category after removing duplicates and combining augmented images with original dataset....
"""




def count_images_in_combined_folder
(combined_dir):
    image_count = defaultdict(int)

    for category in os.listdir(combined_dir):
        category_path = os.path.join(combined_dir, category)
        if os.path.isdir(category_path):
            image_count[category] = len(os.listdir(category_path))

    return image_count

def main(combined_dir):
    image_count = count_images_in_combined_folder(combined_dir)
    print("Number of images in each category:")
    for category, count in image_count.items():
        print(f"{category}: {count} images")

# Path to your combined images directory
combined_dir = r''

main(combined_dir)
