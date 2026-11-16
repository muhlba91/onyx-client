"""Server-Sent Events parser."""

from collections.abc import AsyncIterable, AsyncIterator


async def parse(lines: AsyncIterable[str]) -> AsyncIterator[tuple[str, str]]:
    """Parse Server-Sent Events from lines without line endings.

    Yields (event, data) whenever a blank line completes an event with data.
    Multi-line data is joined with newlines; comments and unknown fields are
    ignored.

    lines: the lines of the stream"""
    event, data = "message", []
    async for line in lines:
        if not line:
            if data:
                yield event, "\n".join(data)
            event, data = "message", []
            continue
        field, _, value = line.partition(":")
        value = value.removeprefix(" ")
        if field == "event":
            event = value or "message"
        elif field == "data":
            data.append(value)
