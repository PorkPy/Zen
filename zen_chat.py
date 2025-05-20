import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

# Set OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]
st.write(f"Using API key: {api_key}")

# Define prompt template
text_prompt = PromptTemplate.from_template("""
Answer this question in the style of a monk who never gives a straight answer and only replys using minimalistic spiritual metaphor:
{question}
""")

# Create LLM chain
llm = OpenAI(temperature=0)
qa_chain = LLMChain(prompt=text_prompt, llm=llm)

# Router function
def route_input(user_input):
    if any(x in user_input.lower() for x in ["draw", "image", "picture"]):
        return "image"
    elif any(x in user_input.lower() for x in ["code", "python", "script"]):
        return "code"
    else:
        return "text"

# Define behavior for each type
def handle_text(user_input):
    return qa_chain.run({"question": user_input})

def handle_image(user_input):
    return "Imagine a beautiful picture based on -> '" + user_input + "'"

def handle_code(user_input):
    return "Python code that handles -> '" + user_input + "'"

# Streamlit UI
st.title("Zen")
user_input = st.text_input("Ask me anything!", "")

if user_input:
    route = route_input(user_input)
    if route == "text":
        response = handle_text(user_input)
    elif route == "image":
        response = handle_image(user_input)
    elif route == "code":
        response = handle_code(user_input)
    else:
        response = "I don't understand that request."

    st.write(response)

if __name__ == "__main__":
    main()
