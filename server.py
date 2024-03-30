from flask import Flask, request, jsonify
import requests  # Import requests library
import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
app = Flask(__name__)

@app.route('/submit-data', methods=['POST'])
def submit_data():
  # Get data from request form
    data = request.form.to_dict()
    with open("image.jpg", "rb") as image_file:
        content = base64.b64encode(image_file.read()).decode("utf-8")

    image1 = Part.from_data(data=base64.b64decode(content), mime_type="image/png")
    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
    [image1, f"Please anaylse the lighting and spacing in the room {data.get('location')} and recomend 3 types of plants to plant."],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        stream = True,
    )

    #response is a json

    return jsonify(responses)

if __name__ == '__main__':
  app.run(debug=True)
