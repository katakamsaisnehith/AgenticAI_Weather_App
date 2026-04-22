# create a free API key at https://www.tomorrow.io/weather-api/
# create a free API key at https://geocode.maps.co/

import os
from dotenv import load_dotenv
import logfire
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.mistral import MistralModel
from pydantic import BaseModel
from httpx import Client
from dataclasses import dataclass
from typing import Any
import time


load_dotenv(override=True)
logfire.configure(token=os.getenv("LOGFIRE_TOKEN"))
"""time.sleep(1)"""
logfire.instrument_httpx()


@dataclass
class All_deps:
    client :Client
    geocode_url: str
    weather_url: str
    geocode_api: str
    weather_api: str


class weather_responses(BaseModel):
    temperature: float
    description: str



agent = Agent(
    model= MistralModel(
        model_name=os.getenv('MISTRAL_CHAT_MODEL'),
        api_key=os.getenv('MISTRAL_API_KEY'),
    ),
    system_prompt=
    "You are an intelligent weather agent." \
    "Extract the geocodes for the address mentioned in userprompt using geocode agent tool." \
    "Then using the extracted latitude and longitude find the temperarture and it's description using the weather agent tool.",

    result_type=weather_responses,
    )


@agent.tool()
def extract_geocode(ctx: RunContext[All_deps], address: str) -> str:
    """
    Get the latitude and longitude for given location.

    args:
    ctx: context
    address: The name of the location.
    
    """

    res = ctx.deps.client.get(
        url= ctx.deps.geocode_url,
        params= {
            "q": address,
            "api_key": ctx.deps.geocode_api,
        },
    )
    res.raise_for_status()
    return res.json()

@agent.tool()
def extract_weather(ctx: RunContext[All_deps], lat: str, lon: str)-> dict[str, Any]:
    """
    Get weather description from the given lat and lon.

    args:
    ctx: context,
    lat: langitude of the location,
    lon: longitude of the locction

    """
    res2 = ctx.deps.client.get(
        url= ctx.deps.weather_url,
        params={
            "location": f"{lat},{lon}",
            "apikey": ctx.deps.weather_api,
            "units": "metric",
        },
    )
    res2.raise_for_status()
    data = res2.json()
    values = data["data"]["values"]

    code_lookup = {
        1000:   "Clear, Sunny",
        1100:	"Mostly Clear",
        1101:	"Partly Cloudy",
        1102:	"Mostly Cloudy",
        1001:	"Cloudy",
        2000:   "Fog",
        2100:   "Light Fog",
        4000:   "Drizzle",
        4001:   "Rain",
        4200:   "Light Rain",
        4201:   "Heavy Rain",
        5000:   "Snow",
        5001:   "Flurries",
        5100:   "Light Snow",
        5101:   "Heavy Snow",
        6000:   "Freezing Drizzle",
        6001:   "Freezing Rain",
        6200:   "Light Freezing Rain",
        6201:   "Heavy Freezing Rain",
        7000:   "Ice Pellets",
        7101:   "Heavy Ice Pellets",
        7102:   "Light Ice Pellets",
        8000:   "Thunderstorm"

    }

    return{
        "temperature" : f"{values["temperatureApparent"]:0.0f} °C",
        "description" : code_lookup.get(values["weatherCode"])

    }



deps = All_deps(
    client = Client(),
    geocode_url = "https://geocode.maps.co/search",
    weather_url = "https://api.tomorrow.io/v4/weather/realtime",

    geocode_api = os.getenv("GEOCODING_API_Key"),
    weather_api = os.getenv("WEATHER_API_Key")

)

result = agent.run_sync(
    user_prompt= f"what is the weather in Chennai?",deps=deps
    )

print(result.data)