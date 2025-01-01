from serpapi import GoogleSearch
import requests
import os
import time

"""
This python script was used to download images of each category from the google images..via serper api...(it's free for 100 searches)...
"""



# Your SerpApi API key
API_KEY = ""

# List of 100 plants/crops to search for
plant_names = [   
                 
              "Raw Cauliflower"
           
]

# Output directory to save images
output_dir = "plant_images"
os.makedirs(output_dir, exist_ok=True)

# Function to scrape and download images for a plant/crop
def download_images_for_plant(plant_name, num_images=250):
    print(f"Fetching images for: {plant_name}")
    
    # Create a subdirectory for the plant
    plant_dir = os.path.join(output_dir, plant_name)
    os.makedirs(plant_dir, exist_ok=True)

    # Initialize variables
    images_downloaded = 0
    start = 0  # Pagination start index for SerpApi

    while images_downloaded < num_images:
        # Search parameters
        params = {
            "api_key": API_KEY,
            "engine": "google",
            "q": plant_name,
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
            "tbm": "isch",
            "start": start,  # Pagination parameter
        }
        
        # Perform search
        search = GoogleSearch(params)
        results = search.get_dict()
        images = results.get("images_results", [])
        
        if not images:
            print(f"No more images found for {plant_name}.")
            break

        # Download images from the current batch
        for image in images:
            if images_downloaded >= num_images:
                break

            image_url = image.get("original")
            if image_url:
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(image_url, headers=headers, timeout=10)
                    response.raise_for_status()  # Check for HTTP request errors
                    
                    # Save the image in the plant-specific directory
                    image_path = os.path.join(plant_dir, f"{plant_name}_{images_downloaded + 1}.jpg")
                    with open(image_path, "wb") as file:
                        file.write(response.content)
                    
                    print(f"Saved: {image_path}")
                    images_downloaded += 1
                except Exception as e:
                    print(f"Failed to download {image_url}: {e}")
        
        # Increment start for the next batch of images
        start += 20  # Each page fetches 20 images by default

        # Avoid hitting rate limits
        time.sleep(2)

    print(f"Downloaded {images_downloaded} images for {plant_name}.")

# Loop through the list of plants and fetch images
for plant in plant_names:
    download_images_for_plant(plant, num_images=250)

print("Image collection complete.")
