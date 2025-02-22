from taskflowai import WebTools
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
import sys

class SerperSearchShopping:
    @staticmethod
    def search_web(cls):
        try:
            logging.info("Performing web shopping search using SerperSearch shopping.")
            search = WebTools.serper_search(search_type="shopping")
            logging.info("Web search shpping completed successfully.")
            return search
        except Exception as e:
            logging.info("Failed to perform web search shopping.")
            raise CustomException(sys, e)