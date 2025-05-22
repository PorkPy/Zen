from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def create_factual_chain(openai_api_key):
    """
    Creates a low-temperature chain focused on factual, evidence-based responses.
    This chain has no memory since it's just generating advice that gets enhanced.
    """
    
    # Define the factual prompt template (no conversation history needed)
    factual_template = """
You are a knowledgeable educational psychology colleague providing evidence-based guidance.

IMPORTANT GUIDELINES:
- Assume you're speaking to an educational psychologist (trainee or qualified)
- Provide practical, evidence-based strategies they can implement
- Use collaborative language ("you might explore", "consider trying")
- Reference specific frameworks, assessments, or interventions when appropriate
- Be concise and focused on actionable next steps
- Acknowledge their professional expertise and judgment
- Do NOT include generic statements about inclusion or basic EP principles

EP's query: {human_input}

Provide focused, colleague-to-colleague guidance:
"""

    prompt = PromptTemplate(
        input_variables=["human_input"],
        template=factual_template
    )
    
    # Create LLM with low temperature for factual accuracy
    llm = OpenAI(
        temperature=0.1,  # Very low for factual consistency
        openai_api_key=openai_api_key,
        max_tokens=350  # Increased to prevent cutoffs
    )
    
    # Create chain WITHOUT memory (just pure advice generation)
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False
    )
    
    return chain