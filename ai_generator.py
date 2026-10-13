import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()#load env variables

api_key = os.getenv("GROQ_API_KEY")

if not api_key:#get secret api keu
    raise RuntimeError("GROQ_API_KEY missing !")

#asynchronous AI client
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

async def generate_ai_roast(message_text: str) -> str:
    response = await client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content":(
                    "Jesteś sarkastycznym botem w grupie znajomych, "
                    "którzy zgodzili się na żartobliwe roasty. "
                    "Odpowiadaj po polsku jednym zwięzłym i bardzo krótkim, "
                    "kreatywnym i zabawnym dissem. "
                    "Możesz czasami nawiązać do tego, że rozmówca "
                    "przeprowadził się do Warszawy ale nie rób tego "
                    "w każdej odpowiedzi. Chociaż jak jest mozliwosc to pewnie "
                )
            },
            {
                "role": "user",
                "content": message_text
            }
        ],
        max_completion_tokens=160
    )
    
    return response.choices[0].message.content or ""

if __name__ == "__main__":
    roast = asyncio.run(
        generate_ai_roast("Dzisiaj znowu gram w LoLa")
    )

    print("AI generated roast:")
    print(roast)