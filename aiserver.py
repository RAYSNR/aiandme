from flask import Flask, send_from_directory

# ✅ Serve from public folder
app = Flask(__name__, static_folder='public', static_url_path='')

# ✅ Serve the homepage (youtube_input.html) at root
@app.route('/')
def serve_home():
    return send_from_directory('public', 'youtube_input.html')

# ✅ Optional: Direct access to /youtube_input.html
@app.route('/youtube_input.html')
def serve_youtube():
    return send_from_directory('public', 'youtube_input.html')

# ✅ Ping route for sanity check
@app.route('/ping')
def ping():
    return {'status': 'alive'}

# ✅ Entry point for Railway
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
