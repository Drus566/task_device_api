import aiopg
from config import * 

async def postgres_connect(body):
    async with aiopg.create_pool(database=DATABASE, user=USER, password=PASSWORD, host=HOST) as pool:       
        async with pool.acquire() as conn:  
            async with conn.cursor() as cur:
               return await body(cur) 

