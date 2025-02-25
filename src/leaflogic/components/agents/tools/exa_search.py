import os
from dotenv import load_dotenv
from taskflowai import WebTools
from src.leaflogic.logger import logging
from typing import Optional


class ExaSearch:
    @staticmethod
    def search_web(query: str, num_results: Optional[int] = 5):
        """Perform a web search with a query and return the result."""
        try:
            if "EXA_API_KEY" not in os.environ:
                raise Exception("EXA_API_KEY environment variable is not set")

            search_result = WebTools.exa_search(query, int(num_results))
            return search_result

        except Exception as e:
            print(f"Search failed: {e}")
            return "No data available"
