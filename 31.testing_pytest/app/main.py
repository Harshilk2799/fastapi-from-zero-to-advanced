# Sync

def add(a, b):
    return a + b 


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b 


# Async 
import asyncio 

async def async_add(a, b):
    await asyncio.sleep(1)
    return a + b 

async def async_divide(a, b):
    await asyncio.sleep(1)
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b 