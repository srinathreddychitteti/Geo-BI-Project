import os
from dotenv import load_dotenv
from typing import List, Dict, Any

from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

# Load environment variables from .env file
load_dotenv()

def create_llm_chain() -> Runnable:
    """
    Initializes and returns the LangChain runnable sequence (chain).
    
    The chain consists of a prompt template, a Hugging Face LLM, and an
    output parser.

    Returns:
        A configured LangChain runnable object.
    """
    # Initialize the LLM endpoint from Hugging Face
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        task="text-generation",
        temperature=0.7,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        timeout=120
    )
    llm = ChatHuggingFace(llm=llm_endpoint)

    # Define the prompt structure for the analysis task
    prompt_template = """
    You are a professional Geo-Spatial Business Intelligence Analyst.
    Your task is to provide a concise, data-driven analysis for a marketing manager.

    Here is a list of businesses and their available data:
    {business_data}

    Based *only* on the data provided, perform the following analysis:
    1.  **Summary:** Briefly summarize the market for '{business_type}' in '{location}'.
    2.  **Market Landscape:** Comment on the density and distribution of these businesses.
    3.  **Conclusion:** Provide a short, professional conclusion with a strategic recommendation.

    Provide the analysis in a clean, easy-to-read markdown format.
    """

    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["business_data", "business_type", "location"]
    )

    # Chain the components together using the LangChain Expression Language (LCEL)
    return prompt | llm | StrOutputParser()

# Initialize the chain once when the module is loaded
chain = create_llm_chain()

def generate_analysis(business_data: List[Dict[str, Any]], business_type: str, location: str) -> str:
    """
    Generates a market analysis using the LLM chain.

    Args:
        business_data: A list of dictionaries, where each dict contains business info.
        business_type: The type of business being analyzed.
        location: The location of the analysis.

    Returns:
        A string containing the formatted analysis from the LLM, or an error message.
    """
    if not isinstance(business_data, list) or not business_data:
        return "Not enough data to perform analysis or an error occurred during data fetching."
    
    # Format the business data into a simple string for the prompt
    data_string = "\n".join([f"- Name: {b.get('name', 'N/A')}, Type: {b.get('type', 'N/A')}" for b in business_data])
    
    # Invoke the LLM chain with the formatted data
    try:
        result = chain.invoke({
            "business_data": data_string,
            "business_type": business_type,
            "location": location
        })
        return result
    except Exception as e:
        logging.error(f"LLM chain invocation failed: {e}")
        return "Error: The AI model failed to generate an analysis. Please try again later."