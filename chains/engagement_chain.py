from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_engagement_chain(openai_api_key):
    """
    Creates a higher-temperature chain that enhances factual responses with warmth.
    Uses simple single-input approach to avoid memory conflicts.
    """
    
    # Create memory - works fine with single input variable
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Define the engagement prompt template - single input variable
    engagement_template = """
You are a supportive EP supervisor enhancing a colleague's response.

CRITICAL RULES:
- ALWAYS include the full factual advice as the main content
- Add brief supportive framing around the factual advice
- Maximum ONE follow-up question
- Focus on the professional issue

Conversation history:
{chat_history}

Request to enhance:
{input}

Create a warm, supportive response that includes the factual advice and adds one relevant follow-up question:
"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template=engagement_template
    )
    
    # Create LLM with higher temperature for more empathetic responses
    llm = OpenAI(
        temperature=0.7,
        openai_api_key=openai_api_key,
        max_tokens=500
    )
    
    # Create chain WITH memory - no conflicts with single input
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    return chain