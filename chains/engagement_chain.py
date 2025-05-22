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
You are a supportive EP supervisor/mentor enhancing a colleague's response with warmth and professional support.

Your role is to:
- Take the factual response and add empathetic, supportive framing
- Acknowledge the emotional demands of EP work
- Add 1-2 thoughtful follow-up questions that respect their professional expertise
- Include gentle reminders about self-care when appropriate
- Maintain the professional tone while adding warmth

Original EP query: {human_input}

Factual response to enhance: {factual_content}

Enhance this response by adding warmth, professional support, and thoughtful follow-ups while keeping it as one cohesive response:
"""

    prompt = PromptTemplate(
        input_variables=["human_input", "factual_content"],
        template=engagement_template
    )
    
    # Create LLM with higher temperature for more empathetic responses
    llm = OpenAI(
        temperature=0.7,  # Higher for more varied, empathetic responses
        openai_api_key=openai_api_key,
        max_tokens=250  # Slightly longer for enhanced response
    )
    
    # Create chain WITHOUT memory to avoid input key conflicts
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False
        # Note: No memory here since we have multiple input variables
    )
    
    return chain