"""
This script is used for creating Chat Manager to efficiently handle data. More Specifically, this script contains model
layer of MVC architecture.
"""

import sys
sys.path.append("..")

import uuid

class ChatManager():
    def __init__(self):
        self.chats = {} # first_key: user_id --> second_key:chat_id --> chat_data

    def create_chat(self, user_id, chat_id, system_prompt):
        """Create a new chat for a user."""
        if user_id not in self.chats:
            self.chats[user_id] = {}

        self.chats[user_id][chat_id] = {
            "system_prompt": system_prompt,
            "messages": []
        }

    def get_chat(self, user_id, chat_id):
        """Get chat by user_id, and chat_id."""
        return self.chats.get(user_id, {}).get(chat_id)

    def add_message(self, user_id, chat_id, role, content):
        """Add a message to a chat."""
        # chat = self.get_chat(user_id, chat_id)
        # if chat:
        #     chat["messages"].append({"role": role, "content": content})
        if chat := self.get_chat(user_id, chat_id):
            chat["messages"].append({"role": role, "content": content})

    def get_conversation(self, user_id, chat_id):
        """Get full conversation including system message."""
        if chat := self.get_chat(user_id, chat_id):
            system_message = {"role": "system", "content": chat["system_prompt"]}
            return [system_message] + chat["messages"]
        return []

def load_system_prompt(file_path: str) -> str:
    """Load system prompt from file."""
    try:
        with open(file_path, "r") as file:
            return file.read()
    except ValueError as e:
        print(f"Error in loading system prompt: {e}")
        return "You are a helpful assistant."

if __name__ == "__main__":
    # load the system prompt
    system_prompt_path = "system_prompt.txt"
    system_prompt = load_system_prompt(system_prompt_path)

    # initialize manager
    manager = ChatManager()

    # Create a new chat_id
    id = str(uuid.uuid4())
    user_id = "user_" + id
    chat_id = "chat_" + id

    manager.create_chat(user_id, chat_id, system_prompt)
    manager.add_message(user_id, chat_id, "user", "Hello!")
    manager.add_message(user_id, chat_id, "assistant", "Hi there!")

    # Get the chat history
    conversation = manager.get_conversation(user_id, chat_id)

    ################### Example with multiple messages ###################
    # Add some messages
    messages = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"},
        {"role": "assistant", "content": "I'm just a program, but I'm here to help!"}
    ]

    # add all messages to the chat using add_message function
    for message in messages:
        manager.add_message(user_id, chat_id, message["role"], message["content"])

    # get all the conversations using get_conversation function
    conversations = manager.get_conversation(user_id, chat_id)

    # print each message's role and content from conversation
    # conversations is list of dictionaries [{}]
    for role, content in conversations[0].items():
        print(f"role: {role} \n content: {content}")