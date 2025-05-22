from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_engagement_chain(openai_api_key):
    """
    Creates a higher-temperature chain focused on empathetic engagement
    and generating thoughtful follow-up questions.
    """
    
    # Create memory for this chain
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Define the engagement prompt template
    engagement_template = """
You are an empathetic special education mentor who adds warmth and generates thoughtful follow-up questions.

Your role is to:
- Add empathetic framing to responses
- Generate 1-2 relevant follow-up questions that dig deeper
- Show understanding of the emotional/practical challenges
- Suggest related areas to explore

Given this factual content: {factual_content}

And this original question: {human_input}

Conversation history:
{chat_history}

Add empathetic engagement and generate thoughtful follow-up questions:
"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "factual_content"],
        template=engagement_template
    )
    
    # Create LLM with higher temperature for more creative/empathetic responses
    llm = OpenAI(
        temperature=0.7,  # Higher for more varied, empathetic responses
        openai_api_key=openai_api_key,
        max_tokens=200  # Shorter for just engagement elements
    )
    
    # Create and return the chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    return chain