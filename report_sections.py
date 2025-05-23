import streamlit as st
from report_generator import generate_professional_report

def save_and_navigate(section_data, direction, db, anthropic_api_key=None):
    """Helper function to save current section data and navigate"""
    # Update session state with current data
    st.session_state.report_data.update(section_data)
    
    # Generate or use existing report ID
    if not st.session_state.current_report_id:
        st.session_state.current_report_id = db.generate_report_id(
            st.session_state.report_data.get("child_name", "Unknown"), "ehc_assessment"
        )
    
    if direction == "next":
        st.session_state.current_section += 1
    elif direction == "previous":
        st.session_state.current_section -= 1
    elif direction == "save_exit":
        db.save_report(
            st.session_state.current_report_id,
            "ehc_assessment",
            st.session_state.report_data.get("child_name", "Unknown"),
            st.session_state.report_data,
            st.session_state.current_section
        )
        st.session_state.report_mode = None
        st.success(f"Report saved! ID: {st.session_state.current_report_id}")
    elif direction == "generate_report":
        # Mark as completed and save
        db.save_report(
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

def render_navigation_buttons(section_data, current_section, total_sections, db, anthropic_api_key=None):
    """Render navigation buttons for report sections"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_section > 0:
            if st.button("← Previous Section"):
                save_and_navigate(section_data, "previous", db)
        else:
            st.button("← Previous Section", disabled=True)
    
    with col2:
        if current_section < total_sections - 1:
            if st.button("Next Section →"):
                save_and_navigate(section_data, "next", db)
        else:
            if st.button("🎯 Generate Professional Report"):
                save_and_navigate(section_data, "generate_report", db, anthropic_api_key)
    
    with col3:
        if st.button("💾 Save & Exit"):
            save_and_navigate(section_data, "save_exit", db)

def render_report_section(section_name, current_section, total_sections, report_data, db, anthropic_api_key):
    """Render the appropriate section based on section name"""
    
    if section_name == "Child Information & Referral":
        st.write("Let's start with basic information about the child and referral:")
        st.caption("💭 *Write however feels natural - notes, bullet points, full sentences. I'll format it properly later.*")
        
        name = st.text_input("Child's name (or initials):", 
                            value=report_data.get("child_name", ""), 
                            key="child_name")
        age = st.text_input("Age and date of birth:", 
                           value=report_data.get("child_age", ""), 
                           key="child_age")
        school = st.text_input("School/setting:", 
                              value=report_data.get("child_school", ""), 
                              key="child_school")
        referral_reason = st.text_area("Reason for referral:", 
                                      value=report_data.get("referral_reason", ""),
                                      key="referral_reason", 
                                      help="Just jot down the key concerns - bullet points are fine!")
        
        section_data = {
            "child_name": name,
            "child_age": age,
            "child_school": school,
            "referral_reason": referral_reason
        }
        
    elif section_name == "Background & History":
        st.write("Tell me about the child's background and developmental history:")
        st.caption("💭 *Don't worry about perfect sentences - capture what you know however works for you.*")
        
        family_background = st.text_area("Family background and home circumstances:", 
                                        value=report_data.get("family_background", ""),
                                        key="family_background",
                                        help="Quick notes are fine - family structure, any relevant circumstances")
        developmental_history = st.text_area("Early developmental history (milestones, concerns):", 
                                           value=report_data.get("developmental_history", ""),
                                           key="developmental_history",
                                           help="Any developmental info you have - bullet points work great")
        medical_history = st.text_area("Relevant medical history:", 
                                     value=report_data.get("medical_history", ""),
                                     key="medical_history",
                                     help="Just note any relevant medical information")
        previous_support = st.text_area("Previous educational support and interventions:", 
                                      value=report_data.get("previous_support", ""),
                                      key="previous_support",
                                      help="List what's been tried before - informal notes are perfect")
        
        section_data = {
            "family_background": family_background,
            "developmental_history": developmental_history,
            "medical_history": medical_history,
            "previous_support": previous_support
        }
        
    elif section_name == "Assessment Methods & Observations":
        st.write("Details about your assessment approach and observations:")
        st.caption("💭 *Just capture your observations naturally - I'll turn them into professional report language.*")
        
        assessment_methods = st.text_area("Assessment methods used (tests, observations, interviews):", 
                                        value=report_data.get("assessment_methods", ""),
                                        key="assessment_methods",
                                        help="List what you did - WISC-V, observations, etc.")
        classroom_observation = st.text_area("Classroom observation findings:", 
                                           value=report_data.get("classroom_observation", ""),
                                           key="classroom_observation",
                                           help="What did you notice? Jot down key observations")
        child_interaction = st.text_area("Direct interaction with child - behavior and engagement:", 
                                       value=report_data.get("child_interaction", ""),
                                       key="child_interaction",
                                       help="How was the child during assessment? Informal notes fine")
        child_views = st.text_area("Child's views and perspectives:", 
                                 value=report_data.get("child_views", ""),
                                 key="child_views",
                                 help="What did the child say? Direct quotes or paraphrasing both work")
        
        section_data = {
            "assessment_methods": assessment_methods,
            "classroom_observation": classroom_observation,
            "child_interaction": child_interaction,
            "child_views": child_views
        }
        
    elif section_name == "Cognitive Assessment":
        st.write("Cognitive assessment results and findings:")
        st.caption("💭 *Record test results, observations during testing, and what they mean. Don't worry about formatting.*")
        
        cognitive_tests = st.text_area("Cognitive tests administered:", 
                                     value=report_data.get("cognitive_tests", ""),
                                     key="cognitive_tests",
                                     help="WISC-V, BPVS, etc. - just list what you used")
        
        cognitive_scores = st.text_area("Test scores and index scores:", 
                                      value=report_data.get("cognitive_scores", ""),
                                      key="cognitive_scores",
                                      help="Raw scores, standard scores, percentiles - whatever format works",
                                      height=100)
        
        cognitive_strengths = st.text_area("Cognitive strengths observed:", 
                                         value=report_data.get("cognitive_strengths", ""),
                                         key="cognitive_strengths",
                                         help="What did the child do well? Areas of strength?")
        
        cognitive_difficulties = st.text_area("Areas of cognitive difficulty:", 
                                            value=report_data.get("cognitive_difficulties", ""),
                                            key="cognitive_difficulties",
                                            help="Where did they struggle? What patterns emerged?")
        
        testing_behavior = st.text_area("Behavior and approach during testing:", 
                                      value=report_data.get("testing_behavior", ""),
                                      key="testing_behavior",
                                      help="How did they engage? Any factors affecting performance?")
        
        section_data = {
            "cognitive_tests": cognitive_tests,
            "cognitive_scores": cognitive_scores,
            "cognitive_strengths": cognitive_strengths,
            "cognitive_difficulties": cognitive_difficulties,
            "testing_behavior": testing_behavior
        }
        
    elif section_name == "Educational Attainment":
        st.write("Educational attainment and academic performance:")
        st.caption("💭 *Note current academic levels, progress,