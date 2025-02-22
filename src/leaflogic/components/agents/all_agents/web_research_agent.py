from taskflowai import Agent
from src.leaflogic.utils import LoadModel
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
import sys
from src.leaflogic.components.agents.tools.serper_search import SerperSearch
from src.leaflogic.components.agents.tools.search_articles import WikiArticles
from src.leaflogic.components.agents.tools.search_images import WikiImages

class WebResearchAgent:
    @staticmethod
    def initialize_web_research_agent():
        """
        Initializes and returns the Web Research Agent for comprehensive crop/plant research.
        """
        try:
            logging.info("Initializing Web Research Agent.")

            web_research_agent = Agent(
                role="Comprehensive Crop and Plant Research Agent",
                goal=(
                    "Gather and analyze complete information about a given crop or plant. "
                    "Fetch details such as scientific classification, historical background, "
                    "common and scientific names, geographical regions where it is grown, health benefits, "
                    "potential health effects, best season for consumption, and uses (e.g., culinary, medicinal, industrial). "
                    "Additionally, retrieve information on the ideal growth conditions, including soil fertility, nutrients, "
                    "temperature, water requirements, and a small guide on how it is cultivated. "
                    "Provide multiple high-quality images for better identification."
                ),
                attributes=(
                    "Thorough researcher, data-driven, botany expert, structured, visual-focused, "
                    "capable of synthesizing multi-source information for accurate reporting."
                ),
                llm=LoadModel.load_openai_model(),
                tools=[
                    SerperSearch.search_web(),  # Fetch web-based research details
                    WikiArticles.fetch_articles(),  # Retrieve historical and scientific details
                    WikiImages.search_images()  # Collect multiple related images
                ],
            )

            logging.info("Web Research Agent initialized successfully.")
            return web_research_agent

        except Exception as e:
            logging.error("Error initializing Web Research Agent")
            raise CustomException(sys, e)
