import streamlit as st
from chains.claude_ep_chain import create_claude_ep_chain

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
</style>
""", unsafe_allow_html=True)

# Set Anthropic API Key from Streamlit Secrets
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

# Initialize chain in session state
if "ep_chain" not in st.session_state:
    st.session_state.ep_chain = create_claude_ep_chain(anthropic_api_key)

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
        if st.button("📋 Start EHC Assessment Report", use_container_width=True):
            st.session_state.report_mode = "ehc_assessment"
            st.session_state.report_data = {}
            st.session_state.current_section = 0
            st.rerun()

# Main content area - check if in report mode
if st.session_state.report_mode == "ehc_assessment":
    # EHC Assessment Report Writing Mode
    st.markdown("### 📋 EHC Assessment Report")
    st.write("I'll guide you through writing an EHC Assessment Report with structured questions.")
    
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
    
    # Progress indicator
    progress = (st.session_state.current_section + 1) / len(ehc_sections)
    st.progress(progress)
    st.write(f"Section {st.session_state.current_section + 1} of {len(ehc_sections)}: **{ehc_sections[st.session_state.current_section]}**")
    
    # Section-specific questions
    current_section = ehc_sections[st.session_state.current_section]
    
    if current_section == "Child Information & Referral":
        st.write("Let's start with basic information about the child and referral:")
        name = st.text_input("Child's name (or initials):", key="child_name")
        age = st.text_input("Age and date of birth:", key="child_age")
        school = st.text_input("School/setting:", key="child_school")
        referral_reason = st.text_area("Reason for referral:", key="referral_reason")
        
        if st.button("Next Section →"):
            st.session_state.report_data.update({
                "child_name": name,
                "child_age": age, 
                "child_school": school,
                "referral_reason": referral_reason
            })
            st.session_state.current_section += 1
            st.rerun()
    
    # Exit report mode
    if st.button("← Back to Consultation Mode"):
        st.session_state.report_mode = None
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
            st.markdown(f"[{resource['name']}]({resource['link']})")