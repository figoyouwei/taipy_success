'''
@author: Youwei Zheng
@target: Chatbot page
@update: 2024.08.09
'''

import taipy.gui.builder as tgb

def create_page():
        
    with tgb.Page() as page:
        # title line
        tgb.toggle(theme=True)
        tgb.text("# Chatbot with LangChain", mode="md", class_name="text-center pb1")

        # footer
        tgb.text("Developed by CR7", mode="md", class_name="text-center pb1")               
    
    return page
