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
st.title("Special Education Zen AI")
st.write("Your specialized assistant for special educational needs guidance and wisdom.")

# Sidebar with resources
with st.sidebar:
    st.header("Helpful Resources")
    st.markdown("[National Center for Learning Disabilities](https://www.ncld.org/)")
    st.markdown("[Council for Exceptional Children](https://exceptionalchildren.org/)")
    st.markdown("[IDEA Resources](https://sites.ed.gov/idea/)")
    
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
if user_input := st.chat_input("Ask about special educational needs..."):
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
                
                # Get engagement response - pass all required inputs as a dict
                engagement_inputs = {
                    "human_input": user_input,
                    "factual_content": factual_response
                }
                engagement_response = st.session_state.engagement_chain.invoke(engagement_inputs)
                
                # Extract the response text
                if isinstance(engagement_response, dict):
                    engagement_text = engagement_response.get("text", str(engagement_response))
                else:
                    engagement_text = str(engagement_response)
                
                # Combine responses
                final_response = combine_responses(factual_response, engagement_text)
            else:
                # Use just the factual chain
                final_response = st.session_state.factual_chain.run(human_input=user_input)
            
            st.write(final_response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_response})

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    # Reset the chains to clear their memory
    st.session_state.factual_chain = create_factual_chain(openai_api_key)
    st.session_state.engagement_chain = create_engagement_chain(openai_api_key)