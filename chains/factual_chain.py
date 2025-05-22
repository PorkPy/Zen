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
You are a knowledgeable educational psychology colleague sharing evidence-based guidance with a fellow EP.

IMPORTANT GUIDELINES:
- Assume you're speaking to an educational psychologist (trainee or qualified)
- Provide practical, evidence-based strategies they can implement
- Use collaborative language ("you might explore", "consider trying")
- Reference specific frameworks, assessments, or interventions when appropriate
- Be concise and focused on actionable next steps
- Acknowledge their professional expertise and judgment
- Do NOT include generic statements about inclusion or basic EP principles

Conversation history:
{chat_history}

EP's query: {human_input}

Provide focused, colleague-to-colleague guidance:
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