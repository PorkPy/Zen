from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_engagement_chain(openai_api_key):
    """
    Creates a higher-temperature chain that enhances factual responses with warmth,
    EP-specific support, and thoughtful follow-up questions.
    This chain maintains conversation memory since it generates the final responses.
    """
    
    # Create memory for this chain since it handles the conversation
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Define the engagement prompt template
    engagement_template = """
You are a supportive EP supervisor enhancing a colleague's response.

CRITICAL RULES:
- ALWAYS include the full factual response as the main content
- ONLY add brief supportive framing around the factual advice
- DO NOT replace the factual content with just wellbeing concerns
- Maximum ONE follow-up question
- Focus on the professional issue, not just self-care
- Remember previous conversation context

Conversation history:
{chat_history}

Current EP query: {human_input}

Factual response to include: {factual_content}

Create a warm, supportive response that includes the factual advice and adds one relevant follow-up question:
"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "factual_content"],
        template=engagement_template
    )
    
    # Create LLM with higher temperature for more empathetic responses
    llm = OpenAI(
        temperature=0.7,  # Higher for more varied, empathetic responses
        openai_api_key=openai_api_key,
        max_tokens=500  # Needs to be larger since it's including the full factual response + enhancements
    )
    
    # Create chain WITH memory since this generates the final conversation
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    return chain