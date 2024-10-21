'''
@author: Youwei Zheng
@target: chatllm client builder
@update: 2024.10.21
'''

import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------
# DashScope ChatModel
# ------------------------------

def create_tongyi_client():
    from langchain_community.chat_models.tongyi import ChatTongyi

    client = ChatTongyi(
        model=os.getenv('DASHSCOPE_CHAT_MODEL'),
        api_key=os.getenv('DASHSCOPE_API_KEY')
    )

    return client


def create_openai_client(temperature=0.9, stream=False):
    '''
    OpenAI Models via langchain_openai
    '''

    from langchain_openai import ChatOpenAI

    client_chat = ChatOpenAI(
        model=os.getenv('OPENAI_MODEL'),
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=temperature,
        streaming=stream
        )
    # client_chat.invoke("Do you know Alibaba?")
    
    return client_chat
    