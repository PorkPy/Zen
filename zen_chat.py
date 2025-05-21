import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
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

# Define Prompt Template
template = """
You are Zen AI, a specialized assistant for special educational needs professionals.
You provide calm, wise, and evidence-based guidance related to special education.
Always assume questions are related to special educational needs contexts and come from an educational psychologist.
Consider inclusive education practices, differentiation techniques, and supportive interventions.
Do not tell the user how important special education is; they already know.

Conversation history:
{chat_history}

Human question: {human_input}

Please provide a thoughtful response that considers special education best practices:
"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

# Create LLM Chain
llm = OpenAI(temperature=0.4, openai_api_key=openai_api_key)
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=st.session_state.memory
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
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Contemplating..."):
            response = chain.run(human_input=user_input)
            st.write(response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)