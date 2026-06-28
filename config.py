import os

from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_community.tools import TavilySearchResults

load_dotenv("config.env")

COHERE_API_KEY = os.getenv["COHERE_API_KEY"]
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

assert TAVILY_API_KEY


llm = ChatCohere(
    model="command-nightly",
    temperature=0.3
)

search_tool = TavilySearchResults(
    max_results=5
)