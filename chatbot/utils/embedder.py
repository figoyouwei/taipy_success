'''
@author: Youwei Zheng
@target: run embedding and save to vectorstore
@discov: Pinecone not supporting dashscope model='text-embedding-v1'
@update: 2024.08.29
'''

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.vectorstores import FAISS

# ------------------------------
# DashScope Embedding Models
# ------------------------------

def create_dashscope_client(temperature=0.9, stream=False):
    '''
    参考资料
    https://help.aliyun.com/zh/model-studio/developer-reference/text-embedding-quick-start-1
    '''

    from langchain_community.embeddings import DashScopeEmbeddings

    client = DashScopeEmbeddings(
        model=os.getenv('DASHSCOPE_EMBD_MODEL'),
        dashscope_api_key=os.getenv('DASHSCOPE_API_KEY'),      
    )
    return client
