import asyncio
import getopt
from contextlib import aclosing
from sys import argv, exit

from onyx_client.client import create
from onyx_client.device.shutter import Shutter
from onyx_client.enum.verify_result import VerifyResult
from onyx_client.stream.events import DeviceChanged, Pulse, Snapshot


def print_shutter(client, device):
    """Print the position of a shutter, taking its animation into account."""
    if isinstance(device, Shutter) and device.actual_position is not None:
        position = device.actual_position.effective_value(client.now())
        print(f"{device.name}: {position:.0f}%")


async def perform(fingerprint: str, access_token: str, local_address: str):
    """Performs your actions."""

    async with create(
        fingerprint=fingerprint, access_token=access_token, local_address=local_address
    ) as client:
        # verify API
        result = await client.verify()
        print(result)
        if result != VerifyResult.OK:
            return

        # stream the state until five heartbeats were received
        pulses = 0
        async with aclosing(client.stream()) as events:
            async for event in events:
                if isinstance(event, Snapshot):
                    for device in event.devices.values():
                        print_shutter(client, device)
                elif isinstance(event, DeviceChanged):
                    print_shutter(client, event.device)
                elif isinstance(event, Pulse):
                    pulses += 1
                    if pulses == 5:
                        break


if __name__ == "__main__":
    # process command line args
    finger = ""
    token = ""
    address = None
    opts, args = getopt.getopt(
        argv[1:], "hf:t:a:", ["fingerprint=", "token=", "address="]
    )
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
    asyncio.run(perform(finger, token, address))
