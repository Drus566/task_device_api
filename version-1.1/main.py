from databases.postgresql import postgres_connect
from databases.redis import redis_connect

from business_logic import postgres_get_devices_without_endpoint, anagrams_check, postgres_add_devices

from fastapi import FastAPI
from random import choice

app = FastAPI()

@app.post("/add_devices", status_code=201)
async def add_devices():
    await postgres_connect(postgres_add_devices)

@app.get("/get_devices_without_endpoint")
async def get_devices_without_endpoint(): 
    result = await postgres_connect(postgres_get_devices_without_endpoint)
    return result

@app.get("/is_anagram/{str_one}/{str_two}")
async def is_anagram(str_one: str, str_two: str):
    redis = await redis_connect()
    result = await anagrams_check(redis, str_one, str_two) 
    return result
    
