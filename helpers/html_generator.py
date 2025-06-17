def generate_html_output(structured_json, approx_calories, classification, scale, notes):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analysis Result</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .container {{
                text-align: center;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
            }}
            .highlight {{
                color: #007BFF;
                font-weight: bold;
            }}
            .nutrition {{
                margin-top: 20px;
                padding: 10px;
                background-color: #e7f3ff;
                border: 1px solid #007BFF;
                border-radius: 5px;
            }}
            .classification {{
                margin-top: 20px;
                padding: 10px;
                border-radius: 5px;
                color: white;
                font-weight: bold;
            }}
            .scale {{
                margin-top: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .scale div {{
                width: 20%;
                height: 20px;
            }}
            .very-healthy {{ background-color: #006400; }}
            .healthy {{ background-color: #28a745; }}
            .neutral {{ background-color: #ffc107; }}
            .unhealthy {{ background-color: #ff4500; }}
            .very-unhealthy {{ background-color: #dc3545; }}
            .arrow {{
                margin-top: 5px;
                text-align: center;
                font-size: 20px;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Analysis Result</h1>
            <p><span class="highlight">Dish Name:</span> {structured_json.get('dish_name', 'N/A')}</p>
            <p><span class="highlight">Approximate Calories:</span> {approx_calories} kcal</p>
            <div class="nutrition">
                <h2>Total Nutrition</h2>
                <p><span class="highlight">Proteins:</span> {structured_json['total_nutrition'].get('proteins', 'N/A')}</p>
                <p><span class="highlight">Carbs:</span> {structured_json['total_nutrition'].get('carbs', 'N/A')}</p>
                <p><span class="highlight">Fats:</span> {structured_json['total_nutrition'].get('fats', 'N/A')}</p>
            </div>
            <div class="classification {classification.lower()}">
                <h2>Meal Classification: {classification}</h2>
            </div>
            <div class="scale">
                <div class="very-healthy"></div>
                <div class="healthy"></div>
                <div class="neutral"></div>
                <div class="unhealthy"></div>
                <div class="very-unhealthy"></div>
            </div>
            <div class="notes" style="margin-top: 20px; text-align: left;">
                <h3>Notes:</h3>
                <ul>
                    {"".join(f"<li>{note}</li>" for note in notes.split('. ') if note)}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
