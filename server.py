import multiprocessing
from flask import Flask, send_from_directory
from telegram.ext import ApplicationBuilder
from telegram_duco_commands import register_duco_commands
import os

# --- Configuração do Flask ---
app = Flask(__name__, static_folder='.')

@app.route('/')
def home():
    return "<h1>✅ GrokZão + DUCO Miner Online!</h1>"

@app.route('/miner')
def miner():
    return send_from_directory('.', 'miner.html')

# --- Função do Bot (Roda em um processo isolado) ---
def run_bot_process():
    # O ApplicationBuilder criará seu próprio loop de forma limpa
    TOKEN = "8433943118:AAHipph2fV2H9rRdpzskNKCRxupX1zlAm08"
    application = ApplicationBuilder().token(TOKEN).build()
    register_duco_commands(application)
    
    print("✅ Bot do Telegram inicializado em processo isolado.")
    application.run_polling()

# --- Execução Principal ---
if __name__ == '__main__':
    print("🚀 Iniciando sistema completo...")

    # Cria o processo do bot
    bot_process = multiprocessing.Process(target=run_bot_process)
    bot_process.daemon = True # Garante que o bot feche se o servidor principal cair
    bot_process.start()

    # Roda o Flask no processo principal
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Encerrando...")
        bot_process.terminate()