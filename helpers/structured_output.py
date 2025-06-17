import os
import json
import logging
from helpers.json_utils import extract_and_clean_json_block

def process_structured_output(raw_response_text):
    try:
        outer_json = json.loads(raw_response_text)
        inner_text = outer_json["candidates"][0]["content"]["parts"][0]["text"]
        structured_json = extract_and_clean_json_block(inner_text)

        # Save structured JSON to a separate file
        structured_response_path = os.path.join(os.getcwd(), "images", "structured_response.json")
        with open(structured_response_path, "w", encoding="utf-8") as structured_file:
            json.dump(structured_json, structured_file, indent=4)

        return structured_json
    except ValueError as e:
        logging.error("Error processing structured output: %s", str(e))
        raise ValueError("Failed to process structured output.")
