'''
@author: Youwei Zheng
@target: Compute Income
@update: 2024.09.30
'''

def compute_income(rph: int, hours: int, weeks: int):
    income_weekly = rph * hours
    income_yearly = income_weekly * weeks    
    
    return (income_weekly, income_yearly)