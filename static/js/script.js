document.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('capture');
    const startButton = document.getElementById('start');
    const capturedImageDiv = document.getElementById('capturedImage');
    const originalImageDiv = document.getElementById('originalImage');

    // Start the camera when the Start button is clicked
    startButton.addEventListener('click', function() {
        navigator.mediaDevices.getUserMedia({ video: true        })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error("Error accessing the camera: ", error);
        });
    });

    // Capture the image when the Capture button is clicked
    captureButton.addEventListener('click', function() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0);
        
        // Get the captured image data
        const imageData = canvas.toDataURL('image/png');

        // Display the captured image
        capturedImageDiv.innerHTML = `<img src="${imageData}" alt="Captured Image">`;

        // Send the captured image to the server for face detection
        fetch('/capture', {
            method: 'POST',
            body: JSON.stringify({ image: imageData }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.length > 0 && data[0] !== "Unknown") {
                originalImageDiv.innerHTML = `<img src="/images/${data[0]}" alt="Original Image">`;
                alert(`Attendance tracked for: ${data[0]}`);
            } else {
                originalImageDiv.innerHTML = `<p>No match found. Please recapture.</p>`;
            }
        })
        .catch(error => {
            console.error("Error capturing image: ", error);
        });
    });
});