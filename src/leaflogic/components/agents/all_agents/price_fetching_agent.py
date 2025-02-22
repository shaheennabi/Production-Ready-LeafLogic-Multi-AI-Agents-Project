from taskflowai import Agent
from src.leaflogic.utils import LoadModel
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
import sys
from src.leaflogic.components.agents.tools.serper_google_shopping_search import SerperSearchShopping

class PriceFetchingAgent:
    @staticmethod
    def initialize_price_fetching_agent():
        """
        Initializes and returns the Crop or Plant Price Research Agent.
        """
        try:
            logging.info("Initializing the Crop or Plant Price Research Agent.")

            price_fetching_agent = Agent(
                role="Crop or Plant Price Research Agent",
                goal=(
                    "Fetch and compare the best available prices for crops and plants. "
                    "Determine cost per kg or lb based on the user's location, ensuring the most "
                    "cost-effective and high-quality options."
                ),
                attributes=(
                    "Cost-conscious, detail-oriented, region-aware, data-driven, "
                    "capable of finding the best market deals for crops and plants."
                ),
                llm=LoadModel.load_openai_model(),
                tools=[
                    SerperSearchShopping.search_web(search_type="shopping"),  # Fetches prices from Google Shopping
                ],
            )

            logging.info("Crop or Plant Price Research Agent initialized successfully.")
            return price_fetching_agent

        except Exception as e:
            logging.error("Error initializing Crop or Plant Price Research Agent")
            raise CustomException(sys, e)
