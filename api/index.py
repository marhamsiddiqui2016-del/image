from flask import Flask, request, jsonify
import requests
import httpagentparser

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Example logic using your libraries
    user_agent = request.headers.get('User-Agent', '')
    parsed_ua = httpagentparser.detect(user_agent)
    
    return jsonify({
        "message": "Hello from Vercel Python Serverless!",
        "user_agent_parsed": parsed_ua
    })
