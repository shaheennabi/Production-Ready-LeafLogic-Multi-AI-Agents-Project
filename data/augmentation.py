import cv2
import os
import random
import numpy as np

# Define augmentation functions
def flip_image(image):
    return cv2.flip(image, random.choice([-1, 0, 1]))

def rotate_image(image):
    angle = random.randint(-45, 45)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))

def change_brightness(image):
    value = random.randint(-50, 50)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def add_noise(image):
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
    return cv2.add(image, noise)

def zoom_image(image):
    zoom_factor = random.uniform(1.1, 1.5)
    (h, w) = image.shape[:2]
    x1 = int(w * (1 - 1 / zoom_factor) / 2)
    y1 = int(h * (1 - 1 / zoom_factor) / 2)
    cropped = image[y1:h-y1, x1:w-x1]
    return cv2.resize(cropped, (w, h))

# Main function for augmentation
def augment_category(input_folder, output_folder, target_count=250):
    os.makedirs(output_folder, exist_ok=True)
    images = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    existing_count = len(images)

    if existing_count >= target_count:
        print(f"Category {os.path.basename(input_folder)} already has {existing_count} images.")
        return

    augment_functions = [flip_image, rotate_image, change_brightness, add_noise, zoom_image]
    images = [os.path.join(input_folder, img) for img in images]
    random.shuffle(images)

    while len(images) < target_count:
        original_image = cv2.imread(random.choice(images))
        augmented_image = random.choice(augment_functions)(original_image)
        new_filename = f"aug_{len(images)}.jpg"
        cv2.imwrite(os.path.join(output_folder, new_filename), augmented_image)
        images.append(os.path.join(output_folder, new_filename))

    print(f"Augmented {os.path.basename(input_folder)} to {target_count} images.")

# Run the augmentation process
def main(input_base_folder, output_base_folder, target_count=250):
    categories = [d for d in os.listdir(input_base_folder) if os.path.isdir(os.path.join(input_base_folder, d))]
    for category in categories:
        input_folder = os.path.join(input_base_folder, category)
        output_folder = os.path.join(output_base_folder, category)
        augment_category(input_folder, output_folder, target_count)

# Define paths
input_base_folder = "data/plant_images"  # Path to original categories
output_base_folder = "data/augmented_plant_images"  # Path to save augmented data
target_count = 250  # Target number of images per category

# Execute
main(input_base_folder, output_base_folder, target_count)
