from dotenv import load_dotenv
import os
import logfire
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.mistral import MistralModel
from dataclasses import dataclass
from httpx import Client
from geocode_agent import Geocode_coordinates
from pydantic import BaseModel
from typing import Any


@dataclass
class WeatherDeps:
    Url: str
    client: Client
    Api_key: str

class weather_response(BaseModel):
    temperature: float
    description: str


weather_agent = Agent(
    model=MistralModel(
        model_name=os.getenv('MISTRAL_CHAT_MODEL'),
        api_key=os.getenv('MISTRAL_API_KEY')
    ),
    system_prompt='you are a weather forecasting agent to give climate description from coordinates by using the tool',
    result_type= weather_response,
    retries= 2,
)

@weather_agent.tool
def fetch_weather(ctx: RunContext[WeatherDeps], lat:float, lng:float)-> dict[str, Any]:
    """Get weather from the lat and lng

       Args:
            ctx: the context.
            lat: latitude of the location.
            lng: longitude of the location.

       return:
            temperature: str
            description: Any
    """
    
    res = ctx.deps.client.get(
        url= ctx.deps.Url,
        params={
            "apikey": ctx.deps.Api_key,
            "location": f"{lat},{lng}",
            "units": "metric",    
        },
        
    )
    res.raise_for_status()
    data = res.json()
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
        "temperature" : f"{values["temperatureApparent"]:0.0f}°C",
        "description" : code_lookup.get(values['weatherCode'], 'unknown'),
}
    



if __name__ == "__main__":
    load_dotenv(override=True)
    logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))
    # logfire.instrument_openai()
    logfire.instrument_httpx()

    deps = WeatherDeps(
    Url= "https://api.tomorrow.io/v4/weather/realtime",
    client=Client(),
    Api_key= os.getenv("WEATHER_API_Key"),)

    coordinates = Geocode_coordinates(lat=17.385044, lng=78.486671)
    res = weather_agent.run_sync(
    user_prompt= f"what is the weather at the given coordinates {coordinates.model_dump_json()}?",
    deps=deps,
    )
    print(res.data)
