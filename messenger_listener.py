
from fbchat_muqit import Client, EventType, Message, ThreadType
from ai_generator import generate_ai_roast



TARGET_THREAD_ID = "1463018129078170"
TARGET_USER_ID = "100012027947618"  #for now my fb id for the test group

client = Client(cookies_file_path="cookies/session.json")

@client.event(EventType.MESSAGE)
async def on_message(message: Message):
    if message.thread_type != ThreadType.GROUP:
        return

    if str(message.sender_id) == str(client.uid):
        return

    print(f"Group ID: {message.thread_id}")
    print(f"Sender ID: {message.sender_id}")

    if str(message.thread_id) != TARGET_THREAD_ID:
        return

    if str(message.sender_id) != TARGET_USER_ID:
        return

    print("TARGET USER DETECTED")
    
    
    text = (message.text or "").strip()
    command = "!roastbot_ai "
    
    if not text.startswith(command):
        return
    
    prompt = text[len(command):].strip()
    
    if not prompt:
        return
    try:
        roast= await generate_ai_roast(prompt)
    except Exception as error:
        print(f"AI error: {type(error).__name__}")
        return
    
    sent_id = await client.send_message(
        text=roast,
        thread_id=message.thread_id
    )
    
    print(f"Sent message ID: {sent_id}")
    
    
    
if __name__ == "__main__":
    print("Starting Messenger listener...")
    client.run()
    