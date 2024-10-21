"""
@author: Youwei Zheng
@target: Chat completion
@update: 2024.10.21
"""

from utils import create_tongyi_client
from utils import create_openai_client


def chat_tongyi_naive(hm: str) -> str:
    """_summary_

    Args:
        hm (str): Human Message

    Returns:
        _type_: _description_
    """

    # hm = "Do you know Luis Figo?"
    chatllm_client = create_tongyi_client()
    
    message = chatllm_client.invoke(hm)

    return message.content
    

def chat_openai(hm: str) -> str:
    """_summary_

    Args:
        hm (str): Human Message

    Returns:
        _type_: _description_
    """

    # hm = "Do you know Luis Figo?"
    chatllm_client = create_openai_client()    
    message = chatllm_client.invoke(hm)

    return message.content
    