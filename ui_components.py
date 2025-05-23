import streamlit as st
from chains.claude_ep_chain import create_claude_ep_chain

def setup_page_config():
    """Set up page configuration and custom CSS"""
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

def setup_sidebar(db, anthropic_api_key):
    """Set up the sidebar with all its components"""
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
            recent_reports = db.list_reports(5)
            
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
                            loaded_report = db.load_report(report['id'])
                            if loaded_report:
                                st.session_state.report_mode = loaded_report["report_type"]
                                st.session_state.report_data = loaded_report["data"]
                                st.session_state.current_section = loaded_report["current_section"]
                                st.session_state.current_report_id = report['id']
                                st.session_state.generated_report = None
                                st.rerun()
            else:
                st.caption("No saved reports yet")