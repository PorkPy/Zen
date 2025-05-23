import streamlit as st
from chains.claude_ep_chain import create_claude_ep_chain

# Set page config first
st.set_page_config(page_title="Jess - For Educational Psychologists", page_icon="🅹")

# Set Anthropic API Key from Streamlit Secrets
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

# Initialize chain in session state
if "ep_chain" not in st.session_state:
    st.session_state.ep_chain = create_claude_ep_chain(anthropic_api_key)

# Initialize message history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.title("Jess")
st.caption("For Educational Psychologists")
st.write("")  # Add some spacing

# Sidebar with resources and info
with st.sidebar:
    st.header("📚 Professional Bodies")
    st.markdown("[BPS Division of Educational Psychology](https://www.bps.org.uk/divisions/educational-psychology)")
    st.markdown("[Association of Educational Psychologists](https://www.aep.org.uk/)")
    
    st.header("📋 Key Resources")
    st.markdown("[SEND Code of Practice](https://www.gov.uk/government/publications/send-code-of-practice-0-to-25)")
    st.markdown("[NICE Guidelines](https://www.nice.org.uk/)")
    st.markdown("[Mental Capacity Act](https://www.legislation.gov.uk/ukpga/2005/9/contents)")
    
    st.markdown("---")
    
    st.header("ℹ️ About Jess")
    st.write("Jess is your supportive AI colleague for EP practice. Ask questions about cases, interventions, assessments, or professional development.")
    
    st.write("**How to use:**")
    st.write("• Ask questions naturally, as you would a colleague")
    st.write("• Reference previous topics in follow-up questions") 
    st.write("• Request specific frameworks, tools, or strategies")
    
    st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if user_input := st.chat_input("Ask Jess about EP practice, cases, or professional development..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Jess is thinking through this with you..."):
            final_response = st.session_state.ep_chain.run(human_input=user_input)
            st.write(final_response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_response})

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    # Reset the chain to clear memory
    st.session_state.ep_chain = create_claude_ep_chain(anthropic_api_key)