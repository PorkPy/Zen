from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_factual_chain(openai_api_key):
    """
    Creates a low-temperature chain focused on factual, evidence-based responses
    for special educational needs questions.
    """
    
    # Create memory for this chain
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Define the factual prompt template
    factual_template = """
You are a knowledgeable special education consultant providing evidence-based guidance.

IMPORTANT GUIDELINES:
- Provide factual, actionable advice based on best practices
- Reference specific strategies, interventions, or frameworks when appropriate
- Be concise and direct - avoid generic statements about inclusion being important
- Focus on practical implementation
- If you mention research, be specific about the approach or study type
- Do NOT include generic statements about "inclusion being important" or similar filler

Conversation history:
{chat_history}

Question: {human_input}

Provide a focused, practical response:
"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"],
        template=factual_template
    )
    
    # Create LLM with low temperature for factual accuracy
    llm = OpenAI(
        temperature=0.1,  # Very low for factual consistency
        openai_api_key=openai_api_key,
        max_tokens=300  # Keep responses focused
    )
    
    # Create and return the chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    return chain