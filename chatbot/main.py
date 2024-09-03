"""
@author: Youwei Zheng
@target: Main app
@update: 2024.09.03
"""

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    # Retrieve the API key from the environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
