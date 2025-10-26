import asyncio
import getopt
from sys import argv

import aiohttp

from onyx_client.client import create
from onyx_client.data.device_command import DeviceCommand


class LoggingClientSession(aiohttp.ClientSession):
    """Used to intercept requests and to be logged."""

    def __init__(self, enable_logging: bool = True):
        """Initialize the custom logging session."""
        self.enable_logging = enable_logging
        super().__init__()

    async def _request(self, method, url, **kwargs):
        if self.enable_logging:
            print(f"Starting request {method} {url} {kwargs}\n")
        return await super()._request(method, url, **kwargs)


async def shutter_worker(queue, client, device_id):
    """Worker processing our position commands."""
    while True:
        position = await queue.get()
        print(
            await client.send_command(
                device_id, DeviceCommand(properties={"target_position": position})
            )
        )
        await asyncio.sleep(15)
        queue.task_done()


async def perform(fingerprint: str, access_token: str, local_address: str):
    """Performs your actions."""

    # open session and create client
    session = LoggingClientSession()
    client = create(
        fingerprint=fingerprint, access_token=access_token, client_session=session, local_address=local_address
    )

    # verify API
    print(await client.verify())
    print()

    # get all devices
    devices = await client.devices(include_details=True)
    print(devices)
    print()

    # get first device in list
    device_id = devices[0].identifier
    device_id = "5e2912f7-f25e-4f16-bf1a-6cb967a08261"
    device = await client.device(device_id)
    print(device)
    print()

    # assumption: shutter!
    # move shutter to 10%,
    # wait a few seconds,
    # move shutter back to where it was
    queue = asyncio.Queue()
    queue.put_nowait(10)
    queue.put_nowait(90)
    task = asyncio.create_task(shutter_worker(queue, client, device_id))
    print()

    # call the streaming API for 11 devices
    index = 1
    async for device in client.events():
        print(device)
        print(device.actual_position)
        print(device.actual_position.animation)
        index += 1
        if index == 11:
            break
    print()

    # cleanup
    await queue.join()
    task.cancel()
    await session.close()


if __name__ == "__main__":
    # process command line args
    finger = ""
    token = ""
    opts, args = getopt.getopt(argv[1:], "hf:t:", ["fingerprint=", "token="])
    for opt, arg in opts:
        if opt in ("-f", "--fingerprint"):
            finger = arg
        elif opt in ("-t", "--token"):
            token = arg
        elif opt in ("-a", "--address"):
            address = arg

    # check if args are not empty
    if len(finger) == 0 or len(token) == 0:
        print("No fingerprint and/or access token provided.")
        exit(1)

    # we are async, so wait until everything completed
    loop = asyncio.get_event_loop()
    loop.run_until_complete(perform(finger, token, address))
