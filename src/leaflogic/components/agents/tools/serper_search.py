import os
from dotenv import load_dotenv
from taskflowai import WebTools
from src.leaflogic.logger import logging
from typing import Optional

class SerperSearch:
    @staticmethod
    def search_web(query: str, num_results: Optional[int] = 5):
        """Perform a web search using the Serper API.

        Args:
            query (str): The search query.
            num_results (Optional[int]): Number of results to fetch (default: 5).

        Returns:
            dict: The search results from the API.

        Raises:
            RuntimeError: If the search fails.
        """
        try:
            # Load API key from .env
            load_dotenv()
            api_key = os.getenv("SERPER_API_KEY")

            if not api_key:
                raise ValueError("SERPER_API_KEY is not set in the environment.")

            logging.info(f"Initiating web search for query: '{query}' with {num_results} results.")

            # Ensure num_results is an integer
            search_result = WebTools.serper_search(query=query,search_type="search", num_results=int(num_results))

            if search_result:
                logging.info(f"Successfully retrieved {len(search_result)} results for query: '{query}'")
            else:
                logging.warning(f"No results found for query: '{query}'")

            return search_result
        except Exception as e:
            logging.error(f"❌ Failed to perform web search for query '{query}': {e}")
            raise RuntimeError(f"Failed to perform web Serper search: {e}") from e
