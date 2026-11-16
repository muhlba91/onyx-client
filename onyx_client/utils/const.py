"""Constants for the Onyx Client."""

API_URL = "https://api.hella.link"
API_HEADERS = {
    "Content-Type": "application/json",
}
API_VERSION = "v6"
DEPRECATED_API_VERSION = "v3"
AUTHORIZE_API_VERSION = "v3"
STREAM_CONNECT_TIMEOUT = 10
STREAM_READ_TIMEOUT = 90  # seconds, three missed pulses
STREAM_MAX_BACKOFF = 60
