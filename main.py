import streamlit as st
from chains.simple_ep_chain import create_ep_chain

# Set page config first
st.set_page_config(page_title="Special Education Zen AI", page_icon="🧘")

# Set OpenAI API Key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Initialize chain in session state
if "ep_chain" not in st.session_state:
    st.session_state.ep_chain = create_ep_chain(openai_api_key)

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
    
    # Simple settings
    st.header("Settings")
    st.write("Using balanced single-chain approach for optimal EP support.")

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
        with st.spinner("Thinking through this with you..."):
            final_response = st.session_state.ep_chain.run(human_input=user_input)
            st.write(final_response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_response})

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    # Reset the chain to clear memory
    st.session_state.ep_chain = create_ep_chain(openai_api_key)