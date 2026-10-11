
from fbchat_muqit import Client, EventType, Message, ThreadType

client = Client(cookies_file_path="cookies/session.json")

@client.event(EventType.MESSAGE)
async def on_message(message: Message):
    if message.thread_type != ThreadType.GROUP:
        return
    
    if str(message.sender_id) == str(client.uid):
        return
    
    print(f"Group ID: {message.thread_id}")
    print(f"Sender ID: {message.sender_id}")
    
if __name__ == "__main__":
    print("Starting Messenger listener...")
    client.run()
    