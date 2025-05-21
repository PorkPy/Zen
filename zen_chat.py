import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set OpenAI API Key from Streamlit Secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize Memory (Ensures session persistence)
memory = ConversationBufferMemory(memory_key="chat_history")

# Define Prompt Template (Includes chat history)
text_prompt = PromptTemplate.from_template("""
Here is the conversation so far:
{chat_history}

Now respond to: {question}
""")

# Create LLM Chain (Links Memory)
llm = OpenAI(temperature=0)
qa_chain = LLMChain(prompt=text_prompt, llm=llm, memory=memory)

# Streamlit UI
def main():
    st.title("Zen AI")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = ""

    user_input = st.text_input("Ask me anything!", "")

    if user_input:
        response = qa_chain.run({"question": user_input, "chat_history": st.session_state["chat_history"]})
        
        # Update chat history
        st.session_state["chat_history"] += f"User: {user_input}\nAI: {response}\n"
        
        st.write(response)

if __name__ == "__main__":
    main()