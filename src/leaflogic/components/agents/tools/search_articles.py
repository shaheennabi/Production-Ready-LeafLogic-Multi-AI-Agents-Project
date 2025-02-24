from taskflowai import WikipediaTools
from src.leaflogic.logger import logging
import sys


class WikiArticles:
    @staticmethod
    def fetch_articles(query: str):
        """Fetches Wikipedia articles for the given query."""
        try:
            logging.info(f"Fetching Wikipedia articles for query: {query}")
            articles = WikipediaTools.search_articles(query=query)
            
            if articles:
                logging.info(f"Successfully retrieved {len(articles)} articles for '{query}'")
            else:
                logging.warning(f"No articles found for query: {query}")
                
            return articles
        except Exception as e:
            logging.error(f"Error fetching Wikipedia articles for query '{query}': {e}")
            raise RuntimeError(f"Error fetching Wikipedia articles: {e}") from e
