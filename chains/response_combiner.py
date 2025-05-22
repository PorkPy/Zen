def combine_responses(factual_response, engagement_response):
    """
    Combines factual and engagement responses into a cohesive, natural response.
    
    Args:
        factual_response (str): The factual, low-temperature response
        engagement_response (str): The empathetic, high-temperature response with follow-ups
    
    Returns:
        str: Combined response that flows naturally
    """
    
    # Basic combination - you can make this more sophisticated later
    combined = f"{factual_response}\n\n{engagement_response}"
    
    return combined.strip()

def extract_follow_up_questions(engagement_response):
    """
    Extracts follow-up questions from the engagement response.
    This could be enhanced with more sophisticated parsing.
    
    Args:
        engagement_response (str): The engagement response containing questions
        
    Returns:
        list: List of follow-up questions
    """
    
    # Simple extraction - look for sentences ending with '?'
    questions = []
    sentences = engagement_response.split('.')
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence.endswith('?'):
            questions.append(sentence)
    
    return questions

def format_professional_response(factual_content, empathy_content, follow_ups=None):
    """
    More sophisticated response formatting for professional use.
    
    Args:
        factual_content (str): Core factual information
        empathy_content (str): Empathetic framing
        follow_ups (list, optional): List of follow-up questions
        
    Returns:
        str: Professionally formatted response
    """
    
    response_parts = []
    
    # Add the main factual content
    response_parts.append(factual_content)
    
    # Add empathetic elements if provided
    if empathy_content:
        response_parts.append(f"\n{empathy_content}")
    
    # Add follow-up questions in a structured way
    if follow_ups and len(follow_ups) > 0:
        response_parts.append("\n**Some questions to consider:**")
        for i, question in enumerate(follow_ups, 1):
            response_parts.append(f"{i}. {question}")
    
    return "\n".join(response_parts)