"""
@author: Youwei Zheng
@target: Chat completion
@update: 2024.10.31
"""

from utils import create_tongyi_client
from utils import create_openai_client


def chat_tongyi_naive(hm: str) -> str:
    """Chat completion using Tongyi API

    Args:
        hm (str): Human Message

    Returns:
        str: AI response message
    """
    chatllm_client = create_tongyi_client()
    # Assuming create_tongyi_client().invoke is async
    message = chatllm_client.invoke(hm)
    return message.content
    

def chat_openai(hm: str) -> str:
    """Chat completion using OpenAI API
    Args:
        hm (str): Human Message

    Returns:
        str: AI response message
    """

    # hm = "Do you know Luis Figo?"
    chatllm_client = create_openai_client()    
    message = chatllm_client.invoke(hm)

    return message.content
    