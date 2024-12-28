import os
import cv2

# Root directory containing all plant categories
root_dir = "data/plant_images"

# Font settings for OpenCV
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 255)  # Red color in BGR format
font_thickness = 2

# Print the root directory for debugging
print(f"Root directory: {root_dir}")

# Iterate over all categories inside the plant_images folder
for category in os.listdir(root_dir):
    category_path = os.path.join(root_dir, category)
    print(f"Category path: {category_path}")
    
    if os.path.isdir(category_path):  # Check if it's a directory
        print(f"Processing category: {category}")
        for image_name in os.listdir(category_path):
            image_path = os.path.join(category_path, image_name)
            if image_name.endswith(('.jpg', '.png', '.jpeg')):  # Check for valid image extensions
                try:
                    # Read the image
                    img = cv2.imread(image_path)
                    if img is None:
                        print(f"Could not read image: {image_name}")
                        continue
                    
                    # Add the category name to the top-left corner
                    position = (10, 30)  # Top-left corner position (x, y)
                    cv2.putText(img, category, position, font, font_scale, font_color, font_thickness)

                    # Save the updated image
                    cv2.imwrite(image_path, img)
                    print(f"Updated image: {image_path}")
                except Exception as e:
                    print(f"Error processing {image_name}: {e}")

print("Processing complete!")
