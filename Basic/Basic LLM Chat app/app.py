import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")    
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")


import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFacePipeline

prompt = ChatPromptTemplate.from_messages(

    [
        ("system", "You are a helpful assistant.Please respond to the user query in a concise manner."),
        ("user","Question: {question}")
    ]
)
st.title("Local LLM Chat App")
input_text = st.text_input("Enter your question here:")
llm= HuggingFacePipeline.from_model_id(
    model_id="google/codegemma-2b",
    task="text-generation"
)


output = StrOutputParser()
chain = prompt|llm|output
if input_text:
    st.write(chain.invoke({"question": input_text}))