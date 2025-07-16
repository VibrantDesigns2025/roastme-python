from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import openai
import random

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/roast", methods=["POST"])
def roast():
    try:
        image_file = request.files.get("image")
        roast_level = request.form.get("roastLevel", "3")

        if not image_file:
            return jsonify({"error": "No image uploaded"}), 400

        # Convert image to base64
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

        # Safe feature list (no body)
        features = [
            "hair", "lips", "eyes", "clothes",
            "ears", "jewelry", "pose", "expression", "vibe"
        ]

        # Choose features based on roast level
        level = int(roast_level) if roast_level.isdigit() else 3
        num_features = min(level, 4)
        targeted_features = random.sample(features, num_features)
        feature_list = ", ".join(targeted_features)

        # Prompt designed to prevent fallback responses
        prompt = (
            f"Roast the person's {feature_list} shown in the image. "
            f"This is roast level {level}/5. Be brutally funny, sharp, and clever — not offensive. "
            f"Comment directly on what you SEE in the image. No generic intros. Keep it under 50 words."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a roast master AI trained to visually analyze photos. "
                        "Always roast based on visible features — hair, eyes, lips, clothes, etc. "
                        "NEVER say 'I don’t know who this is'. Focus on what you see. Be direct, creative, and hilarious."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=100
        )

        roast_text = response.choices[0].message.content.strip()
        return jsonify({"roast": roast_text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
