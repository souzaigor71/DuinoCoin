"""
Webhook Flask que recebe mensagens do serviço Baileys (whatsapp_baileys/index.js)
e responde com informações do DUCO, ou repassa pro cérebro normal do
GrokZão/Alien quando não é um comando de mineração.

USO NO SEU app.py PRINCIPAL:
    from whatsapp_webhook import whatsapp_bp
    app.register_blueprint(whatsapp_bp)

Configure no serviço Node (whatsapp_baileys/index.js) a variável de ambiente
PYTHON_WEBHOOK apontando pra onde este Flask está rodando, ex:
    PYTHON_WEBHOOK=http://localhost:5000/whatsapp/webhook node index.js
"""
from flask import Blueprint, request, jsonify
from grokzao_mining import get_duco_balance

whatsapp_bp = Blueprint('whatsapp', __name__)

LINK_DO_MINER = "https://SEU-SITE.onrender.com"  # troque pela URL real do Render


@whatsapp_bp.route('/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    data = request.get_json(force=True) or {}
    text = (data.get('text') or '').strip().lower()
    from_jid = data.get('from')

    reply = None

    if 'saldo' in text or 'quanto tenho' in text:
        saldo = get_duco_balance()
        if saldo is not None:
            reply = f"💰 Saldo atual: {saldo} DUCO"
        else:
            reply = "Não consegui consultar o saldo agora, tenta de novo daqui a pouco."

    elif 'minerar' in text or 'mineração' in text:
        reply = f"⛏️ Pra minerar, abra este link no navegador: {LINK_DO_MINER}"

    else:
        # Aqui você conecta com a lógica normal do GrokZão/Alien,
        # chamando a função que já processa mensagens e gera resposta
        # com o Groq. Por exemplo:
        # reply = gerar_resposta_alien(text, canal="whatsapp", remetente=from_jid)
        reply = None

    return jsonify({"reply": reply})
