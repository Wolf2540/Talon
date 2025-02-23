from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import subprocess
from PIL import ImageGrab  # Built-in for Windows screenshots
from datetime import datetime

app = Flask(__name__)

SCREENSHOT_FOLDER = "static/screenshots"
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")  # Loads the web interface

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    if not data or "command" not in data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    command = data["command"]

    if command == "message":
        subprocess.Popen([
            "Powershell", "-Command",
            "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show(\'Hello World\')"
        ], shell=True)

        return jsonify({"status": "success", "message": "Message displayed"}), 200
        
    elif command == "screen":
        # Capture screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_FOLDER, filename)

        ImageGrab.grab().save(filepath)  # Take screenshot and save

        return jsonify({
            "status": "success",
            "message": "Screenshot taken",
            "image_url": f"/screenshots/{filename}"
        }), 200


    return jsonify({"status": "error", "message": "Unknown command"}), 400

@app.route("/latest_screenshot")
def latest_screenshot():
    """Returns the filename of the latest screenshot."""
    images = sorted(os.listdir(SCREENSHOT_FOLDER), reverse=True)
    latest_image = images[0] if images else None
    return {"latest_image": latest_image}

@app.route("/screenshots")
def list_screenshots():
    """List all screenshots and display them as thumbnails with links"""
    images = sorted(os.listdir(SCREENSHOT_FOLDER), reverse=True)  # Sort latest first
    return render_template("screenshots.html", images=images)

@app.route("/screenshots/<filename>")
def get_screenshot(filename):
    """Serve screenshots dynamically"""
    return send_from_directory(SCREENSHOT_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="10.0.1.179", port=5000)
