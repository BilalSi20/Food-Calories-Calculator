# Food Calories Calculator

## Overview
Food Calories Calculator is a FastAPI-based application designed to analyze food items from images and provide structured JSON output with detailed nutritional information. The project integrates Gemini API for image analysis and offers modularized code for scalability and maintainability.

## Features
- **Image Analysis**: Analyze food items in images and extract detailed nutritional information.
- **Structured JSON Output**: Provides structured data including calories, macronutrients, and ingredient details.
- **HTML Visualization**: Displays analysis results in a user-friendly HTML format.
- **Modular Code**: Organized into helpers, routes, and configuration files for better maintainability.
- **Customizable Configuration**: API keys and instructions are stored in a separate `config.py` file for easy updates.

## Project Structure
```
Food Calories Calculator/
├── config.py                # Configuration file for API keys and instructions
├── FoodCaloriesCalculator.py # Main FastAPI application
├── helpers/
│   ├── calculations.py      # Functions for parsing and calorie calculations
│   ├── classifications.py   # Functions for meal classification
│   ├── html_generator.py    # Functions for generating HTML output
│   ├── json_utils.py        # Functions for JSON extraction and cleaning
│   ├── structured_output.py # Functions for processing structured output
├── routes/
│   ├── analyze.py           # Endpoint for food analysis
├── images/                  # Folder for storing images and analysis results
│   ├── sample_image.jpeg    # Example image for analysis
│   ├── raw_response.txt     # Raw API response
│   ├── structured_response.json # Structured JSON output
└── README.md                # Project documentation
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Food Calories Calculator
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn requests pydantic
   ```

## Usage
1. Start the FastAPI server:
   ```bash
   uvicorn FoodCaloriesCalculator:app --reload
   ```
2. Access the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3. Test the `/upload` endpoint:
   - Use the form to upload an image for analysis.
   - View results in `images/structured_response.json` or HTML format.

## Future Development
- **Web Application**: Build a modern frontend using React or Vue.js.
- **Mobile Application**: Develop a cross-platform app with camera integration.
- **Database Integration**: Store analysis history and user data.
- **Advanced AI Models**: Enhance accuracy with machine learning.

## Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.
