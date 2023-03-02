# Onyx Client

[![](https://img.shields.io/github/license/muhlba91/onyx-client?style=for-the-badge)](LICENSE)
[![](https://img.shields.io/github/workflow/status/muhlba91/onyx-client/Python%20package?style=for-the-badge)](https://github.com/muhlba91/onyx-client/actions)
[![](https://img.shields.io/coveralls/github/muhlba91/onyx-client?style=for-the-badge)](https://github.com/muhlba91/onyx-client/)
[![](https://img.shields.io/pypi/pyversions/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)
[![](https://img.shields.io/pypi/v/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)
[![](https://img.shields.io/github/release-date/muhlba91/onyx-client?style=for-the-badge)](https://github.com/muhlba91/onyx-client/releases)
[![](https://img.shields.io/pypi/dm/onyx-client?style=for-the-badge)](https://pypi.org/project/onyx-client/)
[![Known Vulnerabilities](https://snyk.io/test/github/muhlba91/onyx-client/badge.svg)](https://snyk.io/test/github/muhlba91/onyx-client/)
<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="28" width="150"></a>

This repository contains a **Python HTTP client** for [Hella](https://www.hella.info)'
s [ONYX.CENTER API](https://github.com/hella-info/onyx_api).

---

## API Versions

It is encouraged to always update Hella devices to the latest software. This will, mostly, also enforce using the newest
API. In below table you can find an indication of what Hella API version is supported.

| Hella API Version | Client Version    |
|-------------------|-------------------|
| v3                | > = 3.1.0 < 6.0.0 |
| v2                | > = 2.5.0 < 3.0.0 |

## Installation

The package is published in **(Test)PyPi** and can be installed via:

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
| client_session | The initialized `aiohttp.ClientSession`. (Default: `None`, create new session.) |

### Access Control Helper

The method `onyx_client.authorizer.exchange_code` takes the **API code** and performs the exchange to a **fingerprint
and access token**. Please follow the **aforementioned documentation** to retrieve the code.

## Usage

You can **instantiate** the client using the `onyx_client.client.create` method like:

```python
import aiohttp
from onyx_client.client import create
from onyx_client.authorizer import exchange_code

# by providing the fingerprint and access token only
client = create(fingerprint="fingerprint", access_token="access_token")

# by providing the fingerprint, access token and aiohttp client session
client = create(fingerprint="fingerprint", access_token="access_token", client_session=aiohttp.ClientSession())

# by providing the configuration object
client_session = aiohttp.ClientSession()
# e.g. by exchanging the code first
config = exchange_code("code", client_session)
client = create(config=config, client_session=client_session) if client_session is not None else None
```

An **example** is shown in the **`examples` directory**.

---

## Development

The project uses [poetry](https://poetry.eustace.io/) and to install all dependencies and the build environment, run:

```bash
$ pip install poetry
$ poetry install
```

### Testing

1) Install all dependencies as shown above.
2) Run `pytest` by:

```bash
$ poetry run pytest
# or
$ pytest
```

### Linting and Code Style

The project uses [flakehell](https://github.com/life4/flakehell) as a wrapper for flake8,
and [black](https://github.com/psf/black) for automated code style fixing, also
using [pre-commit](https://pre-commit.com/).

1) Install all dependencies as shown above.
2) (Optional) Install pre-commit hooks:

```bash
$ poetry run pre-commit install
```

3) Run black:

```bash
$ poetry run black .
```

4) Run flakehell:

```bash
$ poetry run flakehell lint
```

### Building

This package uses [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) which infers the
version number based on the Git tags. Hence, to have a proper versioning for the distribution, use Python's build system
like:

```bash
$ pip install build
$ python -m build
```

Your distribution will be in the `dist` directory.

### Commit Message

This project follows [Conventional Commits](https://www.conventionalcommits.org/), and your commit message must also
adhere to the additional rules outlined in `.conform.yaml`.

---

## Release

To draft a release, use [standard-version](https://github.com/conventional-changelog/standard-version):

```bash
$ standard-version
# alternatively
$ npx standard-version
```

Finally, push with tags:

```bash
$ git push --follow-tags
```

---

## Contributions

Please feel free to contribute, be it with Issues or Pull Requests! Please read
the [Contribution guidelines](CONTRIBUTING.md)

## Supporting

If you enjoy the application and want to support my efforts, please feel free to buy me a coffe. :)

<a href="https://www.buymeacoffee.com/muhlba91" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="75" width="300"></a>
