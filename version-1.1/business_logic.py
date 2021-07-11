from lib.support_functions import *
from random import choice

# complex query
QUERY = "SELECT dev_type, count(*) FROM devices WHERE devices.id NOT IN (SELECT device_id FROM endpoints) GROUP BY dev_type"

# data
TYPE_DEVICES=("emeter","zigbee","lora","gsm",)

async def anagrams_check(redis, str_one, str_two):
    anagram_counter = await redis.get("anagram_counter")

    if anagram_counter == None: 
        await redis.set("anagram_counter", "0") 

    if str_one == str_two: 
        return { "is_anagram": False, "anagram_counter": anagram_counter } 
        
    str_one = sorted(str_one.lower())
    str_two = sorted(str_two.lower())

    if str_one == str_two:
        await redis.incr("anagram_counter")
        anagram_counter = await redis.get("anagram_counter")

    return  { "is_anagram": str_one == str_two, "anagram_counter": anagram_counter }

async def postgres_add_devices(cur):
    for rec in range(10):
        dev_type = choice(TYPE_DEVICES)
        dev_id = get_mac_address()
   
        await cur.execute(f"INSERT INTO devices (dev_id, dev_type) VALUES ('{dev_id}', '{dev_type}') RETURNING id")
        
        id = await cur.fetchall()
        id = id[0][0]
        
        if is_even(id): 
            comment = f"Endpoint with device id - {id}"
            await cur.execute(f"INSERT INTO endpoints (device_id, comment) VALUES('{id}', '{comment}')")

async def postgres_get_devices_without_endpoint(cur):
    await cur.execute(QUERY)
    result = await cur.fetchall()
    return dict(result)
