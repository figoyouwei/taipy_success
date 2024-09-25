'''
@author: Youwei Zheng
@target: chatllm client builder
@update: 2024.08.28
'''

import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------
# OpenAI Embedding Models
# ------------------------------

def create_tongyi_client():
    from langchain_community.chat_models.tongyi import ChatTongyi

    client = ChatTongyi(
        model=os.getenv('DASHSCOPE_CHAT_MODEL'),
        api_key=os.getenv('DASHSCOPE_API_KEY')
    )

    return client


def create_dashscope_client(temperature=0.9, stream=False):
    '''
    兼容ChatOpenAI, 但只兼容了openai的接口
    https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope
    '''

    from langchain_openai import ChatOpenAI
    
    client = ChatOpenAI(
        model=os.getenv('DASHSCOPE_CHAT_MODEL'),
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        base_url=os.getenv('DASHSCOPE_BASE_URL'),
        # temperature=temperature,
        # streaming=stream
        )

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }, 
        {
            "role": "user",
            "content": "Do you know Alibaba?"
        }
        ]

    client.invoke(messages)
    
    return client

# ------------------------------
# OpenAI chatmodel
# ------------------------------

def create_openai_client(temperature=0.9, stream=False):
    '''
    OpenAI Models via langchain_openai
    Previous chat_models method will be removed in 0.3.0
    '''

    # llm对象
    # from langchain_openai import OpenAI
    # client_llm = OpenAI(
    #     name="text-ada-001",
    #     api_key=os.getenv('OPENAI_API_KEY'),
    #     )    
    # client_llm.invoke("Do you know Alibaba?")        
    
    from langchain_openai import ChatOpenAI

    client_chat = ChatOpenAI(
        model=os.getenv('OPENAI_MODEL'),
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=temperature,
        streaming=stream
        )
    # client_chat.invoke("Do you know Alibaba?")
    
    return client_chat

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    
    chatllm_client = create_tongyi_client()
    type(chatllm_client)
    
    messages = [
        ("system", "你是一名专业的翻译家，可以将用户的中文翻译为英文"),
        ("human", "我喜欢菲戈的踢球方式"),
    ]
    
    chatllm_client.invoke(messages)