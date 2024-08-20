'''
@author: Youwei Zheng
@target: method to create different llm clients.
@update: 2024.07.31
'''

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

# ------------------------------
# Model Builders
# ------------------------------

def create_dashscope_client(temperature=0.9, stream=False):
    '''
    Aliyun Open Source Models
    Token Limit: 1M ?
    '''
    
    client = ChatOpenAI(
        model=os.getenv('Aliyun_DashScope_MODEL'),
        base_url=os.getenv('Aliyun_DashScope_BASE_URL'),
        api_key=os.getenv('Aliyun_DashScope_API_KEY'),
        temperature=temperature,
        streaming=stream
    )
    
    return client

def create_openai_client(temperature=0.9, stream=False):
    '''
    OpenAI Models    
    '''
    
    client = ChatOpenAI(
        model=os.getenv('OPENAI_MODEL'),
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=temperature,
        streaming=stream
    )
    
    return client
