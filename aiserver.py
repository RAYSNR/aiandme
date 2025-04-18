from flask import Flask, request, jsonify, send_from_directory
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory('static', 'youtube_input.html')

@app.route('/api/logVideoUrl', methods=['POST'])
def log_video_url():
    data = request.json
    video_url = data.get("youtube_url", "").strip()

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        creds_dict = json.loads(os.environ['GOOGLE_KEY_JSON'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            ['https://www.googleapis.com/auth/spreadsheets']
        )
        client = gspread.authorize(creds)
        sheet = client.open("AIHUB_QuizData_Master").worksheet("quiz_submission")
        sheet.append_row([datetime.now().isoformat(), video_url], value_input_option='USER_ENTERED')
        return jsonify({"message": "Logged successfully!"})
    except Exception as e:
        print("Error logging to Google Sheets:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
