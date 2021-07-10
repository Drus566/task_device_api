# Task 'devices api' for job offer

# Python 3.8.10
## Packages
- aiopg 1.3.1 
- aioredis 2.0.0a1
- fastapi 0.63.0
## Server
- uvicorn 0.13.4

# Start
cd <folder with project>
uvicorn main:app --reload

# Api
## Checking two strings are they anagrams?
## GET 
### INPUT: /is_anagram/<first_string>/<second_string>
http://localhost:8000/is_anagram/solo/loso
### OUTPUT: { "is_anagram": <are anagram strings?>, "anagram_counter": <count of anagrams in storage> }
{ "is_anagram": true, "anagram_counter": 1 }

## Adding 10 devices to the database, and adding endpoints to 5 of them
## POST 
### INPUT: /add_devices
http://localhost:8000/add_devices
### OUTPUT: none 

## Get all devices without endpoint grouped by device type
## GET 
### INPUT: /get_devices_without_endpoint
http://localhost:8000/get_devices_without_endpoint
### OUTPUT: { "zigbee": <count of type device>, "emeter": <count of type device>, "lora": <count of type device>, "gsm": <count of type device> }
{
  "zigbee": 6,
  "emeter": 5,
  "lora": 2,
  "gsm": 2
}




