document.addEventListener('DOMContentLoaded', function() {
    // Camera functionality
    const cameraBtn = document.getElementById('camera');
    const video = document.getElementById('camera-stream');
    const canvas = document.getElementById('camera-canvas');
    const photoDisplay = document.getElementById('photo');
    const uploadBox = document.getElementById('upload-box');
    const countdownDisplay = document.getElementById('countdown');
    
    let countdownTimer;
    let countdown = 5;
    
    // Handle camera capture button
    cameraBtn.addEventListener('click', function() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            if (confirm("Camera will automatically take a picture in 5 seconds. Make sure the object is in frame. Continue?")) {
                startCamera();
            }
        } else {
            alert("Sorry, your browser doesn't support camera access");
        }
    });
    
    function startCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                video.style.display = 'block';
                
                // Add video to upload box
                if (uploadBox.contains(photoDisplay)) {
                    photoDisplay.style.display = 'none';
                }
                uploadBox.appendChild(video);
                
                // Show and set countdown
                countdownDisplay.style.display = 'block';
                countdownDisplay.textContent = countdown;
                
                // Start countdown
                countdown = 5;
                countdownTimer = setInterval(function() {
                    countdown--;
                    countdownDisplay.textContent = countdown;
                    
                    if (countdown <= 0) {
                        takePhoto(stream);
                        clearInterval(countdownTimer);
                    }
                }, 1000);
            })
            .catch(function(error) {
                console.error("Error accessing camera:", error);
                alert("Unable to access camera: " + error.message);
            });
    }
    
    function takePhoto(stream) {
        // Setup canvas for capturing
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get the image data
        const imageData = canvas.toDataURL('image/png');
        
        // Stop the camera stream
        stream.getTracks().forEach(track => track.stop());
        
        // Hide countdown and video
        countdownDisplay.style.display = 'none';
        video.style.display = 'none';
        
        // Display the captured image
        photoDisplay.src = imageData;
        photoDisplay.style.display = 'block';
    }
});