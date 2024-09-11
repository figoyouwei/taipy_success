'''
@author: Youwei Zheng
@target: Home page with navbar
@update: 2024.09.11
'''

import taipy.gui.builder as tgb

with tgb.Page() as page:
    tgb.text("# Multi-page Application", mode="md", class_name="text-center")
    tgb.navbar(class_name="center-navbar")
