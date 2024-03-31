from flask import Flask, request, render_template, jsonify
import os
import requests
import json
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
  # Import the giveoutput function from main.py
app = Flask(__name__)
CORS(app)
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
    img_str = None
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
    print(response)
    url1 = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + os.environ['GOOGLE_API_KEY']
    # Define the headers
    headers1 = {
        'Content-Type': 'application/json'
    }
    
    # Define the data
    text = f'''Suggest a plant which can be planted here {location}, a budget of {budget} and someone who is {timeframe} busy. Generate a very detailed report about the following information in the format given below
        Sample HTML TO EDIT:
        <div>
            <h1>Plant Report: [Plant Name]</h1>

            <h3>Plant Description</h3>
            <p>Generate a very deatiled description of the plant</p>

            <h3>Care Routine</h3>
            <p>Generate a very detailed care routine including the amount of times to water the plant</p>

            <h3>Logistics</h3>
            <p>Step by step on how to plant this plant in HTML format, ensure its very detailed</p>

            <h3>Sustainability Impact</h3>
            <p>How the cultivation of [Plant Name] contributes to sustainability efforts by [mention environmental benefits]. It also helps in combating climate change by [mention its impact on carbon dioxide levels], exagerate on this.</p>
        </div>
        </html>
        Here is Sample Output:
        <div>
    <h1>Plant Report: Sunflower</h1>

    <h3>Plant Description</h3>
    <p>Sunflowers (Helianthus annuus) are annual plants native to the Americas. They are known for their tall, sturdy stems and bright, cheerful flowers that track the sun's movement throughout the day. The flowers consist of a central disk surrounded by golden-yellow petals, and they can grow up to 12 inches (30 cm) in diameter. Sunflowers are not only ornamental but also provide seeds that are rich in nutrients and oil.</p>

    <h3>Care Routine</h3>
    <p>To care for your sunflower, plant it in well-draining soil in a location that receives full sunlight. Water the plant regularly, keeping the soil evenly moist but not waterlogged. Sunflowers have deep taproots, so occasional deep watering is beneficial, especially during dry periods. Fertilize the plant with a balanced fertilizer once a month during the growing season to encourage healthy growth and abundant blooms.</p>

    <h3>Logistics</h3>
    <p>To plant sunflowers, follow these steps:
        <ol>
            <li>Choose a sunny location with well-draining soil.</li>
            <li>Prepare the soil by loosening it to a depth of at least 6 inches (15 cm).</li>
            <li>Sow sunflower seeds directly into the soil, spacing them 6 to 12 inches (15 to 30 cm) apart.</li>
            <li>Cover the seeds with a thin layer of soil and water gently.</li>
            <li>Keep the soil consistently moist until the seeds germinate, typically within 7 to 10 days.</li>
            <li>Once the seedlings have developed several sets of true leaves, thin them to the desired spacing.</li>
            <li>Provide support for tall varieties by staking them or using a trellis.</li>
            <li>Monitor for pests and diseases, and take appropriate action if necessary.</li>
            <li>Enjoy watching your sunflowers grow and bloom!</li>
        </ol>
    </p>

    <h3>Sustainability Impact</h3>
    <p>The cultivation of sunflowers contributes significantly to sustainability efforts. Sunflowers are known for their ability to absorb heavy metals and toxins from the soil, thus helping to remediate contaminated land and improve soil health. Furthermore, sunflower cultivation promotes biodiversity by providing habitat and food for various pollinators and wildlife.</p>
    <p>Moreover, sunflowers play a crucial role in combating climate change. They are highly efficient at sequestering carbon dioxide from the atmosphere through photosynthesis, converting it into biomass and organic matter. This helps to mitigate the greenhouse effect and reduce the overall carbon footprint. Sunflower fields act as carbon sinks, capturing and storing carbon in the soil, which can remain stored for long periods.</p>
</div>

        '''
    data1 = {
        'contents': [{
            'parts': [{
                'text': text
            }]
        }]
    }
    # Make the POST request
    response1 = requests.post(url1, headers=headers1, data=json.dumps(data1))
    # Get the analysis result
    #analysis1 = response1.json()

    # Return the data as JSON
    # data = {
    #     'analysis' : response1,
    # }
    return response1.json()

if __name__ == '__main__':
    app.run(debug=True)
