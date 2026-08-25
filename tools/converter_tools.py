import re
import requests

def convert_units(text):
    """Convert currency, length, weight, and temperature."""
    text_lower = text.lower().strip()

    # 1. Currency Conversion (USD, INR, EUR, GBP)
    curr_match = re.search(r"(\d+(?:\.\d+)?)\s*(usd|inr|eur|gbp)\s+to\s+(usd|inr|eur|gbp)", text_lower)
    if curr_match:
        amount = float(curr_match.group(1))
        from_curr = curr_match.group(2).upper()
        to_curr = curr_match.group(3).upper()

        rates = {
            "USD": 1.0,
            "INR": 83.5,
            "EUR": 0.92,
            "GBP": 0.79
        }

        if from_curr in rates and to_curr in rates:
            in_usd = amount / rates[from_curr]
            converted = round(in_usd * rates[to_curr], 2)
            return f"{amount} {from_curr} is approximately {converted} {to_curr}, Boss!"

    # 2. Length Conversion (Miles <-> KM)
    dist_match = re.search(r"(\d+(?:\.\d+)?)\s*(miles|mile|km|kilometers|kilometer)\s+to\s+(miles|mile|km|kilometers|kilometer)", text_lower)
    if dist_match:
        val = float(dist_match.group(1))
        unit1 = dist_match.group(2)
        if "mile" in unit1:
            res = round(val * 1.60934, 2)
            return f"{val} miles is equal to {res} kilometers, Boss!"
        else:
            res = round(val / 1.60934, 2)
            return f"{val} kilometers is equal to {res} miles, Boss!"

    # 3. Weight Conversion (KG <-> LBS)
    weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(kg|kilograms|lbs|pounds)\s+to\s+(kg|kilograms|lbs|pounds)", text_lower)
    if weight_match:
        val = float(weight_match.group(1))
        unit1 = weight_match.group(2)
        if "kg" in unit1 or "kilogram" in unit1:
            res = round(val * 2.20462, 2)
            return f"{val} kilograms is equal to {res} pounds, Boss!"
        else:
            res = round(val / 2.20462, 2)
            return f"{val} pounds is equal to {res} kilograms, Boss!"

    return "Please specify a conversion like 'convert 100 USD to INR' or 'convert 5 miles to km'."
