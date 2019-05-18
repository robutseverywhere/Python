# Python3.7.3
# Asyncio example, thank you HackerNoon!

import asyncio
import time

# definition of a coroutine
async def coroutine_1():
    print('coroutine_1 is active on the event loop')

    print('coroutine_1 yielding control. Going to be blocked for 4 seconds')
    await asyncio.sleep(4)

    print('coroutine_1 resumed. coroutine_1 exiting')

# definition of a coroutine
async def coroutine_2():
    print('coroutine_2 is active on the event loop')

    print('coroutine_2 yielding control. Going to be blocked for 5 seconds')
    await asyncio.sleep(5)

    print('coroutine_2 resumed. coroutine_2 exiting')

# this is the event loop
loop = asyncio.get_event_loop()

# schedule both the coroutines to run on the event loop
loop.run_until_complete(asyncio.gather(coroutine_1(), coroutine_2()))

print('\n')

# Second example.

# this is a coroutine definition
async def fake_network_request(request):
    print('making network call for request:  ' + request)
    # simulate network delay
    await asyncio.sleep(1)

    return 'got network response for request: ' + request

# this is a coroutine definition
async def web_server_handler():
    # schedule both the network calls in a non-blocking way.

    # ensure_future creates a task from the coroutine object, and schedules it on the event loop
    task1 = asyncio.ensure_future(fake_network_request('one'))

    # another way to do the scheduling
    task2 = asyncio.get_event_loop().create_task(fake_network_request('two'))

    # simulate a no-op blocking task. This gives a chance to the network requests scheduled above to be executed.
    await asyncio.sleep(0.5)

    print('doing useful work while network calls are in progress...')

    # wait for the network calls to complete. Time to step off the event loop using await! 
    await asyncio.wait([task1, task2])

    print(task1.result())
    print(task2.result())

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.ensure_future(web_server_handler()))


print('\n')

# Third example.

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")


# Now an example that is Synchronous.
""" This is 2.13 seconds longer than the previous example with
the first three run throughs although .2 seconds shorter with
the fourth run through."""


def count():
    print("One")
    time.sleep(1)
    print("Two")

def main():
    for _ in range(3):
        count()

if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")