import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set page config first (must be the first Streamlit command)
st.set_page_config(page_title="Zen AI", page_icon="🧘")

# Set OpenAI API Key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Initialize Memory in session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize message history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define Prompt Template for precise special education guidance
edu_prompt = PromptTemplate.from_template("""
You are Zen AI, a specialized assistant for special educational needs professionals.
Provide calm, wise, and evidence-based guidance related to special education.
Assume all questions come from an educational psychologist.

Consider inclusive education practices, differentiation techniques, and supportive interventions.
Do not tell the user how important special education is; they already know.

Human question: {human_input}

Provide a clear, evidence-based response:
""")

# Define Prompt Template for warm conversational follow-up
chat_prompt = PromptTemplate.from_template("""
Based on the educational response, provide a supportive and engaging follow-up.
Maintain a warm, conversational tone.

Educational Response: {edu_response}

Now add a friendly follow-up message:
""")

# Create two LLM models with different temperature settings
edu_llm = OpenAI(temperature=0.4, openai_api_key=openai_api_key)
chat_llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Create two chains
edu_chain = LLMChain(llm=edu_llm, prompt=edu_prompt, output_key="edu_response")
chat_chain = LLMChain(llm=chat_llm, prompt=chat_prompt, output_key="chat_response")

# Combine into a sequential chain
full_chain = SequentialChain(
    chains=[edu_chain, chat_chain],
    input_variables=["human_input"],
    output_variables=["edu_response", "chat_response"]
)

# Streamlit UI
st.title("Zen")
st.write("Welcome to Zen—Your Special Education Companion.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if user_input := st.chat_input("Ask Zen..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response (education + conversational follow-up)
    with st.chat_message("assistant"):
        with st.spinner("Contemplating..."):
            response = full_chain.run({"human_input": user_input})
            st.write(response["edu_response"])  # Educational guidance
            st.write(response["chat_response"])  # Conversational follow-up

    # Add AI responses to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["edu_response"]})
    st.session_state.messages.append({"role": "assistant", "content": response["chat_response"]})

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)