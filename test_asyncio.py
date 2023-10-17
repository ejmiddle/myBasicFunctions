import asyncio
import random

# Simulating an async API call that returns a square of a number after a delay
async def async_api_call(x):
    delay = random.randint(1, 5)  # Simulating variable API response times
    await asyncio.sleep(delay)
    print(f"Task {x} completed after {delay} seconds.")
    return x * x

async def main():
    # Creating multiple async tasks
    tasks = [async_api_call(i) for i in range(10)]
    
    print("Tasks created. They are now running asynchronously.")
    
    # Doing something else while the tasks are running
    print("We can do other things while we wait for the tasks to complete.")
    
    # Waiting for all tasks to complete and gathering their results
    results = await asyncio.gather(*tasks)
    
    print(f"All tasks completed! Results: {results}")

# Running the main async function
asyncio.run(main())
