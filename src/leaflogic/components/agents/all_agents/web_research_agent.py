from taskflowai import Agent
from src.leaflogic.utils import LoadModel
from src.leaflogic.logger import logging
from src.leaflogic.components.agents.tools.exa_search import ExaSearch
from src.leaflogic.components.agents.tools.search_articles import WikiArticles
from src.leaflogic.components.agents.tools.search_images import WikiImages


class WebResearchAgent:
    @staticmethod
    def initialize_web_research_agent():
        """
        Initializes and returns the Crop or Plant Web Research Agent.
        """
        try:
            web_research_agent = Agent(
                role="Crop and Plant Research Agent",
                goal="Collect key details about a crop or plant, including classification, uses, growth conditions, and images.",
                attributes="Accurate, structured, and data-driven.",
                llm=LoadModel.load_openai_model(),
                tools=[
                    WikiArticles.fetch_articles,
                    WikiImages.search_images,
                    ExaSearch.search_web
                ],
            )

            return web_research_agent

        except Exception as e:
            raise Exception(f"Failed to initialize Web Research Agent: {str(e)}")