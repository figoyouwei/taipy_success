from stateclass import State


def request(state: State, prompt: str) -> str:
    """
    Send a prompt to the GPT-4 API and return the response.

    Args:
        - state: The current state of the app.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    print(prompt)
    random_response = [
        "How are you?",
        "What are you doing?",
        "What is your name?",
        "Who are you?",
    ]

    import numpy as np

    return random_response[np.random.randint(0, 4)]

    response = state.client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-4-turbo-preview",
    )
    return response.choices[0].message.content
