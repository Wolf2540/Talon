function sendCommand() {
    let cmd = document.getElementById("commandInput").value.trim();
    let responseMessage = document.getElementById("responseMessage");
    let screenshotPreview = document.getElementById("screenshotPreview");

    if (cmd === "") {
        responseMessage.style.color = "red";
        responseMessage.textContent = "Please enter a command!";
        return;
    }

    fetch("/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: cmd })
    })
    .then(response => response.json())
    .then(data => {
        responseMessage.style.color = data.status === "success" ? "green" : "red";
        responseMessage.textContent = data.message;

        // If a screenshot was taken, update the image source
        if (data.image_url) {
            updateLatestImage();

            //screenshotPreview.src = data.image_url + "?t=" + new Date().getTime();  // Avoid browser cache
            //screenshotPreview.style.display = "block";  // Show image
        }
    })
    .catch(error => {
        responseMessage.style.color = "red";
        responseMessage.textContent = "Error sending command!";
        console.error("Error:", error);
    });

    document.getElementById("commandInput").value = ""; // Clear input field
}

// Allow pressing "Enter" to send command
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("commandInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendCommand();
        }
    });
});


function updateLatestImage() {
    fetch('/latest_screenshot')
        .then(response => response.json())
        .then(data => {
            if (data.latest_image) {
                let timestamp = new Date().getTime(); // Prevent caching
                let imageUrl = `/screenshots/${data.latest_image}?t=${timestamp}`;
                document.getElementById("latest-img").src = imageUrl;
                document.getElementById("latest-link").href = imageUrl;
            }
        });
}

// Load the latest screenshot on page load
updateLatestImage();
