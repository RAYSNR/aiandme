from flask import Flask, request, jsonify, send_from_directory
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Initialize Flask app with public folder
app = Flask(__name__, static_folder='public', static_url_path='')

# Serve static index from root
@app.route('/')
def serve_index():
    return send_from_directory('public', 'youtube_input.html')

# API route to log YouTube video URL to Google Sheets
@app.route('/api/logVideoUrl', methods=['POST'])
def log_video_url():
    data = request.json
    video_url = data.get("youtube_url", "").strip()

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        # Load Google API credentials from Railway env var
        creds_dict = json.loads(os.environ['GOOGLE_KEY_JSON'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            ['https://www.googleapis.com/auth/spreadsheets']
        )

        client = gspread.authorize(creds)
        sheet = client.open("AIHUB_QuizData_Master").worksheet("quiz_submission")

        # Log to sheet
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, video_url])

        return jsonify({"message": "Logged successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check
@app.route('/health')
def health_check():
    return "OK", 200

# Serve other static files (optional fallback)
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
