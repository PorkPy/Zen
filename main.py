import streamlit as st
from chains.claude_ep_chain import create_claude_ep_chain
from db_manager import ReportDatabase

# Set page config first
st.set_page_config(page_title="Jess - For Educational Psychologists", page_icon="🅹")

# Custom CSS for fancy title and sidebar styling
st.markdown("""
<style>
.fancy-title {
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(45deg, #FF69B4, #FFB6C1, #DDA0DD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0;
    cursor: pointer;
}

/* Fix excessive white space in sidebar */
.stSidebar > div:first-child {
    padding-top: 1rem !important;
}

.stSidebar .stButton {
    margin-bottom: 0.5rem !important;
    margin-top: 0 !important;
}

/* Make sidebar more compact overall */
.stSidebar .element-container {
    margin-bottom: 0.5rem !important;
}

/* Style the new conversation button to match title */
.stSidebar button[kind="primary"] {
    background: linear-gradient(45deg, #FF69B4, #FFB6C1, #DDA0DD) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 20px !important;
}

/* Report display styling */
.report-section {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #FF69B4;
}

.report-header {
    color: #2c3e50;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Set Anthropic API Key from Streamlit Secrets
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

# Initialize chain in session state
if "ep_chain" not in st.session_state:
    st.session_state.ep_chain = create_claude_ep_chain(anthropic_api_key)

# Initialize database
if "db" not in st.session_state:
    st.session_state.db = ReportDatabase()

# Initialize message history and resources in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mentioned_resources" not in st.session_state:
    st.session_state.mentioned_resources = []

# Initialize report writing state
if "report_mode" not in st.session_state:
    st.session_state.report_mode = None
if "report_data" not in st.session_state:
    st.session_state.report_data = {}
if "current_section" not in st.session_state:
    st.session_state.current_section = 0
if "current_report_id" not in st.session_state:
    st.session_state.current_report_id = None
if "generated_report" not in st.session_state:
    st.session_state.generated_report = None

# Resource detection function
def detect_resources(text):
    """Detect mentioned EP resources in text and return relevant links"""
    resources = {}
    text_lower = text.lower()
    
    # Assessment tools
    if "sensory profile" in text_lower or "sensory profile-2" in text_lower:
        resources["Sensory Profile-2"] = "https://www.pearsonassessments.com/store/usassessments/en/Store/Professional-Assessments/Behavior/Sensory-Profile-2/p/100000822.html"
    
    if "ados" in text_lower or "ados-2" in text_lower:
        resources["ADOS-2"] = "https://www.ados-2.com/"
    
    if "wisc" in text_lower:
        resources["WISC-V"] = "https://www.pearsonassessments.com/store/usassessments/en/Store/Professional-Assessments/Cognition-%26-Neuro/Wechsler-Intelligence-Scale-for-Children-%7C-Fifth-Edition/p/100000771.html"
    
    # Frameworks and approaches
    if "functional behavioral assessment" in text_lower or "fba" in text_lower:
        resources["Functional Behavioral Assessment"] = "https://www.pbis.org/topics/functional-behavioral-assessment"
    
    if "cbt" in text_lower or "cognitive behavioral" in text_lower:
        resources["CBT Resources"] = "https://www.babcp.com/"
    
    if "attachment" in text_lower:
        resources["Attachment Theory"] = "https://www.attachmentparenting.org/"
    
    if "pica" in text_lower:
        resources["PICA Information"] = "https://www.nationaleatingdisorders.org/pica"
    
    return resources

def generate_professional_report(report_data, anthropic_api_key):
    """Generate a professional EHC report from the collected data"""
    
    # Create a specialized chain for report generation
    from langchain_anthropic import ChatAnthropic
    from langchain.prompts import PromptTemplate
    
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

# Streamlit UI - Clean title without button functionality (button now in sidebar)
st.markdown('<h1 class="fancy-title">🦋 Jess</h1>', unsafe_allow_html=True)
st.caption("For Educational Psychologists")
st.write("")  # Add some spacing

# Sidebar with resources and info  
with st.sidebar:
    # Start fresh button at top with better styling
    if st.button("Start Fresh", type="primary", use_container_width=True, help="Begin a new conversation"):
        st.session_state.messages = []
        st.session_state.mentioned_resources = []
        st.session_state.ep_chain = create_claude_ep_chain(anthropic_api_key)
        st.rerun()
    
    # About Jess with butterfly icon and nature theme explanation
    with st.expander("🦋 About Jess"):
        st.write("Jess provides expert EP case consultation using advanced AI. Ask about complex cases, diagnostic frameworks, interventions, and professional development.")
        
        st.write("**How to use:**")
        st.write("• Describe cases naturally - Jess will ask probing questions")
        st.write("• Reference cultural, developmental, and systemic factors") 
        st.write("• Request specific assessments, frameworks, or evidence")
        
        st.markdown("---")
        st.write("**Our Nature Theme:**")
        st.write("🦋 **Butterfly (Jess)** - transformation, growth, guidance")
        st.write("🐝 **Bee (User)** - busy, productive, working hard (like EPs!)")
        st.write("Both are pollinators who help things grow and flourish, just like EP work! 🌸")
    
    st.header("📚 Professional Bodies")
    with st.expander("UK Organizations"):
        st.markdown("- [BPS Division of Educational & Child Psychology](https://www.bps.org.uk/member-networks/division-educational-and-child-psychology)")
        st.markdown("- [Association of Educational Psychologists](https://www.aep.org.uk/)")
    
    st.header("📋 Key Resources")
    with st.expander("Legislation & Guidelines"):
        st.markdown("- [SEND Code of Practice](https://www.gov.uk/government/publications/send-code-of-practice-0-to-25)")
        st.markdown("- [NICE Guidelines](https://www.nice.org.uk/)")
        st.markdown("- [Mental Capacity Act](https://www.legislation.gov.uk/ukpga/2005/9/contents)")
    
    with st.expander("Derby City Council"):
        st.markdown("- [Derby's SEND Local Offer](https://www.derby.gov.uk/education-and-learning/derbys-send-local-offer/)")
        st.markdown("- [Derby SEND Strategy](https://www.derby.gov.uk/education-and-learning/derbys-send-local-offer/send-inclusion-derby/our-send-strategy/)")
        st.markdown("- [Choosing Schools with SEND](https://www.derby.gov.uk/education-and-learning/derbys-send-local-offer/education/choosing-a-school-for-a-child-with-send/)")
    
    with st.expander("Special Schools & Placements"):
        st.markdown("- [Independent Schools Council](https://www.isc.co.uk/)")
        st.markdown("- [National Association of Special Schools](https://www.nasschools.org.uk/)")
        st.markdown("- [IPSEA - Legal Advice](https://www.ipsea.org.uk/)")
    
    with st.expander("Assessment Tools"):
        st.markdown("- [Sensory Profile-2](https://www.pearsonassessments.com/store/usassessments/en/Store/Professional-Assessments/Behavior/Sensory-Profile-2/p/100000822.html)")
        st.markdown("- [ADOS-2 Overview](https://www.ados-2.com/)")
        st.markdown("- [WISC-V Information](https://www.pearsonassessments.com/store/usassessments/en/Store/Professional-Assessments/Cognition-%26-Neuro/Wechsler-Intelligence-Scale-for-Children-%7C-Fifth-Edition/p/100000771.html)")
    
    with st.expander("Frameworks & Interventions"):
        st.markdown("- [Functional Behavioral Assessment](https://www.pbis.org/topics/functional-behavioral-assessment)")
        st.markdown("- [CBT Resources](https://www.babcp.com/)")
        st.markdown("- [Attachment Theory](https://www.attachmentparenting.org/)")
    
    st.header("📝 Report Writing")
    with st.expander("EHC Assessment Reports"):
        if st.button("📋 Start New EHC Report", use_container_width=True):
            st.session_state.report_mode = "ehc_assessment"
            st.session_state.report_data = {}
            st.session_state.current_section = 0
            st.session_state.current_report_id = None
            st.session_state.generated_report = None
            st.rerun()
        
        # Show recent reports
        st.write("**Recent Reports:**")
        recent_reports = st.session_state.db.list_reports(5)
        
        if recent_reports:
            for report in recent_reports:
                status = "✅ Complete" if report["is_completed"] else "🔄 In Progress"
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"{report['child_name']} - {status}")
                    st.caption(f"Updated: {report['updated_at'][:16]} | ID: {report['id']}")
                
                with col2:
                    if st.button("📖 Load", key=f"load_{report['id']}", help="Continue this report"):
                        # Load the report
                        loaded_report = st.session_state.db.load_report(report['id'])
                        if loaded_report:
                            st.session_state.report_mode = loaded_report["report_type"]
                            st.session_state.report_data = loaded_report["data"]
                            st.session_state.current_section = loaded_report["current_section"]
                            st.session_state.current_report_id = report['id']
                            st.session_state.generated_report = None
                            st.rerun()
        else:
            st.caption("No saved reports yet")

# Main content area - check if in report mode
if st.session_state.report_mode == "ehc_assessment":
    # EHC Assessment Report Writing Mode
    st.markdown("### 📋 EHC Assessment Report")
    st.info("💡 **Write naturally!** Use bullet points, notes, or full sentences - whatever works for you. Jess will structure and format everything into a professional report at the end.")
    
    # Report sections
    ehc_sections = [
        "Child Information & Referral",
        "Background & History", 
        "Assessment Methods & Observations",
        "Cognitive Assessment",
        "Educational Attainment",
        "Social, Emotional & Behavioral Factors",
        "Psychological Formulation",
        "Recommendations & Provision"
    ]
    
    # Check if we're viewing the generated report
    if st.session_state.generated_report:
        st.markdown("### 📄 Generated Professional Report")
        
        # Display the generated report
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.generated_report)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.button("📝 Edit Report Data"):
                st.session_state.generated_report = None
                st.rerun()
        
        with col2:
            if st.button("🔄 Regenerate Report"):
                with st.spinner("Regenerating professional report..."):
                    st.session_state.generated_report = generate_professional_report(
                        st.session_state.report_data, anthropic_api_key
                    )
                st.rerun()
        
        with col3:
            # Download button
            st.download_button(
                label="📥 Download Report",
                data=st.session_state.generated_report,
                file_name=f"EHC_Report_{st.session_state.report_data.get('child_name', 'Unknown')}_{st.session_state.current_report_id}.txt",
                mime="text/plain"
            )
        
        with col4:
            if st.button("🏠 Back to Main"):
                st.session_state.report_mode = None
                st.session_state.generated_report = None
                st.rerun()
        
        return  # Exit early when showing generated report
    
    # Progress indicator
    progress = (st.session_state.current_section + 1) / len(ehc_sections)
    st.progress(progress)
    st.write(f"Section {st.session_state.current_section + 1} of {len(ehc_sections)}: **{ehc_sections[st.session_state.current_section]}**")
    
    # Section-specific questions
    current_section = ehc_sections[st.session_state.current_section]
    
    if current_section == "Child Information & Referral":
        st.write("Let's start with basic information about the child and referral:")
        st.caption("💭 *Write however feels natural - notes, bullet points, full sentences. I'll format it properly later.*")
        name = st.text_input("Child's name (or initials):", 
                            value=st.session_state.report_data.get("child_name", ""), 
                            key="child_name")
        age = st.text_input("Age and date of birth:", 
                           value=st.session_state.report_data.get("child_age", ""), 
                           key="child_age")
        school = st.text_input("School/setting:", 
                              value=st.session_state.report_data.get("child_school", ""), 
                              key="child_school")
        referral_reason = st.text_area("Reason for referral:", 
                                      value=st.session_state.report_data.get("referral_reason", ""),
                                      key="referral_reason", 
                                      help="Just jot down the key concerns - bullet points are fine!")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section", disabled=True):  # Disabled on first section
                pass
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "child_name": name,
                    "child_age": age, 
                    "child_school": school,
                    "referral_reason": referral_reason
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                # Auto-save current section data
                st.session_state.report_data.update({
                    "child_name": name,
                    "child_age": age, 
                    "child_school": school,
                    "referral_reason": referral_reason
                })
                
                # Generate or use existing report ID
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        name or "Unknown", "ehc_assessment"
                    )
                
                # Save to database
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    name or "Unknown",
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
                
    elif current_section == "Background & History":
        st.write("Tell me about the child's background and developmental history:")
        st.caption("💭 *Don't worry about perfect sentences - capture what you know however works for you.*")
        family_background = st.text_area("Family background and home circumstances:", 
                                        value=st.session_state.report_data.get("family_background", ""),
                                        key="family_background",
                                        help="Quick notes are fine - family structure, any relevant circumstances")
        developmental_history = st.text_area("Early developmental history (milestones, concerns):", 
                                           value=st.session_state.report_data.get("developmental_history", ""),
                                           key="developmental_history",
                                           help="Any developmental info you have - bullet points work great")
        medical_history = st.text_area("Relevant medical history:", 
                                     value=st.session_state.report_data.get("medical_history", ""),
                                     key="medical_history",
                                     help="Just note any relevant medical information")
        previous_support = st.text_area("Previous educational support and interventions:", 
                                      value=st.session_state.report_data.get("previous_support", ""),
                                      key="previous_support",
                                      help="List what's been tried before - informal notes are perfect")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "academic_levels": academic_levels,
                    "curriculum_access": curriculum_access,
                    "academic_strengths": academic_strengths,
                    "learning_barriers": learning_barriers
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "academic_levels": academic_levels,
                    "curriculum_access": curriculum_access,
                    "academic_strengths": academic_strengths,
                    "learning_barriers": learning_barriers
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
                
    elif current_section == "Social, Emotional & Behavioral Factors":
        st.write("Social, emotional and behavioral observations:")
        st.caption("💭 *Describe the child's social interactions, emotional regulation, and behavior patterns.*")
        
        social_skills = st.text_area("Social skills and peer relationships:", 
                                   value=st.session_state.report_data.get("social_skills", ""),
                                   key="social_skills",
                                   help="How does the child interact with peers and adults?")
        
        emotional_regulation = st.text_area("Emotional development and regulation:", 
                                          value=st.session_state.report_data.get("emotional_regulation", ""),
                                          key="emotional_regulation",
                                          help="How does the child manage emotions and stress?")
        
        behavioral_patterns = st.text_area("Behavioral observations and patterns:", 
                                         value=st.session_state.report_data.get("behavioral_patterns", ""),
                                         key="behavioral_patterns",
                                         help="Any concerning or notable behavioral patterns?")
        
        self_esteem = st.text_area("Self-esteem and confidence:", 
                                 value=st.session_state.report_data.get("self_esteem", ""),
                                 key="self_esteem",
                                 help="How does the child view themselves and their abilities?")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "social_skills": social_skills,
                    "emotional_regulation": emotional_regulation,
                    "behavioral_patterns": behavioral_patterns,
                    "self_esteem": self_esteem
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "social_skills": social_skills,
                    "emotional_regulation": emotional_regulation,
                    "behavioral_patterns": behavioral_patterns,
                    "self_esteem": self_esteem
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
                
    elif current_section == "Psychological Formulation":
        st.write("Your psychological formulation and professional analysis:")
        st.caption("💭 *This is your expert interpretation - write your professional thoughts naturally.*")
        
        formulation = st.text_area("Psychological formulation:", 
                                 value=st.session_state.report_data.get("formulation", ""),
                                 key="formulation",
                                 help="Your professional analysis of what's happening for this child",
                                 height=150)
        
        contributing_factors = st.text_area("Contributing factors and underlying causes:", 
                                          value=st.session_state.report_data.get("contributing_factors", ""),
                                          key="contributing_factors",
                                          help="What factors are contributing to the child's difficulties?")
        
        prognosis = st.text_area("Prognosis and future considerations:", 
                                value=st.session_state.report_data.get("prognosis", ""),
                                key="prognosis",
                                help="What's the outlook? What should be considered going forward?")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "formulation": formulation,
                    "contributing_factors": contributing_factors,
                    "prognosis": prognosis
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "formulation": formulation,
                    "contributing_factors": contributing_factors,
                    "prognosis": prognosis
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
                
    elif current_section == "Recommendations & Provision":
        st.write("Recommendations and provision needed:")
        st.caption("💭 *Specify what support the child needs - be as detailed or brief as works for you.*")
        
        educational_provision = st.text_area("Educational provision recommendations:", 
                                            value=st.session_state.report_data.get("educational_provision", ""),
                                            key="educational_provision",
                                            help="What educational support/placement is needed?",
                                            height=120)
        
        interventions = st.text_area("Specific interventions and strategies:", 
                                   value=st.session_state.report_data.get("interventions", ""),
                                   key="interventions",
                                   help="What specific interventions should be implemented?",
                                   height=120)
        
        professional_support = st.text_area("Professional support required:", 
                                           value=st.session_state.report_data.get("professional_support", ""),
                                           key="professional_support",
                                           help="What other professionals need to be involved?")
        
        monitoring = st.text_area("Review and monitoring arrangements:", 
                                value=st.session_state.report_data.get("monitoring", ""),
                                key="monitoring",
                                help="How should progress be monitored and reviewed?")
        
        # Navigation buttons - Final section
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("🎯 Generate Professional Report"):
                # Save current data first
                st.session_state.report_data.update({
                    "educational_provision": educational_provision,
                    "interventions": interventions,
                    "professional_support": professional_support,
                    "monitoring": monitoring
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                # Mark as completed and save
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section,
                    is_completed=True
                )
                
                # Generate the professional report
                with st.spinner("🦋 Jess is transforming your notes into a professional EHC report..."):
                    st.session_state.generated_report = generate_professional_report(
                        st.session_state.report_data, anthropic_api_key
                    )
                
                st.success(f"🎉 Professional report generated! ID: {st.session_state.current_report_id}")
                st.balloons()
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "educational_provision": educational_provision,
                    "interventions": interventions,
                    "professional_support": professional_support,
                    "monitoring": monitoring
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
    
    # Add spacing before exit button
    st.markdown("---")
    st.write("**Report Controls:**")
    if st.button("🚪 Exit Report (without saving)", type="secondary"):
        st.session_state.report_mode = None
        st.session_state.report_data = {}
        st.session_state.current_section = 0
        st.session_state.generated_report = None
        st.rerun()

else:
    # Normal consultation mode
    # Display chat messages with nature-themed avatars
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="🐝"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🦋"):
                st.write(message["content"])

    # Chat input (natural Streamlit position - no extra buttons!)
    if user_input := st.chat_input("Ask Jess about EP practice, cases, or professional development..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message with bee avatar
        with st.chat_message("user", avatar="🐝"):
            st.write(user_input)
        
        # Generate AI response with butterfly avatar
        with st.chat_message("assistant", avatar="🦋"):
            with st.spinner("Jess is thinking through this with you..."):
                final_response = st.session_state.ep_chain.run(human_input=user_input)
                st.write(final_response)
                
                # Detect and add new resources
                new_resources = detect_resources(final_response)
                for name, link in new_resources.items():
                    if name not in [r["name"] for r in st.session_state.mentioned_resources]:
                        st.session_state.mentioned_resources.append({"name": name, "link": link})
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_response})

# Show recently mentioned resources below the input (only in consultation mode)
if st.session_state.report_mode is None and st.session_state.mentioned_resources:
    st.markdown("---")
    st.subheader("📎 Resources mentioned in this conversation")
    
    # Display in columns for better layout
    cols = st.columns(2)
    for i, resource in enumerate(st.session_state.mentioned_resources[-6:]):  # Show last 6
        with cols[i % 2]:
            st.markdown(f"[{resource['name']}]({resource['link']})")session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "family_background": family_background,
                    "developmental_history": developmental_history,
                    "medical_history": medical_history,
                    "previous_support": previous_support
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "family_background": family_background,
                    "developmental_history": developmental_history,
                    "medical_history": medical_history,
                    "previous_support": previous_support
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
                
    elif current_section == "Assessment Methods & Observations":
        st.write("Details about your assessment approach and observations:")
        st.caption("💭 *Just capture your observations naturally - I'll turn them into professional report language.*")
        assessment_methods = st.text_area("Assessment methods used (tests, observations, interviews):", 
                                        value=st.session_state.report_data.get("assessment_methods", ""),
                                        key="assessment_methods",
                                        help="List what you did - WISC-V, observations, etc.")
        classroom_observation = st.text_area("Classroom observation findings:", 
                                           value=st.session_state.report_data.get("classroom_observation", ""),
                                           key="classroom_observation",
                                           help="What did you notice? Jot down key observations")
        child_interaction = st.text_area("Direct interaction with child - behavior and engagement:", 
                                       value=st.session_state.report_data.get("child_interaction", ""),
                                       key="child_interaction",
                                       help="How was the child during assessment? Informal notes fine")
        child_views = st.text_area("Child's views and perspectives:", 
                                 value=st.session_state.report_data.get("child_views", ""),
                                 key="child_views",
                                 help="What did the child say? Direct quotes or paraphrasing both work")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "assessment_methods": assessment_methods,
                    "classroom_observation": classroom_observation,
                    "child_interaction": child_interaction,
                    "child_views": child_views
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "assessment_methods": assessment_methods,
                    "classroom_observation": classroom_observation,
                    "child_interaction": child_interaction,
                    "child_views": child_views
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
                
    elif current_section == "Cognitive Assessment":
        st.write("Cognitive assessment results and findings:")
        st.caption("💭 *Record test results, observations during testing, and what they mean. Don't worry about formatting.*")
        
        cognitive_tests = st.text_area("Cognitive tests administered:", 
                                     value=st.session_state.report_data.get("cognitive_tests", ""),
                                     key="cognitive_tests",
                                     help="WISC-V, BPVS, etc. - just list what you used")
        
        cognitive_scores = st.text_area("Test scores and index scores:", 
                                      value=st.session_state.report_data.get("cognitive_scores", ""),
                                      key="cognitive_scores",
                                      help="Raw scores, standard scores, percentiles - whatever format works",
                                      height=100)
        
        cognitive_strengths = st.text_area("Cognitive strengths observed:", 
                                         value=st.session_state.report_data.get("cognitive_strengths", ""),
                                         key="cognitive_strengths",
                                         help="What did the child do well? Areas of strength?")
        
        cognitive_difficulties = st.text_area("Areas of cognitive difficulty:", 
                                            value=st.session_state.report_data.get("cognitive_difficulties", ""),
                                            key="cognitive_difficulties",
                                            help="Where did they struggle? What patterns emerged?")
        
        testing_behavior = st.text_area("Behavior and approach during testing:", 
                                      value=st.session_state.report_data.get("testing_behavior", ""),
                                      key="testing_behavior",
                                      help="How did they engage? Any factors affecting performance?")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.session_state.current_section -= 1
                st.rerun()
        with col2:
            if st.button("Next Section →"):
                st.session_state.report_data.update({
                    "cognitive_tests": cognitive_tests,
                    "cognitive_scores": cognitive_scores,
                    "cognitive_strengths": cognitive_strengths,
                    "cognitive_difficulties": cognitive_difficulties,
                    "testing_behavior": testing_behavior
                })
                st.session_state.current_section += 1
                st.rerun()
        with col3:
            if st.button("💾 Save & Exit"):
                st.session_state.report_data.update({
                    "cognitive_tests": cognitive_tests,
                    "cognitive_scores": cognitive_scores,
                    "cognitive_strengths": cognitive_strengths,
                    "cognitive_difficulties": cognitive_difficulties,
                    "testing_behavior": testing_behavior
                })
                
                if not st.session_state.current_report_id:
                    st.session_state.current_report_id = st.session_state.db.generate_report_id(
                        st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
                    )
                
                st.session_state.db.save_report(
                    st.session_state.current_report_id,
                    "ehc_assessment",
                    st.session_state.report_data.get("child_name", "Unknown"),
                    st.session_state.report_data,
                    st.session_state.current_section
                )
                
                st.session_state.report_mode = None
                st.success(f"Report saved! ID: {st.session_state.current_report_id}")
                st.rerun()
    
    elif current_section == "Educational Attainment":
        st.write("Educational attainment and academic performance:")
        st.caption("💭 *Note current academic levels, progress, and curriculum access naturally.*")
        
        academic_levels = st.text_area("Current academic levels and attainment:", 
                                     value=st.session_state.report_data.get("academic_levels", ""),
                                     key="academic_levels",
                                     help="Reading age, maths levels, National Curriculum levels, etc.")
        
        curriculum_access = st.text_area("Access to curriculum and learning:", 
                                        value=st.session_state.report_data.get("curriculum_access", ""),
                                        key="curriculum_access",
                                        help="How well can they access mainstream curriculum?")
        
        academic_strengths = st.text_area("Academic strengths and interests:", 
                                        value=st.session_state.report_data.get("academic_strengths", ""),
                                        key="academic_strengths",
                                        help="What subjects/areas does the child excel in?")
        
        learning_barriers = st.text_area("Barriers to learning and progress:", 
                                        value=st.session_state.report_data.get("learning_barriers", ""),
                                        key="learning_barriers",
                                        help="What's preventing optimal academic progress?")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous Section"):
                st.