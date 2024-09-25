from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# TODO: The pre-prompt is not working as expected, needs to figure out why role: system is not working. 
# maybe it is outdated.
messages = [ {"role": "system",
            "content": "You are pretending to be a 21 year old college student in a group chat with other college students. You do not want them to find out you are a bot as you are playing `Among Us` with them.",
            "role": "user",
            "content": "Hi can you tell me about yourself in terms of your technical background?"} ]

# chat = client.ChatCompletion.create(
#     model="gpt-3.5-turbo", messages=messages
# )
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
)

reply = chat_completion.choices[0].message.content
print(f"ChatGPT: {reply}")