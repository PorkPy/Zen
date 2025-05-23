import streamlit as st
from chains.claude_ep_chain import create_claude_ep_chain
from db_manager import ReportDatabase
from report_generator import generate_professional_report
from report_sections import render_report_section
from ui_components import setup_page_config, setup_sidebar

# Set page config and styling
setup_page_config()

# Set Anthropic API Key from Streamlit Secrets
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

# Initialize session state
if "ep_chain" not in st.session_state:
    st.session_state.ep_chain = create_claude_ep_chain(anthropic_api_key)

if "db" not in st.session_state:
    st.session_state.db = ReportDatabase()

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

# Main UI
st.markdown('<h1 class="fancy-title">🦋 Jess</h1>', unsafe_allow_html=True)
st.caption("For Educational Psychologists")
st.write("")

# Setup sidebar
setup_sidebar(st.session_state.db, anthropic_api_key)

# Main content area
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
    else:
        # Show section progress and render current section
        progress = (st.session_state.current_section + 1) / len(ehc_sections)
        st.progress(progress)
        st.write(f"Section {st.session_state.current_section + 1} of {len(ehc_sections)}: **{ehc_sections[st.session_state.current_section]}**")
        
        # Render the current section
        render_report_section(
            ehc_sections[st.session_state.current_section], 
            st.session_state.current_section,
            len(ehc_sections),
            st.session_state.report_data,
            st.session_state.db,
            anthropic_api_key
        )
        
        # Exit button
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

    # Chat input
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