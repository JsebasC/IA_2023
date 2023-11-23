document.addEventListener("DOMContentLoaded", function() {
    const imageInput = document.getElementById("imageInput");
    const predictedClass = document.getElementById("predictedClass");
    const imagePreview = document.getElementById("imageUpload");
	
    imageInput.addEventListener("change", function(event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
			displayImage(selectedFile, imagePreview);
            sendImageForPrediction(selectedFile);
        }
    });
	
	
    function displayImage(imageFile, imageElement) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imageElement.src = e.target.result;
        };
        reader.readAsDataURL(imageFile);
    }

    function sendImageForPrediction(imageFile) {
        const formData = new FormData();

        const requestOptions = {
            method: "POST",
            body: JSON.stringify({ imageUpload: imageFile.name }),
            headers: {
                "Content-Type": "application/json"
            }
        };
	
		console.log(requestOptions);

        fetch("http://127.0.0.1:5000/predict", requestOptions)
        .then(response => response.json())
        .then(data => {
            predictedClass.textContent = data.predicted_class;
        })
        .catch(error => {
            console.error("Error al realizar la predicción:", error);
        });
    }
});
