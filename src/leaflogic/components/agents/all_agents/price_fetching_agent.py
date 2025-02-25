from taskflowai import Agent
from src.leaflogic.logger import logging
from src.leaflogic.utils import LoadModel
from src.leaflogic.components.agents.tools.exa_shopping_search import ExaShoppingSearch
from src.leaflogic.components.agents.tools.serper_shopping_search import SerperShoppingSearch


class PriceFetchingAgent:
    @staticmethod
    def initialize_price_fetching_agent(query: str):
        """
        Initializes and returns the Crop or Plant Price Research Agent.

        Args:
            query (str): The plant name or keyword for price research.

        Returns:
            Agent: A price research agent instance.
        """
        try:
            price_fetching_agent = Agent(
                role="Price Research Agent",
                goal="Find and compare the best prices for crops and plants across different markets.",
                attributes="Cost-conscious, data-driven, and focused on accurate price comparisons.",
                llm=LoadModel.load_openai_model(),
                tools=[ExaShoppingSearch.search_web, SerperShoppingSearch.search_web],
            )

            return price_fetching_agent

        except Exception as e:
            raise Exception(f"Error initializing Price Research Agent: {str(e)}")
