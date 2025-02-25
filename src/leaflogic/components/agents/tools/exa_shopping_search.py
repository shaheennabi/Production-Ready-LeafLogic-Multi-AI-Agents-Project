import os
from dotenv import load_dotenv
from taskflowai import WebTools
from src.leaflogic.logger import logging
from typing import Optional

import os
from taskflowai import WebTools
from typing import Optional

class ExaShoppingSearch:
    @staticmethod
    def search_web(query: str, num_results: Optional[int] = 5):
        """Perform a web search for shopping results with a given query."""
        try:
            if "EXA_API_KEY" not in os.environ:
                raise Exception("EXA_API_KEY environment variable is not set")

            
            search_result = WebTools.exa_search(
                queries=query,  
                search_type="keyword",
                num_results=int(num_results)
            )
            return search_result

        except Exception as e:
            return f"Search failed: {e}"  
