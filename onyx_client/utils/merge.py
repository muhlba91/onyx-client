"""JSON Merge Patch (RFC 7386)."""

from typing import Any


def merge_patch(target: Any, patch: Any) -> Any:
    """Apply a JSON merge patch to the target without modifying it.

    Objects are merged recursively, null removes a key, anything else replaces.

    target: the JSON document to patch
    patch: the JSON merge patch"""
    if not isinstance(patch, dict):
        return patch
    result = dict(target) if isinstance(target, dict) else {}
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = merge_patch(result.get(key), value)
    return result
