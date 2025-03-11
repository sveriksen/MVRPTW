"""Simple module to render numbers more cleanly"""

def format_number(num: int | float) -> str:
    """
    Returns a string representation of a number with spaces as thousand separators.
    Args:
        num (int | float): The number to format.
    Returns:
        str: The formatted number as a string.
    """
    return f"{num:,}".replace(",", " ")
