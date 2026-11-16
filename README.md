# Onyx Client

[![](https://img.shields.io/github/license/muhlba91/onyx-client?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/github/actions/workflow/status/muhlba91/onyx-client/release.yml?style=for-the-badge)](https://github.com/muhlba91/onyx-client/actions/workflows/release.yml)
[![](https://img.shields.io/coveralls/github/muhlba91/onyx-client?style=for-the-badge)](https://github.com/muhlba91/onyx-client/)
[![](https://api.scorecard.dev/projects/github.com/muhlba91/onyx-client/badge?style=for-the-badge)](https://scorecard.dev/viewer/?uri=github.com/muhlba91/onyx-client)
[![](https://img.shields.io/pypi/pyversions/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)
[![](https://img.shields.io/pypi/v/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)
[![](https://img.shields.io/github/release-date/muhlba91/onyx-client?style=for-the-badge)](https://github.com/muhlba91/onyx-client/releases)
[![](https://img.shields.io/pypi/dm/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)
[![](https://img.shields.io/github/all-contributors/muhlba91/onyx-client?color=ee8449&style=for-the-badge)](#contributors)
<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="28" width="150"></a>

This repository contains a **Python HTTP client** for [Hella](https://www.hella.info)'
s [ONYX.CENTER API](https://github.com/hella-info/onyx_api).

---

## API Versions

It is encouraged to always update Hella devices to the latest software. This will, mostly, also enforce using the newest
API. In below table you can find an indication of what Hella API version is supported.

| Hella API Version | Client Version                           |
|-------------------|------------------------------------------|
| v6                | >= 12.0.0                                |
| v3                | >= 3.1.0 (deprecated, removed in 13.0.0) |
| v2                | >= 2.5.0 < 3.0.0                         |

The client uses **v6** by default. `api_version="v3"` is still accepted for ONYX.CENTERs that do not support v6; v6-only features (automations, update status, logout, tint, active command) are unavailable then and their calls fail.

## Installation

The package is published in [**PyPi**](https://pypi.org/project/onyx-client/) and can be installed via:

```bash
pip install onyx-client
```

## Configuration

The configuration defines **connection properties** as a `dict` for the application running.

**Attention**: make sure to **read**
the [Onyx API Access Control](https://github.com/hella-info/onyx_api#access-control) description to **retrieve the
fingerprint and access token**!

| Option         | Description                                                                     |
|----------------|---------------------------------------------------------------------------------|
| fingerprint    | The fingerprint of the ONYX.CENTER.                                             |
| access_token   | The permanent access token.                                                     |
| local_address  | The local address to use (default: None).                                       |
| client_session | The initialized `aiohttp.ClientSession`. (Default: `None`, create new session.) |
| api_version    | The API version to use (default: `v6`, deprecated: `v3`).                       |

### Local Access

The local address can be used to access the ONYX.CENTER API from within the local network. If set, the client will use this address for all API requests.

### Access Control Helper

The method `onyx_client.authorizer.exchange_code` takes the **API code** and an optional **local API address**, and performs the exchange to a **fingerprint and access token**. Please follow the **aforementioned documentation** to retrieve the code.

## Usage

### Initialization

You can instantiate the client using the `onyx_client.client.create` method like:

```python
import aiohttp
from onyx_client.client import create
from onyx_client.authorizer import exchange_code

# by providing the fingerprint and access token only
client = create(fingerprint="fingerprint", access_token="access_token")

# by providing the fingerprint, access token and aiohttp client session
client = create(
    fingerprint="fingerprint",
    access_token="access_token",
    client_session=aiohttp.ClientSession(),
)

# by providing the fingerprint, access token and local API address
client = create(
    fingerprint="fingerprint", access_token="access_token", local_address="localhost"
)

# by providing the configuration object
client_session = aiohttp.ClientSession()
# e.g. by exchanging the code first
config = await exchange_code("code", client_session)
client = (
    create(config=config, client_session=client_session) if config is not None else None
)
```

### Verification

`verify()` checks the connection and returns a `VerifyResult`: `OK`, `UNREACHABLE` (also on unexpected responses), `UNAUTHORIZED` (HTTP 401/403) or `VERSION_UNSUPPORTED` (the ONYX.CENTER does not offer the configured API version).

### Streaming

`stream()` yields the state of the ONYX.CENTER as events while you iterate it. The client never runs background tasks.

```python
# all imports and a client exists...
from onyx_client.stream.events import DeviceChanged, Snapshot

async for event in client.stream():
    if isinstance(event, Snapshot):
        print(event.devices)
    elif isinstance(event, DeviceChanged):
        print(event.device)
```

| Event                | Emitted when                                                                                                |
|----------------------|-------------------------------------------------------------------------------------------------------------|
| `Snapshot`           | the stream (re)connects; carries all `devices`, `groups`, `automations` and the `update` status.            |
| `DeviceAdded`        | a device was added; carries the complete `device`.                                                          |
| `DeviceChanged`      | a device changed; carries the complete `device`.                                                            |
| `DeviceRemoved`      | a device was removed; carries its `identifier`.                                                             |
| `GroupsChanged`      | any group changed; carries all `groups`.                                                                    |
| `AutomationsChanged` | any automation changed; carries all `automations`.                                                          |
| `UpdateChanged`      | the update status changed; carries the `update` status.                                                     |
| `Pulse`              | the ONYX.CENTER sends its heartbeat (every 30 seconds on current firmware); carries its `time`.             |
| `Resynced`           | the stream reconnected; the following `Snapshot` replaces the state and is followed by the differences.     |

The client applies the patches of the stream to its own copy of the state, so every event carries complete objects. On errors, or if no data arrives for 90 seconds, it reconnects with an exponential backoff (1 to 60 seconds); rejected credentials (HTTP 401/403) raise `aiohttp.ClientResponseError`. `resync()` forces a reconnect, e.g. to periodically replace the state with a fresh snapshot. `close()` ends the stream at its next message or reconnect; break out of the loop inside `contextlib.aclosing(client.stream())` to release the connection immediately.

### Animations

ONYX reports movements as animations and keeps reporting the value from before a movement, even after it finished. Use `effective_value(client.now())` to get the current value of animated properties (e.g. `actual_position`, `actual_angle`, `actual_brightness`); `is_animating(client.now())` tells whether the property is still animated. `client.now()` is the ONYX.CENTER time, corrected by the clock offset measured on every (re)connect.

### Automations, Updates and Logout

- `automations()`, `enable_automation(identifier)` and `disable_automation(identifier)` read and switch the automations.
- `update_status()`, `check_for_update()` and `install_update()` read and install software updates of the ONYX.CENTER. Installing restarts the ONYX.CENTER; the stream reconnects once it is back.
- `logout()` revokes the access token and returns `True` if the token is invalid afterwards.

### Examples

The [`streaming`](examples/streaming/) example in the [`examples`](examples/) directory verifies the connection and streams shutter positions.

## Migration from 11.x to 12.0.0

- The client uses API **v6**; pass `api_version="v3"` to keep using v3 (deprecated, removed in 13.0.0).
- `events()`, `start()`, `stop()`, `set_event_callback()` and the `event_loop` parameters are removed; use `stream()`.
- `Configuration` raises `InvalidConfigurationException` for an unsupported `api_version`.
- `verify()` returns a `VerifyResult` instead of a boolean.
- `devices()` has no `include_details` parameter anymore and returns summaries; use `device(identifier)` for the properties.
- Devices are immutable by convention: `update_with()` and `keys()` are removed; every event carries the complete device.
- The device type is taken from the API's type only. Unknown types are `DeviceType.UNKNOWN`; `raw_type` keeps the API value.
- `NumericValue.read_only` is renamed to `readonly`. `BooleanValue` is removed; enumerations are `EnumValue`s.
- `AnimationKeyframe` takes `(value, duration, delay, interpolation)`.
- `Click` and `Switch` take the same leading arguments as all other devices; all devices accept `raw_type`, `tint` and `active_command` as keyword arguments.
- `init_device(identifier, data)` takes the complete API data; `numeric_value()`, `boolean_value()`, `onyx_client.utils.device_type`, `onyx_client.utils.filter` and `UpdateException` are removed.

---

## Development

The project uses [poetry](https://poetry.eustace.io/). Tool versions (Python, uv, Poetry) are managed with [mise](https://mise.jdx.dev): run `mise trust` and `mise install` once, then install all dependencies and the build environment:

```bash
poetry install
```

### Testing

1) Install all dependencies as shown above.
2) Run `pytest` by:

```bash
poetry run pytest
# or
pytest
```

Run mutation testing with `mutmut` by:

```bash
poetry run mutmut run
# check results
poetry run mutmut results
```

### Linting and Code Style

The project uses [ruff](https://github.com/astral-sh/ruff) for automated code linting and fixing, also using [pre-commit](https://pre-commit.com/).

1) Install all dependencies as shown above.
2) (Optional) Install pre-commit hooks:

```bash
poetry run pre-commit install
```

3) Run ruff:

```bash
poetry run ruff check .
# poetry run ruff format .
```

### Building

This package uses [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) which infers the
version number based on the Git tags. Hence, to have a proper versioning for the distribution, use Python's build system
like:

```bash
pip install build
python -m build
```

Your distribution will be in the `dist` directory.

### Commit Message

This project follows [Conventional Commits](https://www.conventionalcommits.org/), and your commit message must also
adhere to the additional rules outlined in `.conform.yaml`.

---

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://muehlbachler.io/"><img src="https://avatars.githubusercontent.com/u/653739?v=4?s=100" width="100px;" alt="Daniel Mühlbachler-Pietrzykowski"/><br /><sub><b>Daniel Mühlbachler-Pietrzykowski</b></sub></a><br /><a href="#maintenance-muhlba91" title="Maintenance">🚧</a> <a href="https://github.com/muhlba91/pulumi-proxmoxve/commits?author=muhlba91" title="Code">💻</a> <a href="https://github.com/muhlba91/pulumi-proxmoxve/commits?author=muhlba91" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MitterdorferMathias"><img src="https://avatars.githubusercontent.com/u/32190212?v=4?s=100" width="100px;" alt="Mathias Mitterdorfer"/><br /><sub><b>Mathias Mitterdorfer</b></sub></a><br /><a href="https://github.com/muhlba91/pulumi-proxmoxve/commits?author=MitterdorferMathias" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/robertweitl"><img src="https://avatars.githubusercontent.com/u/121123263?v=4?s=100" width="100px;" alt="Robert Weitlaner"/><br /><sub><b>Robert Weitlaner</b></sub></a><br /><a href="https://github.com/muhlba91/pulumi-proxmoxve/commits?author=robertweitl" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Supporting

If you enjoy the application and want to support my efforts, please feel free to buy me a coffe. :)

<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="75" width="300"></a>
