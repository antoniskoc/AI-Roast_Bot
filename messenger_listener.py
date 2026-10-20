
from fbchat_muqit import Client, EventType, Message, ThreadType
from ai_generator import generate_ai_roast
import time 
import os

from dotenv import load_dotenv


load_dotenv()
TARGET_THREAD_ID = os.getenv("TARGET_THREAD_ID")
TARGET_USER_ID = os.getenv("TARGET_USER_ID")


if not TARGET_THREAD_ID:
    raise RuntimeError ( " Missing TARGET_THREAD_ID in .env")

if not TARGET_USER_ID:
    raise RuntimeError ( " Missing TARGET_USER_ID in .env")


COOLDOWN_SECONDS = 30       

last_roast_at = 0.0
is_generating = False


client = Client(cookies_file_path="cookies/session.json")

@client.event(EventType.MESSAGE)
async def on_message(message: Message):
    global last_roast_at, is_generating
    
    
    if message.thread_type != ThreadType.GROUP:
        return

    if str(message.sender_id) == str(client.uid):
        return
    

    print(f"Group ID: {message.thread_id}")
    print(f"Sender ID: {message.sender_id}")

    if str(message.thread_id) != TARGET_THREAD_ID:
        return

    print(f"Message sender ID: {message.sender_id}")
    if str(message.sender_id) != TARGET_USER_ID:
        return

    print("TARGET USER DETECTED")
    
    
    text = (message.text or "").strip()
    
    if not text:
        return
    
    if is_generating:
        print("AI is already generating! ")
        return
    
    current_time = time.monotonic()
    
    if current_time - last_roast_at < COOLDOWN_SECONDS:
        print("Cooldown active! Skipping message.")
        return
    is_generating=True
    
    try:
        print("GENERATING AI ROAST")
        
        roast = await generate_ai_roast(text[:500])    
    
        if not roast.strip():
         print("AI returned empty response.")
         return
    
        sent_id = await client.send_message(
         text=roast,
         thread_id=message.thread_id
         )
        print(f"Sent message ID: {sent_id}")
    
    except Exception as error:
        print(f"AI error: {type(error).__name__}")
        return
    finally:
        last_roast_at= time.monotonic()
        is_generating=False
        
    
    
    
    
    
    

    