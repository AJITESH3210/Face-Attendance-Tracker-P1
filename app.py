from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np

app = Flask(__name__)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    
    # Get the base64 image data
    image_data = data['image'].split(',')[1]  
    image_data = base64.b64decode(image_data)  # Decode the base64 data

    # Convert the byte data to a numpy array using frombuffer
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Decode the image

    if img is None or img.size == 0:
        return jsonify({'error': 'Image not found or empty'}), 400  # Return error if image is None or empty

    # Convert to grayscale for face detection
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if any faces were found
    if len(faces) == 0:
        return jsonify({'error': 'No match found. Please recapture.'}), 400

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Encode the processed image back to base64 for sending back to the client
    _, buffer = cv2.imencode('.png', img)
    processed_image_data = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'processed_image': f"data:image/png;base64,{processed_image_data}"})

if __name__ == '__main__':
    app.run(debug=True)