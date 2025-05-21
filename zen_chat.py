import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set OpenAI API Key from Streamlit Secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize Memory (Session-Based Storage)
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
        st.session_state["chat_history"] = []

    # Show conversation history above input
    for entry in st.session_state["chat_history"]:
        st.write(entry)

    # User input field with session state retrieval
    user_input = st.text_input("Ask Zen", value=st.session_state.get("user_input", ""), key="user_input")

    # Submit button to trigger response processing
    if st.button("Submit"):
        if user_input:
            response = qa_chain.run({"question": user_input, "chat_history": "\n".join(st.session_state["chat_history"])})

            # Append conversation to history
            st.session_state["chat_history"].append(f"**You:** {user_input}")
            st.session_state["chat_history"].append(f"**Zen AI:** {response}")

            # Clear input field safely by updating session state
            st.session_state["user_input"] = ""

            # Display the updated history without forcing a page refresh

if __name__ == "__main__":
    main()