from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate

def generate_professional_report(report_data, anthropic_api_key):
    """Generate a professional EHC report from the collected data"""
    
    # Create a specialized chain for report generation
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        anthropic_api_key=anthropic_api_key,
        max_tokens=3000,
        temperature=0.2
    )
    
    # Comprehensive report generation prompt
    report_prompt = PromptTemplate(
        input_variables=["report_data"],
        template="""
You are an expert Educational Psychologist writing a professional EHC Assessment Report. 

Transform the following informal notes and data into a comprehensive, professionally written EHC Assessment Report. 

The report should be:
- Written in professional, clear language appropriate for statutory assessment
- Well-structured with clear headings
- Evidence-based and objective
- Suitable for sharing with parents, schools, and local authority
- Following standard EHC report format and conventions

Report Data:
{report_data}

Generate a complete professional EHC Assessment Report with these sections:

1. CHILD INFORMATION & REFERRAL DETAILS
2. BACKGROUND AND DEVELOPMENTAL HISTORY  
3. ASSESSMENT METHODS AND OBSERVATIONS
4. COGNITIVE ASSESSMENT FINDINGS
5. EDUCATIONAL ATTAINMENT AND PROGRESS
6. SOCIAL, EMOTIONAL AND BEHAVIOURAL FACTORS
7. PSYCHOLOGICAL FORMULATION
8. RECOMMENDATIONS AND PROVISION

Format each section clearly with headings. Write in third person. Use professional language throughout while maintaining accessibility for all readers including parents.

Professional EHC Assessment Report:
"""
    )
    
    # Format the report data for the prompt
    formatted_data = ""
    for key, value in report_data.items():
        if value and value.strip():
            formatted_data += f"{key.replace('_', ' ').title()}: {value}\n\n"
    
    # Generate the report
    response = llm.invoke(report_prompt.format(report_data=formatted_data))
    return response.content