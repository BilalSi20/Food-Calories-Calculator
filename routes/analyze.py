import os
import base64
import logging
import json
from fastapi import APIRouter, HTTPException
import requests
from helpers.json_utils import extract_and_clean_json_block

router = APIRouter()

@router.get("/analyze-food")
def analyze_food():
    try:
        logging.info("Starting food analysis from 'images' folder.")
        # Görsel dosyasını otomatik olarak 'images' klasöründen al
        image_path = os.path.join(os.getcwd(), "images", "sample_image.jpeg")  # Dinamik dosya yolu
        if not os.path.exists(image_path):
            logging.error(f"Image not found at path: {image_path}")
            raise HTTPException(status_code=404, detail="Image not found")

        # Görseli Base64 formatına çevir
        with open(image_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')

        logging.info("Sending image to Gemini API.")
        # Gemini API'ye JSON gövdesi ile gönderim
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyCsyrZxq8hiLugQ8_7r1UJyv7UY-octaW0",
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": base64_image
                                }
                            },
                            {
                                "text": """You are a Food Analysis AI. Your task is to analyze food items from the provided image and return a detailed structured JSON output."""
                            }
                        ]
                    }
                ]
            },
            headers={"Content-Type": "application/json"}
        )

        logging.info("Received response from Gemini API.")

        # Log raw response for debugging
        raw_response_text = response.text
        logging.debug(f"Raw API response: {raw_response_text}")

        # Extract JSON content from raw response
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
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logging.error(f"Error during food analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
