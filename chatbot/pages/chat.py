"""
@author: Youwei Zheng
@target: Whole page
@update: 2024.09.03
"""

import taipy.gui.builder as tgb

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as chat:
    # Doc for chat control: https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/
    tgb.chat(
        "{conversation}", 
        users=users, 
        on_action=send_message, 
        sender_id="Human"
    )
