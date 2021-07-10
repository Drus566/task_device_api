# aioredis version 2.0.0
import aioredis
import aiopg
import asyncio

from fastapi import FastAPI
from random import randrange, choice

app = FastAPI()

@app.post("/add_devices", status_code=201)
async def add_devices():
    await process_postgres()

@app.get("/get_devices_without_endpoint")
async def get_devices_without_endpoint(): 
    async with aiopg.create_pool(database=DATABASE, user=USER, password=PASSWORD, host=HOST) as pool:       
        async with pool.acquire() as conn:  
            async with conn.cursor() as cur:
                await cur.execute(QUERY)
                result = await cur.fetchall()
                return dict(result)
        
@app.get("/is_anagram/{str_one}/{str_two}")
async def is_anagram(str_one: str, str_two: str):
    redis = await aioredis.from_url(REDIS_URL)
    anagram_counter = await redis.get("anagram_counter")

    if anagram_counter == None: await redis.set("anagram_counter", "0") 
    if str_one == str_two: return {"is_anagram": False, "anagram_counter": anagram_counter } 
        
    str_one = sorted(str_one.lower())
    str_two = sorted(str_two.lower())

    if str_one == str_two:
        await redis.incr("anagram_counter")
        anagram_counter = await redis.get("anagram_counter")

    return { "is_anagram": str_one == str_two, "anagram_counter": anagram_counter }

async def process_postgres():
    async with aiopg.create_pool(database=DATABASE, user=USER, password=PASSWORD, host=HOST) as pool:       
        async with pool.acquire() as conn:  
            async with conn.cursor() as cur:
                for rec in range(10):
                    # for endpoint
                    dev_type = choice(TYPE_DEVICES)
                    dev_id = get_mac_address()
    
                    # `RETURNING id` - get created record id
                    await cur.execute(f"INSERT INTO devices (dev_id, dev_type) VALUES ('{dev_id}', '{dev_type}') RETURNING id")

                    # get id from query
                    id = await cur.fetchall()
                    # get id from list and tuple.
                    id = id[0][0]
    
                    # for add endpoint for device
                    if is_even(id): 
                        comment = f"Endpoint with device id - {id}"
                        await cur.execute(f"INSERT INTO endpoints (device_id, comment) VALUES('{id}', '{comment}')")

def get_mac_address():
    mac = []
    for byte in range(6):
        byte = hex(randrange(256)).replace('0x', '').zfill(2)
        mac.append(byte)
    mac = ':'.join(mac)
    return mac

def get_ip_address():
    ip = []
    for byte in range(4):
        byte = str(randomrange(256))
        ip.append(byte)
    ip = '.'.join(ip)
    return ip

def is_even(num):
    if num % 2 == 0:
        return True 
    else:
        return False

# complex query
QUERY = "SELECT dev_type, count(*) FROM devices WHERE devices.id NOT IN (SELECT device_id FROM endpoints) GROUP BY dev_type"

# data
TYPE_DEVICES=("emeter","zigbee","lora","gsm",)

# config 
REDIS_URL="redis://localhost:6379"
DATABASE="hardware"
USER="postgres"
PASSWORD="6101"
HOST="localhost"

