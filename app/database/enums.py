from .utils.breeds import get_breeds

import enum


def create_str_enum(name: str, *values: str, **vals: str) -> enum.Enum:
    """Dynamically create a str Enum."""

    val = {val: val for val in values} if not vals else vals

    return enum.Enum(name, val, type=str)


Breeds = create_str_enum("Breeds", **get_breeds())
