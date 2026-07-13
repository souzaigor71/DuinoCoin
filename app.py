# app.py
from flask import Flask, render_template, request, jsonify
from grokzao_mining import mining_bp, get_duco_balance
import os

app = Flask(__name__)
app.register_blueprint(mining_bp)

# === Rota principal (Avatar) ===
@app.route('/')
def home():
    return send_from_directory('static', 'avatar.html')

@app.route('/miner')
def miner_page():
    return send_from_directory('static', 'miner.html')

# === API para o GrokZão usar ===
@app.route('/api/mining/status')
def mining_status():
    saldo = get_duco_balance()
    return jsonify({
        "saldo": saldo,
        "username": "deef",
        "link_miner": "/miner"
    })

# Webhook simples (WhatsApp + Telegram podem chamar)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    msg = data.get('mensagem', '').lower()
    
    if any(x in msg for x in ['saldo', 'quanto tenho', 'duco']):
        saldo = get_duco_balance()
        resposta = f"💰 Seu saldo atual é **{saldo} DUCO**" if saldo else "Não consegui consultar o saldo agora."
        return jsonify({"resposta": resposta, "emocao": "feliz"})
    
    elif any(x in msg for x in ['minerar', 'mineração', 'hash']):
        return jsonify({
            "resposta": "⛏️ Quer minerar? Abre aqui: <a href='/miner' target='_blank'>Instituto Underground Miner</a>",
            "emocao": "neutro"
        })
    
    # Aqui você pode chamar Groq normalmente para respostas gerais
    return jsonify({"resposta": "Entendi! Fale mais sobre o que quer.", "emocao": "neutro"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)