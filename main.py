import streamlit as st
from chains.factual_chain import create_factual_chain
from chains.engagement_chain import create_engagement_chain
from chains.response_combiner import combine_responses

# Set page config first
st.set_page_config(page_title="Special Education Zen AI", page_icon="🧘")

# Set OpenAI API Key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Initialize chains in session state
if "factual_chain" not in st.session_state:
    st.session_state.factual_chain = create_factual_chain(openai_api_key)

if "engagement_chain" not in st.session_state:
    st.session_state.engagement_chain = create_engagement_chain(openai_api_key)

# Initialize message history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.title("Educational Psychology Zen AI")
st.write("Your supportive colleague for educational psychology guidance and professional development.")

# Sidebar with resources
with st.sidebar:
    st.header("Helpful Resources")
    st.markdown("[British Psychological Society](https://www.bps.org.uk/)")
    st.markdown("[Association of Educational Psychologists](https://www.aep.org.uk/)")
    st.markdown("[SEND Code of Practice](https://www.gov.uk/government/publications/send-code-of-practice-0-to-25)")
    
    st.markdown("---")
    
    # Feature toggles for development
    st.header("Response Style")
    use_dual_temp = st.checkbox("Enhanced Engagement", value=True, 
                               help="Combines factual accuracy with empathetic engagement")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if user_input := st.chat_input("Ask about EP practice, cases, or professional development..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Contemplating your question..."):
            if use_dual_temp:
                # Get factual response
                factual_response = st.session_state.factual_chain.run(human_input=user_input)
                
                # Combine into single input for engagement chain
                combined_input = f"Original EP question: {user_input}\n\nFactual advice to enhance: {factual_response}"
                
                # Get enhanced response using simple single-input approach
                final_response = st.session_state.engagement_chain.run(input=combined_input)
            else:
                # Use just the factual chain
                final_response = st.session_state.factual_chain.run(human_input=user_input)
            
            st.write(final_response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_response})

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    # Reset both chains to clear their memory
    st.session_state.factual_chain = create_factual_chain(openai_api_key)
    st.session_state.engagement_chain = create_engagement_chain(openai_api_key)