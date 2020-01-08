import pytest
from meetup_search.rest_api.argument_validator import (
    string_list_validator,
    filter_validator,
    positive_int_validator,
    sort_validator,
)
from typing import List


def test_string_list_validator():
    # check for valid values
    valid_values: List = [
        "name",
    ]

    for value in valid_values:
        assert string_list_validator(value=value) == value

    # check for invalid values
    invalid_values: List = [[""], 0, 0.0, True, False, "", {}]

    for value in invalid_values:
        with pytest.raises(ValueError):
            string_list_validator(value=value)


def test_filter_validator():
    # check for valid filter
    valid_values: List = [
        {"meetup_id": 1},
        {"events__meetup_id": "1"},
        {"meetup_id": 1, "events__meetup_id": "1"},
    ]

    for value in valid_values:
        assert filter_validator(value=value) == value

    # check for invalid values
    invalid_values: List = [[""], 0, 0.0, True, False, "", {}]

    for value in invalid_values:
        with pytest.raises(ValueError):
            filter_validator(value=value)


def test_positive_int_validator():
    # check for valid filter
    valid_values: List = [
        0,
        5,
        25,
    ]

    for value in valid_values:
        assert positive_int_validator(value=value) == value

    # check for invalid values
    invalid_values: List = [[""], -1]

    for value in invalid_values:
        with pytest.raises(ValueError):
            positive_int_validator(value=value)


def test_sort_validator():
    # check for valid filter
    valid_values: List = [
        # order options
        {"meetup_id": {"order": "asc", "mode": "avg"}},
        {"meetup_id": {"order": "desc", "mode": "avg"}},
        # mode options
        {"meetup_id": {"order": "asc", "mode": "min"}},
        {"meetup_id": {"order": "asc", "mode": "max"}},
        {"meetup_id": {"order": "asc", "mode": "sum"}},
        {"meetup_id": {"order": "asc", "mode": "avg"}},
        {"meetup_id": {"order": "asc", "mode": "median"}},
    ]

    for value in valid_values:
        assert sort_validator(value=value) == value

    # check for invalid values
    invalid_values: List = [
        [""],
        0,
        0.0,
        True,
        False,
        "",
        "meetup_id",
        "-meetup_id",
        {},
        {"": {"order": "asc", "mode": "avg"}},
        {"meetup_id": {"mode": "avg"}},
        {"meetup_id": {"order": "asc"}},
        {"meetup_id": {"order": "0", "mode": "avg"}},
        {"meetup_id": {"order": "asc", "mode": "0"}},
    ]

    for value in invalid_values:
        with pytest.raises(ValueError):
            sort_validator(value=value)