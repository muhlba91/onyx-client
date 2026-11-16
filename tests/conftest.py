from pathlib import Path
from unittest.mock import MagicMock

import aiohttp
import pytest

orig_client_response_init = aiohttp.ClientResponse.__init__


def patched_client_response_init(self, *args, **kwargs):
    kwargs.setdefault("stream_writer", MagicMock())
    orig_client_response_init(self, *args, **kwargs)


aiohttp.ClientResponse.__init__ = patched_client_response_init


FIXTURES = Path(__file__).parent / "fixtures" / "v6"


@pytest.fixture
def captured():
    """Read an anonymised capture of a real ONYX.CENTER (firmware 2.13.4)."""
    return lambda name: (FIXTURES / name).read_text()
