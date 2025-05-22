from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_engagement_chain(openai_api_key):
    """
    Creates a higher-temperature chain that enhances factual responses with warmth,
    EP-specific support, and thoughtful follow-up questions.
    This acts as an "editor" that takes the factual response and makes it more supportive.
    """
    
    # Define the engagement prompt template
    engagement_template = """
You are a supportive EP supervisor enhancing a colleague's response.

CRITICAL RULES:
- ALWAYS include the full factual response as the main content
- ONLY add brief supportive framing around the factual advice
- DO NOT replace the factual content with just wellbeing concerns
- Maximum ONE follow-up question
- Focus on the professional issue, not just self-care

Your task: Take the factual response below and enhance it by adding a warm introduction and ONE follow-up question.

Original EP query: {human_input}

Factual response to include: {factual_content}

Format your response like this:
[Brief warm acknowledgment] [Include the full factual response] [One relevant follow-up question]
"""

    prompt = PromptTemplate(
        input_variables=["human_input", "factual_content"],
        template=engagement_template
    )
    
    # Create LLM with higher temperature for more empathetic responses
    llm = OpenAI(
        temperature=0.7,  # Higher for more varied, empathetic responses
        openai_api_key=openai_api_key,
        max_tokens=500  # Needs to be larger since it's including the full factual response + enhancements
    )
    
    # Create chain WITHOUT memory to avoid input key conflicts
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False
        # Note: No memory here since we have multiple input variables
    )
    
    return chain