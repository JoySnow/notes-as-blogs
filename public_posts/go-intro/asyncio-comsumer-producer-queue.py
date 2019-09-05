import asyncio
import random
import time


async def producer(name, queue):
    cnt = 0
    while True:
        # Get a "work item" out of the queue.
        cnt += 1
        print(f'{name} : {cnt}')
        await queue.put(f'{name}-{cnt}')

        # Sleep for the "sleep_for" seconds.
        sleep_for = random.uniform(0.05, 1.0)
        await asyncio.sleep(sleep_for)
        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def consumer(name, queue):
    # we consume only top 10
    for i in range(10):
        v = await queue.get()
        print(f'{name}: {v}, {i}')

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

    print(f'{name} is finished')


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(producer(f'producer-{i}', queue))
        tasks.append(task)

    consumer_task = asyncio.create_task(consumer('consumer-0', queue))
    tasks.append(consumer_task)

    print(f'tasks: {tasks}')

    # Wait until the queue is fully processed.
    started_at = time.monotonic()

    done, pending = await asyncio.wait(set(tasks), return_when=asyncio.FIRST_COMPLETED)
    print(f"done: {done}")
    print(f"pending: {pending}")
    print("tasks are done")

    if consumer_task in done:
        print("handle")
        # Cancel our worker tasks.
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print(f"main(): canceled {task} .")
        # Wait until all worker tasks are cancelled.
        #await asyncio.gather(*tasks, return_exceptions=True)

    total_slept_for = time.monotonic() - started_at

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    #print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


# Note: due to jupyter, the right one is un-work.
asyncio.run(main())
# await main()
