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


async def perform(fingerprint: str, access_token: str):
    """Performs your actions."""

    # open session and create client
    session = LoggingClientSession()
    client = create(
        fingerprint=fingerprint, access_token=access_token, client_session=session
    )

    # verify API
    print(await client.verify())
    print()

    # get all devices
    devices = await client.devices(include_details=True)
    print(devices)
    print()

    # call the events API
    def received(device):
        print(device)
        print(device.actual_position)
        print(device.actual_position.animation)

    client.set_event_callback(received)
    client.start()

    queue = asyncio.Queue()
    queue.put_nowait(300)
    await queue.join()
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

    # check if args are not empty
    if len(finger) == 0 or len(token) == 0:
        print("No fingerprint and/or access token provided.")
        exit(1)

    # we are async, so wait until everything completed
    loop = asyncio.get_event_loop()
    loop.run_until_complete(perform(finger, token))
