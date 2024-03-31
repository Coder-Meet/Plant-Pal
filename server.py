from flask import Flask, request, render_template, jsonify
import os
import requests
import json
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Set your API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBKQosXb6tOzY_SbTGjV5J03i4Z21uiTms'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-data', methods=['POST'])
def submit_data():
    # Get form data
    location = request.form.get('location')
    budget = request.form.get('budget')
    timeframe = request.form.get('timeframe')
    image_file = request.files.get('image')

    # Check if an image was uploaded
    has_image = 'Yes' if image_file else 'No'

    # If an image was uploaded, convert it to base64
    if image_file:
        img = Image.open(image_file)
        img = img.resize((512, int(img.height*512/img.width)))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

    # Define the URL
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=' + os.environ['GOOGLE_API_KEY']

    # Define the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Define the data
    data = {
        'contents': [{
            'parts': [{
                'text': f'Please analyse the lighting and spacing in the room and recommend 3 plants to plants and a breif description about them, provide the output in JSON format with keys, plant-1, plant-2, plant-3'
            }, {
                'inline_data': {
                    'mime_type': 'image/jpeg',
                    'data': img_str
                }
            }]
        }]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Get the analysis result
    analysis = response.json()

    # Return the data as JSON
    data = {
        'location': location,
        'budget': budget,
        'timeframe': timeframe,
        'has_image': has_image,
        'analysis': analysis
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
