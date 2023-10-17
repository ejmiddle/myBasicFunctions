import asyncio
import random

# Simulating an async API call that returns a square of a number after a delay
async def async_api_call(x, maxSeconds = 1, taskIdent=0):
    # delay = random.randint(1, maxSeconds)  # Simulating variable API response times
    delay = maxSeconds  # Simulating variable API response times
    await asyncio.sleep(delay)
    print(f"Task {x} completed after {delay} seconds for task {taskIdent}.")
    return x * x

async def main():
    # Creating multiple async tasks
    tasks = [async_api_call(i,5, taskIdent=1) for i in range(20)]
    print("Task 1 created. They are now running asynchronously.")
    print("Wait for a few seconds")
    await asyncio.sleep(15)  # wait for 5 seconds

    print("Wait for a few seconds")
    tasks2 = [async_api_call(i, maxSeconds=10, taskIdent=2) for i in range(5)]
    
    print("All Tasks created. They are now running asynchronously.")
    
    # Doing something else while the tasks are running
    print("We can do other things while we wait for the tasks to complete.")
    
    # Waiting for all tasks to complete and gathering their results
    results = await asyncio.gather(*tasks)

    print(f"All tasks completed! Results: {results}")

    # Waiting for all tasks to complete and gathering their results
    results = await asyncio.gather(*tasks2)
    
    print(f"All tasks2 completed! Results: {results}")

# Running the main async function
asyncio.run(main())
