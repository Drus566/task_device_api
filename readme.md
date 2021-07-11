# Task 'devices api' for job offer
# Versions
## 1.0
One monolit file `main.py` for whole app
## 1.1
Added distributed code

**FILES**:
- main.py - entry point app
- business_logic.py - business logic for app, like a controller of mvc pattern
- config.py 

**DIRS**
- databases - in this dir located `redis.py` and `postgresql.py` for connecting
- lib - located additional lib with funcs like a `get_mac_address`, `is_even`

# Software

## Redis-server 5.0.7
## Postgresql 13.3
## Python 3.8.10
### Packages
- aiopg 1.3.1 
- aioredis 2.0.0a1
- fastapi 0.63.0
### Server
- uvicorn 0.13.4

# Start
## Create database and load scheme
```
sudo su postgres
psql
CREATE DATABASE hardware;
<ctrl+d>
psql hardware << ./path/to/test.sql
```
## Load web-server
```
cd %folder with project%
uvicorn main:app --reload
```

# Api
## Checking two strings are they anagrams?
**GET** 
*INPUT:* `/is_anagram/<first_string>/<second_string>`
Example: http://localhost:8000/is_anagram/solo/loso
*OUTPUT*: `{ "is_anagram": <are anagram strings?>, "anagram_counter": <count of anagrams in storage> }`
Example: { "is_anagram": true, "anagram_counter": 1 }

## Adding 10 devices to the database, and adding endpoints to 5 of them
**POST**
*INPUT*: `/add_devices`
Example: http://localhost:8000/add_devices
*OUTPUT*: `none`	

## Get all devices without endpoint grouped by device type
**GET**
*INPUT*: `/get_devices_without_endpoint`
Example: http://localhost:8000/get_devices_without_endpoint
*OUTPUT*: `{ "zigbee": %count of type device%, "emeter": %count of type device%, "lora": %count of type device%, "gsm": %count of type device% }`
Example:
{
  "zigbee": 6,
  "emeter": 5,
  "lora": 2,
  "gsm": 2
}

# Problem with code
If from api will get parameters like in *is_anagram*, then in *Version-1.1* of code: 
```
@app.post("/add_devices/{param}", status_code=201)
async def add_devices(param: param):
    await postgres_connect(postgres_add_devices, param)
```
need pass **param** in each function of code, but the chain of functions is quite long:
```
async def postgres_connect(body, param):
    async with aiopg.create_pool(database=DATABASE, user=USER, password=PASSWORD, host=HOST) as pool:       
        async with pool.acquire() as conn:  
            async with conn.cursor() as cur:
               return await body(cur, param) 
```
Desire do like redis:
```
redis = await redis_connect()
await anagrams_check(redis, str_one, str_two) 
async def anagrams_check(redis, str_one, str_two):
```
