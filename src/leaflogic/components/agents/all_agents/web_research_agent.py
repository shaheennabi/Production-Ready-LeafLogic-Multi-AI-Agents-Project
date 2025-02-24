from taskflowai import Agent
from src.leaflogic.utils import LoadModel
from src.leaflogic.logger import logging
from src.leaflogic.components.agents.tools.serper_search import SerperSearch
from src.leaflogic.components.agents.tools.search_articles import WikiArticles
from src.leaflogic.components.agents.tools.search_images import WikiImages

class WebResearchAgent:
    @staticmethod
    def initialize_web_research_agent():
        """
        Initializes and returns the Crop or Plant Web Research Agent.
        """
        try:
            logging.info("Initializing Web Research Agent...")

            # Lazy-load model only when agent is actually created
            web_research_agent = Agent(
                role="Crop and Plant Research Agent",
                goal="Collect key details about a crop or plant, including classification, uses, growth conditions, and images.",
                attributes="Accurate, structured, and data-driven.",
                llm=LoadModel.load_openai_model(),  
                tools=[
                    WikiArticles.fetch_articles,
                    WikiImages.search_images,
                    SerperSearch.search_web
                ],
            )

            logging.info("✅ Web Research Agent initialized successfully.")
            return web_research_agent

        except Exception as e:
            logging.error(f"❌ Failed to initialize Web Research Agent: {e}")
            raise RuntimeError(f"Failed to initialize Web Research Agent: {e}") from e
