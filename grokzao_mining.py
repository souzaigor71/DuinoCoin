# grokzao_mining.py (substitua o atual)
from flask import Blueprint, send_from_directory, jsonify, current_app
import requests
import os

mining_bp = Blueprint('mining', __name__)

DUCO_USERNAME = "deef"
MINER_HTML = "miner.html"

@mining_bp.route('/minerar')
def minerar_page():
    return send_from_directory(current_app.static_folder, MINER_HTML)

def get_duco_balance(username=DUCO_USERNAME):
    try:
        r = requests.get(f"https://server.duinocoin.com/users/{username}", timeout=8)
        data = r.json()
        if data.get("success"):
            return round(data["result"]["balance"]["balance"], 4)
    except:
        pass
    return None

@mining_bp.route('/api/duco/saldo')
@mining_bp.route('/api/duco/saldo/<username>')
def duco_saldo_endpoint(username=None):
    username = username or DUCO_USERNAME
    saldo = get_duco_balance(username)
    return jsonify({
        "username": username,
        "saldo": saldo,
        "status": "ok" if saldo is not None else "erro"
    })