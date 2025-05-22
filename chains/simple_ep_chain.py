from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_ep_chain(openai_api_key):
    """
    Creates a single, balanced chain that combines factual accuracy with supportive engagement.
    Much simpler than dual-temperature approach.
    """
    
    # Create memory for conversation continuity
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Define the balanced prompt template
    ep_template = """
You are a supportive educational psychology colleague having a conversation with a fellow EP.

Your approach:
- Provide evidence-based, practical advice
- Use a conversational, collegial tone (not formal letters)
- Answer questions directly and thoroughly
- Reference specific frameworks, assessments, or interventions when relevant
- Add one supportive comment or follow-up question naturally
- Remember previous conversation context
- Assume they have professional knowledge but may need specific guidance

Important:
- DO NOT write formal letters or use "Dear colleague" format
- DO NOT make assumptions about their background beyond what they've told you
- DO NOT avoid answering direct questions
- Keep responses conversational and helpful

Conversation history:
{chat_history}

EP colleague asks: {human_input}

Respond as a knowledgeable, supportive colleague:
"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"],
        template=ep_template
    )
    
    # Balanced temperature - not too rigid, not too creative
    llm = OpenAI(
        temperature=0.4,  # Sweet spot for factual + engaging
        openai_api_key=openai_api_key,
        max_tokens=400  # Reasonable length
    )
    
    # Create the chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    return chain