"""Subsystem Base Class."""

from math import ceil


class Subsystem():
    """Base Class for all Subsystems of the Spacecraft."""

    def _roundup(x, next_largest):
        """Rounds a number up to the next largest."""
        return float(ceil(x / next_largest)) * next_largest

    def _format_number(x):
        """Formats a number."""
        return "{:.2f}".format(x)
