from taskflowai import WikipediaTools
from src.leaflogic.logger import logging
import sys


class WikiImages:
    @staticmethod
    def search_images(query: str):
        """Search for images on Wikipedia based on the given query."""
        try:
            logging.info(f"Searching for Wikipedia images for query: {query}")
            images = WikipediaTools.search_images(query=query)
            
            if images:
                logging.info(f"Successfully retrieved {len(images)} images for '{query}'")
            else:
                logging.warning(f"No images found for query: {query}")

            return images
        except Exception as e:
            logging.error(f"Error fetching Wikipedia images for query '{query}': {e}")
            raise RuntimeError(f"Error fetching Wikipedia images: {e}") from e
