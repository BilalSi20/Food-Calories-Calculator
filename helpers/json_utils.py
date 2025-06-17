import re
import logging
import json

def extract_and_clean_json_block(text: str) -> dict:
    """
    Extracts and parses a JSON code block (```json ... ```) from the text,
    cleaning unwanted newlines inside string values.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("Starting precise JSON extraction from raw text.")

    # 1. ```json ... ``` arasını bul
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, text, re.DOTALL)

    if not match:
        logging.error("No JSON code block found.")
        raise ValueError("No valid JSON code block found.")

    raw_json_block = match.group(1)
    logging.debug(f"Extracted JSON content: \n{raw_json_block[:300]}...")

    # 2. Satır içi bölünmüş stringleri düzelt (örn: \"fats\": \"4 \ngrams\" gibi)
    cleaned_json = re.sub(r'\s*\n\s*', ' ', raw_json_block)  # satır içi boşlukları tek satıra indir
    cleaned_json = re.sub(r'\s{2,}', ' ', cleaned_json)      # aşırı boşlukları azalt
    cleaned_json = cleaned_json.strip()

    logging.debug(f"Cleaned JSON content: \n{cleaned_json[:300]}...")

    # Parse the cleaned JSON string into a dictionary
    try:
        parsed_json = json.loads(cleaned_json)
    except json.JSONDecodeError as e:
        logging.error("Failed to parse cleaned JSON string.")
        raise ValueError("Invalid JSON format.") from e

    return parsed_json
