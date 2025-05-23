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
                            key=f"child_name_edit_{current_section}")
        age = st.text_input("Age and date of birth:", 
                           value=report_data.get("child_age", ""), 
                           key=f"child_age_edit_{current_section}")
        school = st.text_input("School/setting:", 
                              value=report_data.get("child_school", ""), 
                              key=f"child_school_edit_{current_section}")
        referral_reason = st.text_area("Reason for referral:", 
                                      value=report_data.get("referral_reason", ""),
                                      key=f"referral_reason_edit_{current_section}", 
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
                                        key=f"family_background_edit_{current_section}",
                                        help="Quick notes are fine - family structure, any relevant circumstances")
        developmental_history = st.text_area("Early developmental history (milestones, concerns):", 
                                           value=report_data.get("developmental_history", ""),
                                           key=f"developmental_history_edit_{current_section}",
                                           help="Any developmental info you have - bullet points work great")
        medical_history = st.text_area("Relevant medical history:", 
                                     value=report_data.get("medical_history", ""),
                                     key=f"medical_history_edit_{current_section}",
                                     help="Just note any relevant medical information")
        previous_support = st.text_area("Previous educational support and interventions:", 
                                      value=report_data.get("previous_support", ""),
                                      key=f"previous_support_edit_{current_section}",
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
                                        key=f"assessment_methods_edit_{current_section}",
                                        help="List what you did - WISC-V, observations, etc.")
        classroom_observation = st.text_area("Classroom observation findings:", 
                                           value=report_data.get("classroom_observation", ""),
                                           key=f"classroom_observation_edit_{current_section}",
                                           help="What did you notice? Jot down key observations")
        child_interaction = st.text_area("Direct interaction with child - behavior and engagement:", 
                                       value=report_data.get("child_interaction", ""),
                                       key=f"child_interaction_edit_{current_section}",
                                       help="How was the child during assessment? Informal notes fine")
        child_views = st.text_area("Child's views and perspectives:", 
                                 value=report_data.get("child_views", ""),
                                 key=f"child_views_edit_{current_section}",
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
                                     key=f"cognitive_tests_edit_{current_section}",
                                     help="WISC-V, BPVS, etc. - just list what you used")
        
        cognitive_scores = st.text_area("Test scores and index scores:", 
                                      value=report_data.get("cognitive_scores", ""),
                                      key=f"cognitive_scores_edit_{current_section}",
                                      help="Raw scores, standard scores, percentiles - whatever format works",
                                      height=100)
        
        cognitive_strengths = st.text_area("Cognitive strengths observed:", 
                                         value=report_data.get("cognitive_strengths", ""),
                                         key=f"cognitive_strengths_edit_{current_section}",
                                         help="What did the child do well? Areas of strength?")
        
        cognitive_difficulties = st.text_area("Areas of cognitive difficulty:", 
                                            value=report_data.get("cognitive_difficulties", ""),
                                            key=f"cognitive_difficulties_edit_{current_section}",
                                            help="Where did they struggle? What patterns emerged?")
        
        testing_behavior = st.text_area("Behavior and approach during testing:", 
                                      value=report_data.get("testing_behavior", ""),
                                      key=f"testing_behavior_edit_{current_section}",
                                      help="How did they engage? Any factors affecting performance?")
        
        section_data = {
            "cognitive_tests": cognitive_tests,
            "cognitive_scores": cognitive_scores,
            "cognitive_strengths": cognitive_strengths,
            "cognitive_difficulties": cognitive_difficulties,
            "testing_behavior": testing_behavior
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
        st.caption("💭 *Note current academic levels, progress, and curriculum access naturally.*")
        
        academic_levels = st.text_area("Current academic levels and attainment:", 
                                     value=report_data.get("academic_levels", ""),
                                     key=f"academic_levels_edit_{current_section}",
                                     help="Reading age, maths levels, National Curriculum levels, etc.")
        
        curriculum_access = st.text_area("Access to curriculum and learning:", 
                                        value=report_data.get("curriculum_access", ""),
                                        key=f"curriculum_access_edit_{current_section}",
                                        help="How well can they access mainstream curriculum?")
        
        academic_strengths = st.text_area("Academic strengths and interests:", 
                                        value=report_data.get("academic_strengths", ""),
                                        key=f"academic_strengths_edit_{current_section}",
                                        help="What subjects/areas does the child excel in?")
        
        learning_barriers = st.text_area("Barriers to learning and progress:", 
                                        value=report_data.get("learning_barriers", ""),
                                        key=f"learning_barriers_edit_{current_section}",
                                        help="What's preventing optimal academic progress?")
        
        section_data = {
            "academic_levels": academic_levels,
            "curriculum_access": curriculum_access,
            "academic_strengths": academic_strengths,
            "learning_barriers": learning_barriers
        }
        
    elif section_name == "Social, Emotional & Behavioral Factors":
        st.write("Social, emotional and behavioral observations:")
        st.caption("💭 *Describe the child's social interactions, emotional regulation, and behavior patterns.*")
        
        social_skills = st.text_area("Social skills and peer relationships:", 
                                   value=report_data.get("social_skills", ""),
                                   key=f"social_skills_edit_{current_section}",
                                   help="How does the child interact with peers and adults?")
        
        emotional_regulation = st.text_area("Emotional development and regulation:", 
                                          value=report_data.get("emotional_regulation", ""),
                                          key=f"emotional_regulation_edit_{current_section}",
                                          help="How does the child manage emotions and stress?")
        
        behavioral_patterns = st.text_area("Behavioral observations and patterns:", 
                                         value=report_data.get("behavioral_patterns", ""),
                                         key=f"behavioral_patterns_edit_{current_section}",
                                         help="Any concerning or notable behavioral patterns?")
        
        self_esteem = st.text_area("Self-esteem and confidence:", 
                                 value=report_data.get("self_esteem", ""),
                                 key=f"self_esteem_edit_{current_section}",
                                 help="How does the child view themselves and their abilities?")
        
        section_data = {
            "social_skills": social_skills,
            "emotional_regulation": emotional_regulation,
            "behavioral_patterns": behavioral_patterns,
            "self_esteem": self_esteem
        }
        
    elif section_name == "Psychological Formulation":
        st.write("Your psychological formulation and professional analysis:")
        st.caption("💭 *This is your expert interpretation - write your professional thoughts naturally.*")
        
        formulation = st.text_area("Psychological formulation:", 
                                 value=report_data.get("formulation", ""),
                                 key=f"formulation_edit_{current_section}",
                                 help="Your professional analysis of what's happening for this child",
                                 height=150)
        
        contributing_factors = st.text_area("Contributing factors and underlying causes:", 
                                          value=report_data.get("contributing_factors", ""),
                                          key=f"contributing_factors_edit_{current_section}",
                                          help="What factors are contributing to the child's difficulties?")
        
        prognosis = st.text_area("Prognosis and future considerations:", 
                                value=report_data.get("prognosis", ""),
                                key=f"prognosis_edit_{current_section}",
                                help="What's the outlook? What should be considered going forward?")
        
        section_data = {
            "formulation": formulation,
            "contributing_factors": contributing_factors,
            "prognosis": prognosis
        }
        
    elif section_name == "Recommendations & Provision":
        st.write("Recommendations and provision needed:")
        st.caption("💭 *Specify what support the child needs - be as detailed or brief as works for you.*")
        
        educational_provision = st.text_area("Educational provision recommendations:", 
                                            value=report_data.get("educational_provision", ""),
                                            key=f"educational_provision_edit_{current_section}",
                                            help="What educational support/placement is needed?",
                                            height=120)
        
        interventions = st.text_area("Specific interventions and strategies:", 
                                   value=report_data.get("interventions", ""),
                                   key=f"interventions_edit_{current_section}",
                                   help="What specific interventions should be implemented?",
                                   height=120)
        
        professional_support = st.text_area("Professional support required:", 
                                           value=report_data.get("professional_support", ""),
                                           key=f"professional_support_edit_{current_section}",
                                           help="What other professionals need to be involved?")
        
        monitoring = st.text_area("Review and monitoring arrangements:", 
                                value=report_data.get("monitoring", ""),
                                key=f"monitoring_edit_{current_section}",
                                help="How should progress be monitored and reviewed?")
        
        section_data = {
            "educational_provision": educational_provision,
            "interventions": interventions,
            "professional_support": professional_support,
            "monitoring": monitoring
        }
    
    else:
        st.error(f"Unknown section: {section_name}")
        return
    
    # Render navigation buttons
    render_navigation_buttons(section_data, current_section, total_sections, db, anthropic_api_key)