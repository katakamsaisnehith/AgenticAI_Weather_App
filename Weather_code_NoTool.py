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


"""
OUTPUT: 

I'm a large language model, I don't have real-time access to current weather conditions. However, I can suggest some options to find the current weather in Hyderabad:

1. Check online weather websites like AccuWeather, Weather.com, or the Indian Meteorological Department (IMD) website.
2. Use mobile apps like weather.com, AccuWeather, or Dark Sky to get the current weather conditions.

Please note that I can provide historical or general information on Hyderabad's climate, but I won't be able to provide real-time weather updates.
"""
