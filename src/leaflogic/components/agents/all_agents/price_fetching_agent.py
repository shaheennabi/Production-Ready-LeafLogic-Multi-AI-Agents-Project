from taskflowai import Agent
from src.leaflogic.logger import logging
from src.leaflogic.utils import LoadModel
from src.leaflogic.components.agents.tools.serper_google_shopping_search import SerperShoppingSearch

class PriceFetchingAgent:
    @staticmethod
    def initialize_price_fetching_agent(query: str):
        """
        Initializes and returns the Crop or Plant Price Research Agent.

        Returns:
            Agent: A price research agent instance.
        """
        try:
            logging.info("Initializing Price Research Agent...")

            # Lazy-load model inside the Agent initialization
            price_fetching_agent = Agent(
                role="Price Research Agent",
                goal="Find and compare the best prices for crops and plants across different markets.",
                attributes="Cost-conscious, data-driven, and focused on accurate price comparisons.",
                llm=LoadModel.load_openai_model(),  # Model is only loaded when creating the agent
                tools=[SerperShoppingSearch.search_web],
            )

            logging.info("✅ Price Research Agent initialized successfully.")
            return price_fetching_agent

        except Exception as e:
            logging.error(f"❌ Failed to initialize Price Research Agent: {e}")
            raise RuntimeError(f"Failed to initialize Price Research Agent: {e}") from e
