"""
Comandos DUCO + Integração com GrokZão para Telegram
Arquivo atualizado - julho/2026
"""

import requests
from telegram import Update
from telegram.ext import ContextTypes

# ================= CONFIGURAÇÕES =================
DUCO_USERNAME = "deef"
LINK_DO_MINER = "https://grokzao.onrender.com/miner"  # ← Troque pela sua URL real

# Endpoint da sua API Flask (mesmo servidor)
API_BASE = "https://grokzao.onrender.com"  # ← Mude para localhost:5000 se estiver testando local


async def saldo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o saldo DUCO"""
    username = context.args[0] if context.args else DUCO_USERNAME
    
    try:
        r = requests.get(f"{API_BASE}/api/duco/saldo/{username}", timeout=10)
        data = r.json()
        
        if data.get("saldo") is not None:
            await update.message.reply_text(
                f"💰 **Saldo de {data['username']}**\n"
                f"`{data['saldo']}` DUCO"
            )
        else:
            await update.message.reply_text("❌ Não consegui consultar o saldo no momento.")
            
    except Exception as e:
        await update.message.reply_text(f"Erro ao consultar saldo: {str(e)}")


async def minerar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia link do minerador web"""
    await update.message.reply_text(
        "⛏️ **Mineração DUCO - Instituto Underground**\n\n"
        f"🔗 Abra este link no navegador:\n"
        f"{LINK_DO_MINER}\n\n"
        "• O hashing roda no seu navegador\n"
        "• Mantenha a aba aberta\n"
        "• Pode usar até 4-6 threads no PC"
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status geral da mineração"""
    try:
        r = requests.get(f"{API_BASE}/api/mining/status", timeout=8)
        data = r.json()
        
        saldo = data.get("saldo", "??")
        
        texto = (
            "📊 **Status da Mineração**\n\n"
            f"👤 Usuário: `{data.get('username', DUCO_USERNAME)}`\n"
            f"💰 Saldo: `{saldo}` DUCO\n"
            f"🔗 Minerador: [Abrir Miner]({data.get('link_miner', LINK_DO_MINER)})"
        )
        await update.message.reply_text(texto, parse_mode='Markdown')
        
    except:
        await update.message.reply_text(
            "⚠️ Servidor de mineração não respondeu.\n"
            f"Tente: {LINK_DO_MINER}"
        )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensagem de boas-vindas"""
    await update.message.reply_text(
        "🤖 *GrokZão Online!*\n\n"
        "Comandos disponíveis:\n"
        "• /saldo → Ver saldo DUCO\n"
        "• /minerar → Link do minerador\n"
        "• /status → Status completo\n\n"
        "Pode falar normalmente também! (ex: 'qual meu saldo?')"
    )


# ================= FUNÇÃO PARA REGISTRAR NO BOT =================
def register_duco_commands(application):
    """Registre isso no seu botTeste.py ou server.py"""
    from telegram.ext import CommandHandler
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("saldo", saldo_command))
    application.add_handler(CommandHandler("minerar", minerar_command))
    application.add_handler(CommandHandler("status", status_command))
    
    print("✅ Comandos DUCO + GrokZão registrados com sucesso!")