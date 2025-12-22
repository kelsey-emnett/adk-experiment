import os
from dotenv import load_dotenv

load_dotenv(override=True)

from google.adk.agents import SequentialAgent, Agent, LlmAgent
from google.adk.models.registry import _llm_registry_dict, LLMRegistry
from google.adk.models.lite_llm import LiteLlm
from app.wikipedia import wikipedia_full_text

# Register Azure OpenAI pattern with LiteLlm (ADK doesn't include this by default)
_llm_registry_dict['azure/.*'] = LiteLlm
LLMRegistry.resolve.cache_clear()

model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


wikipedia_agent = Agent(
    name="basic_search_agent",
    model=f"azure/{model_deployment}",
    description="Agent to search and print content from a Wikipedia page.",
    instruction="I can search Wikipedia for you and print the first result's page content. Do not summarize content.",
    tools=[wikipedia_full_text],
    output_key="wikipedia_content",
)

summarize_wikipedia_content_agent = LlmAgent(
    name="wikipedia_summarizer_agent",
    model=f"azure/{model_deployment}",
    instruction="""
    You are an expert summarizer that gives a 5-8 sentence summary of a wikipedia article given
    the wikipedia article's content. Summarize the article given the following output:
    
    # Wikipedia Article Content: {wikipedia_content}.
    """,
    description="Summarize the wikipedia article content using a language model.",
    output_key="wikipedia_summary",
)

root_agent = SequentialAgent(
    name="wikipedia_summarizer_workflow",
    sub_agents=[wikipedia_agent, summarize_wikipedia_content_agent],
)