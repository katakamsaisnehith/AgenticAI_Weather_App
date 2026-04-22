import os
import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.mistral import MistralModel
from httpx import Client
from dataclasses import dataclass
from pydantic import BaseModel

load_dotenv(override=True)
logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))
logfire.instrument_httpx()


@dataclass
class GeoCodeDeps:
    url : str
    client: Client
    Api_key: str

class Geocode_coordinates(BaseModel):
    lat: float
    lng: float


Geocode_agent = Agent(
    model= MistralModel(
        model_name=os.getenv('MISTRAL_CHAT_MODEL'),
        api_key=os.getenv('MISTRAL_API_KEY'),
    ),
    system_prompt="You are an intelligent agent to find the geo coordinates.",
    result_type=Geocode_coordinates,
    deps_type=GeoCodeDeps

)


@Geocode_agent.tool
def fetch_lat_long(ctx: RunContext[GeoCodeDeps], Address:str) -> str:
    """Get the latitude and longitude of a Address.

    Args:
         ctx: The context.
         Address: A discription of a address.
    """

    res = ctx.deps.client.get(
        url= ctx.deps.url,
        params={
            "q" : Address,
            "api_key": ctx.deps.Api_key,
        },
    )
    return res.json()


"""deps = geocode_deps(
    url = "https://geocode.maps.co/search",
    client = Client(),
    Api_key = os.getenv('GEOCODING_API_Key'))

result = Geocode_agent.run_sync(user_prompt='what is the weather in Hyderabad, India?',deps=deps)
print(result.data)"""



if __name__=="__main__":
    load_dotenv(override=True)
    logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))
    logfire.instrument_httpx()
    
    deps = GeoCodeDeps(
    url = "https://geocode.maps.co/search",
    client = Client(),
    Api_key = os.getenv('GEOCODING_API_Key'))
    result = Geocode_agent.run_sync(user_prompt='what is the weather in Hyderabad, India?',deps=deps)
    print(result.data)