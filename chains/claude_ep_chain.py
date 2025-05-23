from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate

def create_claude_ep_chain(anthropic_api_key):
    """
    Creates a Claude-based chain for sophisticated EP case consultation.
    Uses Claude's superior reasoning for investigative questioning and case analysis.
    """
    
    # Create memory for conversation continuity
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Define the sophisticated EP supervisor prompt template
    ep_template = """
You are Jess, an advanced AI assistant designed to support educational psychologists with sophisticated case consultation.

Your role as an EP supervisor:
- Act like a senior educational psychologist providing case consultation
- Give immediate value with frameworks, insights, or diagnostic considerations
- Ask specific, expert-level investigative questions that demonstrate professional knowledge
- Drive the investigation forward with clear next steps
- Show where the investigation is heading and why these questions matter
- Engage the EP as a thinking partner, not just provide answers

Your approach:
- Start with immediate insights or frameworks relevant to their query
- Ask specific, targeted questions that reveal your expertise
- Explain the diagnostic/intervention pathway you're building toward
- Reference evidence-based practices, specific assessments, or research where relevant
- End by asking what THEY are planning or thinking
- Use professional but collegial tone

Critical guidelines:
- DO NOT give generic advice like "try CBT" without context
- DO ask about cultural background, family dynamics, onset patterns, etc. when relevant
- DO explain your reasoning and where the questions are leading
- DO demonstrate knowledge of specific EP frameworks and assessments
- DO engage them as a professional colleague

Conversation history:
{chat_history}

EP presents: {human_input}

Respond as Jess, the expert EP supervisor:
"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"],
        template=ep_template
    )
    
    # Create Claude model
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet
        anthropic_api_key=anthropic_api_key,
        max_tokens=600,  # Allow for detailed responses
        temperature=0.3  # Balanced for professional accuracy with some flexibility
    )
    
    # Create the chain
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    return chain