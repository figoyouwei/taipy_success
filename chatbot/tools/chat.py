"""
@author: Youwei Zheng
@target: Chat with openai
@update: 2024.09.03
"""

from utils import create_tongyi_client

def chat_tongyi(hm: str) -> str:
    """_summary_

    Args:
        hm (str): Human Message

    Returns:
        _type_: _description_
    """

    # hm = "Do you know Luis Figo?"
    chatllm_client = create_tongyi_client()
    
    # TODO: just change to chain.invoke()
    message = chatllm_client.invoke(hm)

    return message.content
    