import os

def rename_images_in_folders(base_path):
    """
    Rename images inside folders based on their folder (category) name.

    Parameters:
        base_path (str): Path to the main folder containing category folders.
    """
    # Ensure the base_path exists
    if not os.path.exists(base_path):
        print(f"Error: Path '{base_path}' does not exist.")
        return

    # Iterate over each category folder in the base path
    for category_folder in os.listdir(base_path):
        category_path = os.path.join(base_path, category_folder)

        # Check if it's a directory
        if os.path.isdir(category_path):
            print(f"Processing folder: {category_folder}")

            # Initialize counter for naming images
            counter = 1

            # Iterate over each file in the category folder
            for file_name in os.listdir(category_path):
                file_path = os.path.join(category_path, file_name)

                # Check if it's a file
                if os.path.isfile(file_path):
                    # Get the file extension
                    _, ext = os.path.splitext(file_name)

                    # Construct new name with category and counter
                    new_name = f"{category_folder}{counter}{ext}"
                    new_file_path = os.path.join(category_path, new_name)

                    # Rename the file
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {file_name} -> {new_name}")

                    # Increment counter
                    counter += 1

if __name__ == "__main__":
    # Define the base folder path (update this to your actual folder path)
    base_folder_path = ""

    # Call the function to rename images
    rename_images_in_folders(base_folder_path)
