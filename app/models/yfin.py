'''
@author: Youwei Zheng
@target: data models with yfinance using sqlalchemy.orm.declarative_base
@update: 2024.08.19
'''

from sqlalchemy import Column, DateTime, Float, Integer
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

class YfinSPX(BaseModel):
    __tablename__ = 'table_template'
    Date = Column(DateTime, primary_key=True)  # Use DateTime for datetime64[ns]
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(Integer)  # Volume can be Integer or Float depending on your data