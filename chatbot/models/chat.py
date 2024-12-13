"""
@author: Youwei Zheng
@target: Chat Message Model
@update: 2024.09.11
"""

import uuid
from typing import List
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    message_id: int
    content: str
    sender: str


class ChatSession(BaseModel):
    # user_session_id: str
    chat_session_no: int = 1
    chat_session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[ChatMessage]

    def add_message(self, content: str, sender: str):
        # Changed 'id' to 'message_id' to match the class definition
        new_id = len(self.messages) + 1
        self.messages.append(ChatMessage(message_id=new_id, content=content, sender=sender))

    def update_messages(self, new_messages: List[ChatMessage]):
        """Update the session messages with new messages."""
        self.messages = new_messages
        print(f"Session {self.chat_session_no} messages updated.")  # Changed session_no to chat_session_no
        
    def to_list(self) -> List[List[str]]:
        """Convert ChatMessage instances to a list of lists."""
        return [[str(msg.message_id), msg.content, msg.sender] for msg in self.messages]

    @classmethod
    def from_list(cls, message_list: List[List[str]]):
        """Convert a list of lists to ChatMessage instances and create a ChatSession."""
        messages = [
            ChatMessage(message_id=int(item[0]), content=item[1], sender=item[2])
            for item in message_list
        ]
        return cls(messages=messages)
    

class SessionCollection(BaseModel):
    sessions: List[ChatSession] = []

    def add_session(self, session: ChatSession):
        """Add a new ChatSession to the collection."""
        self.sessions.append(session)

    def get_session(self, session_id: str) -> ChatSession:
        """Retrieve a ChatSession by its session_id."""
        for session in self.sessions:
            if session.chat_session_id == session_id:
                return session
        return None  # Return None if no session with the given ID is found
