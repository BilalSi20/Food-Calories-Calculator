import os
from fastapi import FastAPI, HTTPException, UploadFile, File
import requests
from pydantic import BaseModel
import logging
import base64
import json
import re
from fastapi.responses import HTMLResponse
from routes.analyze import router as analyze_router
from helpers.json_utils import extract_and_clean_json_block
from helpers.structured_output import process_structured_output
from helpers.html_generator import generate_html_output
from helpers.calculations import parse_float, calculate_approx_calories
from helpers.classifications import classify_meal, classify_meal_with_scale, classify_meal_with_scale_v2, classify_meal_with_scale_v3, classify_meal_with_notes
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, GEMINI_API_URL, ANALYSIS_INSTRUCTIONS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create FastAPI app
app = FastAPI(title="Gemini Food Analysis API")

# Register the router
app.include_router(analyze_router)

# Define structured output model
class NutritionInfo(BaseModel):
    proteins: str
    carbs: str
    fats: str

class FinalResult(BaseModel):
    ingredient_name: str
    ingredient_weight_or_volume: str
    ingredient_calories: str
    ingredient_nutrition: NutritionInfo

class FoodAnalysis(BaseModel):
    dish_name: str
    weight_or_volume: str
    calories: str
    ingredients: list[FinalResult]
    total_nutrition: NutritionInfo

@app.get("/analyze-food")
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
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}",
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
                                "text": ANALYSIS_INSTRUCTIONS
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
        
        """
        # Save raw response to a file for analysis

        raw_response_path = os.path.join(os.getcwd(), "images", "raw_response.txt")
        with open(raw_response_path, "w", encoding="utf-8") as raw_file:
            raw_file.write(raw_response_text)
            
        """

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

@app.get("/extract-json")
def extract_json():
    try:
        logging.info("Reading raw response from file.")
        raw_response_path = os.path.join(os.getcwd(), "images", "raw_response.txt")
        with open(raw_response_path, "r", encoding="utf-8") as file:
            raw_text = file.read()

        logging.info("Extracting JSON content.")
        outer_json = json.loads(raw_text)
        inner_text = outer_json["candidates"][0]["content"]["parts"][0]["text"]
        result = extract_and_clean_json_block(inner_text)

        logging.info("JSON extraction successful.")
        return result
    except Exception as e:
        logging.error(f"Error during JSON extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/upload", response_class=HTMLResponse)
def upload_form():
    """
    Returns an HTML form for image upload.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Food Image</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
            }
            form {
                margin-top: 20px;
            }
            input[type="file"] {
                margin-bottom: 20px;
            }
            button {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Upload Food Image for Analysis</h1>
            <form action="/upload-analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <br>
                <button type="submit">Analyze</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/upload-analyze", response_class=HTMLResponse)
def upload_analyze(file: UploadFile = File(...)):
    """
    Handles image upload, analyzes the image, and returns the result.
    """
    try:
        logging.info("Received image for analysis.")

        # Save the uploaded file temporarily
        if not file.filename:
            raise HTTPException(status_code=400, detail="Uploaded file must have a valid name.")

        temp_file_path = os.path.join(os.getcwd(), "images", file.filename)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())

        # Analyze the uploaded image
        with open(temp_file_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')

        logging.info("Sending uploaded image to Gemini API.")
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}",
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
                                "text": ANALYSIS_INSTRUCTIONS
                            }
                        ]
                    }
                ]
            },
            headers={"Content-Type": "application/json"}
        )

        logging.info("Received response from Gemini API.")

        # Extract JSON content from raw response
        raw_response_text = response.text
        try:
            outer_json = json.loads(raw_response_text)
            inner_text = outer_json["candidates"][0]["content"]["parts"][0]["text"]
            structured_json = extract_and_clean_json_block(inner_text)

            # Save structured JSON to a separate file
            structured_response_path = os.path.join(os.getcwd(), "images", "structured_response.json")
            with open(structured_response_path, "w", encoding="utf-8") as structured_file:
                json.dump(structured_json, structured_file, indent=4)

            # Process structured output
            structured_json = process_structured_output(raw_response_text)

            # Parse nutrition values
            protein = parse_float(structured_json["total_nutrition"].get("proteins", "0"))
            fat = parse_float(structured_json["total_nutrition"].get("fats", "0"))
            carbs = parse_float(structured_json["total_nutrition"].get("carbs", "0"))

            # Calculate approximate calories
            approx_calories = calculate_approx_calories(protein, fat, carbs)

            # Classify the meal with scale
            classification, scale, notes = classify_meal_with_notes(
                cal=approx_calories,
                protein=protein,
                fat=fat,
                carbs=carbs
            )

            # Generate HTML output
            return generate_html_output(structured_json, approx_calories, classification, scale, notes)
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logging.error(f"Error during image upload and analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
