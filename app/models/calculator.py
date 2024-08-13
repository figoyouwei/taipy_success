'''
@author: Youwei Zheng
@target: Data Models
@update: 2024.08.13
'''

from pydantic import BaseModel, Field, field_validator

# ------------------------------
# User input levels
# ------------------------------

class Level(BaseModel):
    starting_level: float = Field(default=565.16)
    target_level: float = Field(default=540.00)
    
    @field_validator('starting_level', 'target_level')
    def round_two_digits(cls, value):
        return round(value, 2)

# ------------------------------
# Turing points of difference
# ------------------------------

class Point(BaseModel):
    points_net: float = 0.0
    points_pct: float = 0.0

    @field_validator('points_net', 'points_pct')
    def round_two_digits(cls, value):
        return round(value, 2)
