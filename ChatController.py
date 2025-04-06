"""
This script contains the prototype for the ChatController class.

This call is responsible for orchestrating the flow of data between the user interface and the backend services, \
ensuring that user interactions are processed effectively and efficiently.
"""

import sys
import os

# Add the directory containing ChatController.py to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import uuid # for create distinct user and chat session ID
from flask import session, request

from ChatService import ChatService # for managing data and processing messages

class ChatController():
    def __init__(self):
        self.chat_service = ChatService()
        # self.test_session = {} # to simulate session management for testing purposes

    def ensure_user_session(self):
        """Ensure user has a session ID in the test session."""
        if "user_id" not in session:
            # self.test_session["user_id"] = str(uuid.uuid4())
            session["user_id"] = str(uuid.uuid4())
        return session["user_id"]

    def create_chat(self):
        """Handle chat creation request."""
        # user_id = self.test_session.get("user_id")
        user_id = session.get("user_id")
        if not user_id:
            # instead of exception we return 401 as this will be part of API endpoint.
            # this helps with clear communication with the client
            return {"error": "Session Expired"}, 401

        chat_id = self.chat_service.create_chat(user_id)
        return {
            "chat_id": chat_id,
            "message": "Chat created successfully"
        }

    def send_message(self):
        """Handle message sending request."""
        # user_id = self.test_session.get("user_id")
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Session Expired"}, 401

        chat_id = request.json.get("chat_id")
        user_message = request.json.get("message")

        if not chat_id or not user_message:
            return {"error": "Missing Chat ID or message"}, 400

        try:
            ai_response = self.chat_service.process_message(user_id, chat_id, user_message)
            return {"message": ai_response}
        except Exception as e:
            return {"error": str(e)}, 404
        except RuntimeError as e:
            return {"error": str(e)}, 500