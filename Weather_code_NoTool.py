from dotenv import load_dotenv
import os
import logfire
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

load_dotenv(override=True)

logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))


agent = Agent(
    model=GroqModel(
        model_name=os.getenv('GROQ_MODEL'),
        api_key=os.getenv('GROQ_API_KEY')
    ),
    system_prompt='you are helpful assistant'
)

response = agent.run_sync(user_prompt='what is the current weather in hyderabad? give in short')
print(response.data)
