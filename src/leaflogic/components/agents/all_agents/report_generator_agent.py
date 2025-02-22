from taskflowai import Agent
from src.leaflogic.utils import LoadModel
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
import sys

class ReportGeneratorAgent:
    @staticmethod
    def initialize_report_generator_agent():
        """
        Initializes and returns the Comprehensive Crop/Plant Report Generator Agent.
        """
        try:
            logging.info("Initializing the Report Generator Agent.")

            report_generator_agent = Agent(
                role="Comprehensive Crop/Plant Report Generator",
                goal=(
                    "Generate a high-quality, structured summary of a plant/crop, "
                    "integrating research insights with detailed price analysis. "
                    "Provide scientific classification, historical significance, "
                    "optimal growth conditions, health benefits, potential risks, "
                    "nutrient & soil requirements, and the best available market prices "
                    "per kg/lb based on location. Highlight price trends, cost variations, "
                    "and most economical purchasing options."
                ),
                attributes=(
                    "Analytical, structured, price-focused, research-driven, "
                    "capable of multi-source synthesis, and optimized for high-quality reporting."
                ),
                llm=LoadModel.load_openai_model()  # Uses LLM memory for integrating details
            )

            logging.info("Report Generator Agent initialized successfully.")
            return report_generator_agent

        except Exception as e:
            logging.error("Error initializing Report Generator Agent")
            raise CustomException(sys, e)
