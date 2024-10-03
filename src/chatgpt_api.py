from openai import OpenAI
from config import OPENAI_API_KEY

#If just running the chatgpt_api.py, need to call load_dotenv()
if not OPENAI_API_KEY:
    from dotenv import load_dotenv
    load_dotenv()

client = OpenAI(
    api_key= OPENAI_API_KEY,
)

# TODO: Implement the RobotController class.
# This class is responsible for controlling an LLM (Large Language Model) to facilitate human-like conversation.
# Consider whether a database might be needed to store conversations and manage sessions.

# Example usage:
# The idea is to instantiate the RobotController like this:
# robot = RobotController(type=RobotType.gpt4) or robot = RobotController(type=RobotType.gemini)
# For now, just use gpt-3.5 as the default.

# Below are some example methods that this class should implement:

# def get_response(self, session_id: int) -> str:
#     """
#     This method, get_response(), should take in a session_id, query the database to retrieve all the messages
#     from the session identified by the session_id in the SessionModel.messages attribute.
#     
#     After retrieving all the messages, send them to the AI and process the result.
#     Finally, return the AI-generated response as a string, which will be used in the conversation messages.
#
#     Example:
#     get_response(session_id=3) -> Fetch SessionModel object from the database where id = session_id,
#     retrieve all associated messages, send them to the AI model, and return the AI's response as a string.
#     """
#     pass

# def prompt_robot(self, bot_prompt: str) -> Union[str, bool]:
#     """
#     This method, prompt_robot(), is designed to take in a string (bot_prompt) that provides instructions
#     for the AI to follow. For instance, you could provide a prompt such as:
#     "You are pretending to be a 21-year-old college student in a group chat. Only respond using slang."
#     
#     The function can return either a boolean or a string, depending on the prompt or the desired behavior.
#     The returned value can indicate whether the prompt was successfully applied or provide the AI's response.
#     
#     Example:
#     prompt_robot(bot_prompt="You are pretending to be a 21-year-old college student in a group. Only respond using slang")
#     -> Could return True, or something like: "Sure! I'll only respond in slang terms. Bussin'."
#     """
#     pass

# def impersonate(self, user_id: int, prompt: str) -> str:
#     """
#     The impersonate() method should instruct the AI to generate a message as though it is impersonating a specific user,
#     guided by the provided prompt. For example, the prompt might tell the AI to generate a message as if the user is disconnected
#     or has made an error.
#     
#     The method will pass the prompt to the AI, get the response, process it (if necessary), and return the AI-generated
#     impersonation message as a string.
#     
#     Example:
#     impersonate(user_id=42, prompt="Pretend you're user 42, and the system messed up their response.")
#     -> Could return something like: "Oops, looks like my message didn't go through properly!"
#     """
#     pass

# Additional AI-related features can be added as new methods within the RobotController class.


messages = [    
            {
                "role": "system",
                "content": "You are pretending to be a 21 year old college student in a group " +
                "chat with other college students. You do not want them to find out you are a bot " +
                "as you are playing `Among Us` with them."
            },
            {
                "role": "user",
                "content": "Hi can you tell me about yourself in terms of your technical background?"
            } 
            ]

chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
)


reply = chat_completion.choices[0].message.content
print(f"ChatGPT: {chat_completion.choices}")