"""Deterministic decimal arithmetic helpers with statutory rounding."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union, Optional

TWO_PLACES = Decimal("0.01")
FOUR_PLACES = Decimal("0.0001")


def to_decimal(val: Union[Decimal, float, int, str, None], default: str = "0.00") -> Decimal:
    """Safely convert any numeric representation to high-precision Decimal."""
    if val is None or val == "":
        return Decimal(default)
    try:
        # Convert float through str to avoid floating-point binary representation artifacts
        if isinstance(val, float):
            return Decimal(str(val))
        return Decimal(str(val).strip())
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid numeric input for financial calculation: '{val}'")


def quantize_currency(val: Union[Decimal, float, int, str]) -> Decimal:
    """Quantize to 2 decimal places using statutory ROUND_HALF_UP."""
    dec = to_decimal(val)
    return dec.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def quantize_rate(val: Union[Decimal, float, int, str]) -> Decimal:
    """Quantize exchange rate or tax rate to 4 decimal places."""
    dec = to_decimal(val)
    return dec.quantize(FOUR_PLACES, rounding=ROUND_HALF_UP)
