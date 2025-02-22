from taskflowai import WikipediaTools
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
import sys

class WikiArticles:
    @staticmethod
    def fetch_articles(cls):
        try:
            logging.info("Fetching articles using WikipediaTools.")
            articles = WikipediaTools.search_articles
            logging.info("Articles fetched successfully.")
            return articles
        except Exception as e:
            logging.info("Failed to fetch articles from Wikipedia.")
            raise CustomException(sys, e)