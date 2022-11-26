
from orchard.utils.dig import dig, try_dig
import pytest

def test_dig(dig_obj):
    assert dig(["hello", "world", "bye"], dig_obj) == 3

def test_dig_throws_key_error_when_does_not_exist(dig_obj):
    with pytest.raises(KeyError):
        dig(["hello", "does not exist"], dig_obj)

def test_try_dig(dig_obj):
    assert try_dig(["hello", "world", "bye"], dig_obj) == 3

def test_try_dig_returns_none_when_does_not_exist(dig_obj):
    assert try_dig(["hello", "does not exist"], dig_obj) is None

def test_try_dig_returns_none_if_obj_is_none():
    assert try_dig(["a", "b", "c"], None) is None

def test_dig_with_empty_array_returns_the_original_object(dig_obj):
    assert dig([], dig_obj) == dig_obj