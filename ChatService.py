"""
This script is used for integrating the language model with chat sessions, allowing us to process user messages generated AI responses.
"""

import uuid
from openai import OpenAI

import sys
import os

# Add the directory containing ChatController.py to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from ChatManager import ChatManager

# initialize openai client
API_KEY = ''

class ChatService():
    def __init__(self):
        self.chat_manager = ChatManager()
        self.openai_client = OpenAI(api_key=API_KEY)
        self.system_prompt = self.load_system_prompt('system_prompt.txt')

    def load_system_prompt(self, file_path: str) -> str:
        """Load the system prompt from file."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error in loading system prompt: {e}")
            return "You're a helpful assistant."

    def create_chat(self, user_id: str) -> str:
        """Create a new chat session."""
        chat_id = uuid.uuid4()
        self.chat_manager.create_chat(user_id, chat_id, self.system_prompt)
        return chat_id

    def process_message(self, user_id: str, chat_id: str, message: str) -> str:
        """Process a user message and get AI response."""

        # Step 1: Retrieve the chat
        chat = self.chat_manager.get_chat(user_id, chat_id)
        if not chat:
            raise ValueError("Chat not found")

        # Step 2: Add user message to chat history
        self.chat_manager.add_message(user_id, chat_id, "user", message)

        try:
            # Step 3: Get AI response
            conversation = self.chat_manager.get_conversation(user_id, chat_id)

            response = self.openai_client.chat.completions.create(
                mode="gpt-4",
                messages=conversation,
                temperature=0.7,
                max_tokens=500
            )

            ai_message = response.choices[0].message.content

            # Step 4: Add AI response to chat history
            self.chat_manager.add_message(user_id, chat_id, "assistant", ai_message)
            return ai_message
        except Exception as e:
            # Step 5: Handle exception
            raise RuntimeError(f"Error getting AI response: {e}")