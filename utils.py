"""Utility functions for the loop logo generator."""

from typing import Tuple


def parse_color(raw_color: str) -> Tuple[int, int, int, int]:
    """Convert a hex color string to an RGBA tuple. Returns transparent if 'transparent' is passed."""
    color = (raw_color or "#000000").strip()
    
    # Handle transparent background
    if color.lower() == "transparent":
        return 0, 0, 0, 0
    
    if not color.startswith("#"):
        color = f"#{color}"

    hex_value = color.lstrip("#")
    if len(hex_value) == 3:
        hex_value = "".join(ch * 2 for ch in hex_value)

    if len(hex_value) != 6:
        return 0, 0, 0, 255

    r = int(hex_value[0:2], 16)
    g = int(hex_value[2:4], 16)
    b = int(hex_value[4:6], 16)
    return r, g, b, 255

