from unittest.mock import MagicMock

import aiohttp

orig_client_response_init = aiohttp.ClientResponse.__init__


def patched_client_response_init(self, *args, **kwargs):
    kwargs.setdefault("stream_writer", MagicMock())
    orig_client_response_init(self, *args, **kwargs)


aiohttp.ClientResponse.__init__ = patched_client_response_init
