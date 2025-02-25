## Serper api was down during the creation of this project, so I gave agent the access to ExaShopping as second option:
import os
from dotenv import load_dotenv
from taskflowai import WebTools
from typing import Optional

class SerperShoppingSearch:
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
            # Load environment variables from .env file
            load_dotenv()

            # Retrieve API key
            api_key = os.getenv("SERPER_API_KEY")
            if not api_key:
                raise ValueError("SERPER_API_KEY is not set in the environment or .env file.")

            # Perform web search
            return WebTools.serper_search(query=query, search_type="shopping", num_results=int(num_results))

        except Exception as e:
            raise RuntimeError(f"Failed to perform web Serper search: {e}") from e
