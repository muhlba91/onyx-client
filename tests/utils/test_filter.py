"""Tests for the filters."""
from onyx_client.utils.filter import present


def test_present():
    assert present(1)


def test_not_present():
    assert not present(None)
