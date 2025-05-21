import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Set OpenAI API Key from Streamlit Secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize Memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history")

# Define Prompt Template with conversation memory
text_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Here is the conversation so far:
{chat_history}

Now respond to: {question}
""")

# Create LLM Chain with Memory
llm = OpenAI(temperature=0)
qa_chain = LLMChain(prompt=text_prompt, llm=llm, memory=memory)

# Define the main function
def main():
    st.title("Zen AI")
    user_input = st.text_input("Ask me anything!", "")

    if user_input:
        response = qa_chain.run({"question": user_input})
        st.write(response)

if __name__ == "__main__":
    main()