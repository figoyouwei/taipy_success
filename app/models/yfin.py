'''
@author: Youwei Zheng
@target: data models with yfinance using sqlalchemy.orm.declarative_base
@update: 2024.08.19
'''

from sqlalchemy import Column, DateTime, Float, Integer
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

class BaseIndex(BaseModel):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class
    Date = Column(DateTime, primary_key=True)  # Use DateTime for datetime64[ns]
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(Integer)  # Volume can be Integer or Float depending on your data
    Range = Column(Float)
    RangePct = Column(Float)

class SPX(BaseIndex):
    __tablename__ = 'table_spx'  # Specify the table name for SPX

class NDX(BaseIndex):
    __tablename__ = 'table_ndx'  # Specify the table name for NDX
