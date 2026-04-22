import os
from dotenv import load_dotenv
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from httpx import Client
from geocode_agent import *
from weather_agent import *

load_dotenv(override=True)
logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))
logfire.instrument_httpx()


def workflow(
        user_prompt: str,
        geocode_deps: GeoCodeDeps,
        weather_deps: WeatherDeps
    ):

    geocode_result = Geocode_agent.run_sync(user_prompt=user_prompt,
                                            deps=geocode_deps)
    coordinates = geocode_result.data
    
    weather_result = weather_agent.run_sync(
        user_prompt= f"what is the weather at the give coordinates{coordinates.model_dump_json()}",
        deps=weather_deps)
    
    return weather_result.data




def main(user_prompt: str):
    load_dotenv(override=True)
    logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))
    logfire.instrument_httpx()
    logfire.instrument_openai()

    client = Client()
    geocode_deps = GeoCodeDeps(
        url="https://geocode.maps.co/search",
        client= client,
        Api_key=os.getenv("GEOCODING_API_Key")
    )
    
    weather_deps = WeatherDeps(
        Url="https://api.tomorrow.io/v4/weather/realtime",
        client=client,
        Api_key=os.getenv('WEATHER_API_Key')
    )

    result = workflow(user_prompt, geocode_deps, weather_deps)
    print(result)




if __name__ == "__main__":

    user_prompt = "what is the weather in Mumbai"
    response = main(user_prompt)
    print(response)














"""agent = Agent(MistralModel(
    model_name=os.getenv('MISTRAL_CHAT_MODEL'),
    api_key=os.getenv('MISTRAL_API_KEY')
    ),
    system_prompt=""
)"""

