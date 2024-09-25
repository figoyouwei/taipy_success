'''
@author: Youwei Zheng
@target: Create embedder client
@update: 2024.09.25
'''

import os
from dotenv import load_dotenv

load_dotenv()

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
