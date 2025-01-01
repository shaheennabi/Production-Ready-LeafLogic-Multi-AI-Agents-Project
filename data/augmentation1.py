import cv2
import os
import random
import numpy as np
"""This code is for data augmentation of images, because data is low in quantity we have to add augmentation technique, 
below the python code will randomly pick images from the original image dataset and flip, rotatate, add noise etc to images ..

"""
# Define augmentation functions
def flip_image(image):
    """Flip the image randomly along x, y, or both axes."""
    return cv2.flip(image, random.choice([-1, 0, 1]))

def rotate_image(image):
    """Rotate the image by a random angle between -45 and 45 degrees."""
    angle = random.randint(-45, 45)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))

def change_brightness(image):
    """Adjust the brightness of the image randomly."""
    value = random.randint(-50, 50)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def add_noise(image):
    """Add random Gaussian noise to the image."""
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
    return cv2.add(image, noise)

def zoom_image(image):
    """Apply random zoom effect on the image."""
    zoom_factor = random.uniform(1.1, 1.5)
    (h, w) = image.shape[:2]
    x1 = int(w * (1 - 1 / zoom_factor) / 2)
    y1 = int(h * (1 - 1 / zoom_factor) / 2)
    cropped = image[y1:h-y1, x1:w-x1]
    if cropped.shape[0] == 0 or cropped.shape[1] == 0:
        return image  # Avoid issues with extreme zooms
    return cv2.resize(cropped, (w, h))

# Main function for augmentation
def augment_category(input_folder, output_folder, target_count=250):
    """Augment images in a specific category to reach the target count."""
    os.makedirs(output_folder, exist_ok=True)
    valid_extensions = ('.jpg', '.png', '.jpeg', '.bmp', '.tiff')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_extensions)]
    existing_count = len(images)

    if existing_count >= target_count:
        print(f"Category '{os.path.basename(input_folder)}' already has {existing_count} images.")
        return

    augment_functions = [flip_image, rotate_image, change_brightness, add_noise, zoom_image]
    images = [os.path.join(input_folder, img) for img in images]
    random.shuffle(images)

    augmented_count = 0
    while len(images) + augmented_count < target_count:
        original_image_path = random.choice(images)
        original_image = cv2.imread(original_image_path)

        if original_image is None:
            print(f"Warning: Unable to read image '{original_image_path}'. Skipping.")
            continue

        try:
            augmented_image = random.choice(augment_functions)(original_image)
            new_filename = f"aug_{len(images) + augmented_count + 1}.jpg"
            output_path = os.path.join(output_folder, new_filename)
            cv2.imwrite(output_path, augmented_image)
            augmented_count += 1
        except Exception as e:
            print(f"Error augmenting image '{original_image_path}': {e}")

    print(f"Augmented '{os.path.basename(input_folder)}' to {target_count} images.")

# Run the augmentation process
def main(input_base_folder, output_base_folder, target_count=250):
    """Augment all categories in the input base folder."""
    categories = [d for d in os.listdir(input_base_folder) if os.path.isdir(os.path.join(input_base_folder, d))]
    for category in categories:
        input_folder = os.path.join(input_base_folder, category)
        output_folder = os.path.join(output_base_folder, category)
        augment_category(input_folder, output_folder, target_count)

# Define paths
input_base_folder = "plant_images"  # Path to original categories
output_base_folder = "augmented_plant_images"  # Path to save augmented data
target_count = 250  # Target number of images per category

# Execute
if __name__ == "__main__":
    main(input_base_folder, output_base_folder, target_count)
