import re


def slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (used in data-test ids)."""
    return product_name.lower().replace(" ", "-")


def money(text: str) -> float:
    """Extract the first dollar amount from text like 'Item total: $29.99'."""
    match = re.search(r"\$(\d+(?:\.\d+)?)", text)
    if not match:
        raise ValueError(f"No price found in: {text!r}")
    return float(match.group(1))
