import re
from fastapi import HTTPException

def parse_float(value: str) -> float:
    """
    Parses a string value to float, removing any non-numeric characters like 'g', 'grams', etc.
    """
    try:
        return float(re.sub(r'[^0-9.]', '', value))
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid numeric value: {value}")

def calculate_approx_calories(protein: float, fat: float, carbs: float) -> float:
    """
    Calculates approximate calories using the formula:
    protein * 4 + fat * 9 + carbs * 4
    """
    return round(protein * 4 + fat * 9 + carbs * 4, 2)
