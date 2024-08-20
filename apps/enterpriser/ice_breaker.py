'''
@author: Youwei Zheng
@target: Connect llm with ReAct agent, searching for weibo profile url.
@things: Output Parsers with Pydantic
@update: 2024.08.13
'''

from typing import Tuple, Dict
from langchain_core.prompts import PromptTemplate
import utils.llmbuilder as llmbuilder
from apps.enterpriser.third_parties.tyc import tyc_baseinfo_normal
from apps.enterpriser.output_parsers import parser_summary, Summary

# ------------------------------
# Return response as pydantic object
# ------------------------------

def ice_breaker_with(name: str) -> Tuple[Summary, Dict]:
    # Create llm client
    llm_client = llmbuilder.create_dashscope_client()

    # Create prompt template
    # summary_template = """
    #     你收到一家企业的基本信息数据 {baseinfo_normal}. 
    #     1.撰写一份关于这家企业的基本信息汇总稿件，一段文字不要罗列
    #     2.罗列这家企业2-3项有趣信息

    #     \n{format_instructions}
    #     """

    summary_template = """
        Given the information about a company {baseinfo_normal},
        I want you to create:
        1. A short summary as Summary
        2. two interesting facts about it as Facts
        
        \nPlease output no bold text and linebreake such as \n.
        And generate valid json.

        \n{format_instructions}
        """
        
    prompt_template = PromptTemplate(
        input_variables=["baseinfo_normal"],
        template=summary_template,
        partial_variables={
            "format_instructions": parser_summary.get_format_instructions()
        }
    )

    # Create feed data
    tyc_data = tyc_baseinfo_normal(
        company_name=name
    )
    type(tyc_data)

    # Create chains
    print("Created chains")
    chains = prompt_template | llm_client | parser_summary

    # Call the chains.invoke method
    res:Summary = chains.invoke(
        input={"baseinfo_normal": tyc_data},
    )

    print("Generated results")
    print(res)   
    return res, tyc_data

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Guten Tag, Ice Breaker")
    name = "北京产权交易所有限公司"
    res, data = ice_breaker_with(name)

    print(res)
    print(data)
    res.__dict__