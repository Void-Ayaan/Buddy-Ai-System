import math
import re

def evaluate_math(text):
    """Safely evaluate mathematical expressions."""
    text_lower = text.lower().strip()
    
    # Replace spoken operators
    expr = text_lower.replace("calculate", "").replace("what is", "").replace("multiply by", "*").replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-").strip()

    # Percentage check (e.g. 15 percent of 250)
    pct_match = re.search(r"(\d+(?:\.\d+)?)\s*percent\s+of\s+(\d+(?:\.\d+)?)", text_lower)
    if pct_match:
        pct = float(pct_match.group(1))
        num = float(pct_match.group(2))
        res = round((pct / 100.0) * num, 2)
        return f"{pct} percent of {num} is {res}, Boss!"

    # Square root check
    sqrt_match = re.search(r"square\s+root\s+of\s+(\d+(?:\.\d+)?)", text_lower)
    if sqrt_match:
        val = float(sqrt_match.group(1))
        res = round(math.sqrt(val), 2)
        return f"The square root of {val} is {res}, Boss!"

    # Basic arithmetic expression safety evaluation
    clean_expr = re.sub(r"[^\d+\-*/().]", "", expr)
    if clean_expr:
        try:
            res = round(eval(clean_expr), 4)
            return f"The result is {res}, Boss!"
        except Exception:
            pass

    return "Could not calculate expression."
