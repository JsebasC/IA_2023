document.addEventListener("DOMContentLoaded", function() {
    const imageInput = document.getElementById("imageInput");
    const predictedClass = document.getElementById("predictedClass");
    const imagePreview = document.getElementById("imageUpload");
    const uploadButton = document.getElementById("uploadButton");

    imageInput.addEventListener("change", function(event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            displayImage(selectedFile, imagePreview);
            sendImageForPrediction(selectedFile);
        }
    });

    uploadButton.addEventListener("click", function() {
        imageInput.click();
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
        formData.append("imageUpload", imageFile);
		console.log(fromData);
        const requestOptions = {
            method: "POST",
            body: formData,
			headers: {
            'Content-Type': 'multipart/form-data',
          },
        };

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
