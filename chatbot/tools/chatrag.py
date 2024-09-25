'''
@author: Youwei Zheng
@target: Adapted from intro-to-vector-dbs
@update: 2024.09.25
'''

import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# ------------------------------
# Import Modules
# ------------------------------

from langchain_core.prompts import PromptTemplate

# ------------------------------
# Import Retrieval modules
# ------------------------------

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# ------------------------------
# Import llmbuilder
# ------------------------------

import tools.llmbuilder as llmbuilder
import tools.embedder as embedder

from langchain_community.vectorstores import FAISS

def integrate_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ------------------------------
# Evaluation function
# ------------------------------

def chat_suaee(query: str):
    # Create necessary clients
    print("Creating necessary clients...")
    chatllm_client = llmbuilder.create_tongyi_client()
    embedder_client = embedder.create_dashscope_client()
    
    # Retrieve from vectorstore    
    print("Retrieving from vectorstore...")
    faiss_folder_path = "./faiss_suaee"
    vectorstore = FAISS.load_local(
        folder_path=faiss_folder_path,
        index_name="index",
        embeddings=embedder_client,
        allow_dangerous_deserialization=True
    )

    template = """
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say you don't know and don't try to make up an answer.
        Use three sentences maximum and keep the answer as precise as possible.
        
        {context}
        Question: {question}        
    """

    retrieval_qa_chat_prompt = PromptTemplate.from_template(template=template)

    from langchain_core.runnables import RunnablePassthrough
    
    retrieval_chain = (
        {
            "context": vectorstore.as_retriever() | integrate_docs, 
            "question": RunnablePassthrough()
        } 
        | retrieval_qa_chat_prompt
        | chatllm_client
    )

    # Invoke the retrieval chain with the provided query
    result = retrieval_chain.invoke(query)
    return result.content

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    # Example user query
    query = "你好呀"   
    answer = evaluate(query)
    print("Result from evaluation:")
    print(answer)
