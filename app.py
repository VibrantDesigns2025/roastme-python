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

@app.route("/", methods=["GET"])
def health():
    return "🥩 RoastMeAI API is running!", 200

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

        # Build concise, 3‑line‑max prompt
        prompt = (
            f"Roast the person's {feature_list} shown in the image. "
            f"Level {level}/5. Be brutally funny, sharp, and clever — not offensive. "
            "Deliver your roast in **no more than 3 lines**, each line short and punchy."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You’re a roast master AI trained to visually analyze photos. "
                        "Roast only based on visible features — hair, eyes, lips, clothes, etc. "
                        "Never say “I don’t know who this is.” "
                        "Output must be **3 lines max**, each line punchy, no extra fluff."
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
    # Locally run on port 5000 or $PORT in production
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
