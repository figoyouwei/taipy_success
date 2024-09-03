'''
@author: Youwei Zheng
@target: chatllm client builder
@update: 2024.08.28
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
