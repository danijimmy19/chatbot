"""
This script is used for creating RESTful API using Flask.
"""

import os
import signal
import sys
sys.path.append("..")

from flask import Flask, render_template
from ChatController import ChatController
import secrets

# Free up port 3000 if already in use
os.system("lsof -ti:3000 | xargs kill -9")

# Initialize a Flask Application
app = Flask(__name__)

# Set a secret key for session management
# app.secret_key = secrets.token_hex(16)
app.secret_key = "1234" # for demo

# Create an instance of controller to handle chat operations
chat_controller = ChatController()


# Define route for the templates page that ensures user session
# The client begins by accessing the templates route of the API.
# This step ensures that a user session is established.
@app.route("/")
def index():
    chat_controller.ensure_user_session()
    return render_template("chat.html")

# Define a route for creating a new chat session
# Before sending a message, the client needs to create a new chat session.
# This is done by sending a request to the /api/create_chat route.
@app.route("/chatbot", methods=["POST"])
def create_chat():
    # Delegate the creation of a chat session to the chat controller
    return chat_controller.create_chat()

# Define a route for sending a message in an existing chat session
# With the chat session established, the client can now send a message to the chatbot.
# This involves sending a request to the /api/send_message route, including the chat ID and the message content.
@app.route("/api/send_message", methods=["POST"])
def send_message():
    # Delegate the handling of a message to the chat controller
    return chat_controller.send_message()

def graceful_shutdown(signal_received, frame):
    print("Shutting down server and releasing port...")
    sys.exit(0)

# Attach the signal handler
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000, use_reloader=False)