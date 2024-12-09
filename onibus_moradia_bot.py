import pandas as pd
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from horarios_onibus_moradia import pre_processamento, prox_horario
from filtra_texto import main_debug

# Constantes
saida_moras = "IDA\nSaída da Moradia para o Campus"
saida_unicamp = "VOLTA\nSaída do Campus para a Moradia"
horario_atual = datetime.now().time()

# Função de comando /start no bot
TEXTO_ENTRADA = "Olá! Como vai?\nDigite /ida para saber os próximos 3 horários para ir da MORAS até a UNICAMP\nDigite /volta para saber os próximos 3 horários para ir da UNICAMP até a MORAS\nOBS: Esses são horário referentes ao dia de HOJE!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(TEXTO_ENTRADA)

def detecta_dia_semana():
    data_atual = datetime.today()
    dia_da_semana = data_atual.weekday()
    
    dias_semana = ['SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO', 'DOMINGO']
    
    return dias_semana[dia_da_semana]

async def bandeco(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    nome = "pratos_bandecos.txt"
    
    resposta = main_debug(nome, detecta_dia_semana())
    
    resp=''
    for resultado in resposta:
        resp += resultado
        await update.message.reply_text(resp)
    
    # resposta = ''
    # for prato in pratos:
    #     resposta += f"\n{prato['titulo']}\nPrato principal: {prato['prato_principal']}\nAcompanhamento: {prato['acompanhamento']}\n\n"
    # await update.message.reply_text(resposta)
        
async def ida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Carregar a planilha
    data_atual = datetime.today()
    dia_da_semana = data_atual.weekday()
    
    df = pd.read_excel('HORARIO MORADIA.xlsx')
    
    if dia_da_semana == 5:
        df = pd.read_excel('HORARIO_MORADIA_SABADO.xlsx')
    elif dia_da_semana == 6:
        df = pd.read_excel('HORARIO_MORADIA_DOMINGO.xlsx')    

    # Pré-processamento dos dados
    df = pre_processamento(df)
    
    proximos_3_horarios = prox_horario("IDA", df)
    if len(proximos_3_horarios) > 0:
        resposta = "Esses são os 3 próximos horários de ônibus:\n"
        for horario in proximos_3_horarios:
            resposta += f"{horario}\n"
    
    else: # Esse else precisa de melhora
        
        data_amanha = data_atual + timedelta(days=1)
        
        dia_semana_amanha = data_amanha.weekday()
        
        df = pd.read_excel('HORARIO MORADIA.xlsx')
        resposta_dia_da_semana = "DIA ÚTIL"
    
        if dia_semana_amanha == 5:
            resposta_dia_da_semana = 'SABADO'
            df = pd.read_excel('HORARIO_MORADIA_SABADO.xlsx')
        elif dia_semana_amanha == 6:
            resposta_dia_da_semana = 'DOMINGO'
            df = pd.read_excel('HORARIO_MORADIA_DOMINGO.xlsx')
        
        resposta = f"Nenhum horário dispónivel hoje para a IDA até a UNICAMP. Esses são os primeiros horários de amanhã ({resposta_dia_da_semana}):\n"
        
        df = pre_processamento(df)
        
        for i in range(3):
            resposta += f"{df.at[i, saida_moras]}\n"
                
    await update.message.reply_text(resposta)

async def volta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Carregar a planilha
    data_atual = datetime.today()
    dia_da_semana = data_atual.weekday()
    
    df = pd.read_excel('HORARIO MORADIA.xlsx')
    
    if dia_da_semana == 5:
        df = pd.read_excel('HORARIO_MORADIA_SABADO.xlsx')
    elif dia_da_semana == 6:
        df = pd.read_excel('HORARIO_MORADIA_DOMINGO.xlsx') 

    # Pré-processamento dos dados
    df = pre_processamento(df)
    
    proximos_3_horarios = prox_horario("VOLTA", df)
    if len(proximos_3_horarios) > 0:
        resposta = "Esses são os 3 próximos horários de ônibus:\n"
        for horario in proximos_3_horarios:
            resposta += f"{horario}\n"
    else: # Esse else precisa de melhora        
        data_amanha = data_atual + timedelta(days=1)
        
        dia_semana_amanha = data_amanha.weekday()
        
        df = pd.read_excel('HORARIO MORADIA.xlsx')
        
        resposta_dia_da_semana = 'DIA ÚTIL'
    
        if dia_semana_amanha == 5:
            resposta_dia_da_semana = 'SABADO'
            df = pd.read_excel('HORARIO_MORADIA_SABADO.xlsx')
        elif dia_semana_amanha == 6:
            resposta_dia_da_semana = 'DOMINGO'
            df = pd.read_excel('HORARIO_MORADIA_DOMINGO.xlsx')
        
        df = pre_processamento(df)
        
        resposta = f"Nenhum horário dispónivel hoje para a VOLTA até a MORAS. Esses são os primeiros horários de amanhã ({resposta_dia_da_semana}):\n"
        
        for i in range(3):
            resposta += f"{df.at[i, saida_unicamp]}\n"
                    
    await update.message.reply_text(resposta)

# Função para lidar com mensagens de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Digite /ida ou /volta para saber os horários disponíveis.")

# Função principal do bot
def main():
    # Criar o bot do Telegram
    TOKEN = "7029105684:AAEopPzkphbPcl_RtMIWe3N1pxxuPZ2ap_s" # Substitua pelo token do seu bot
    application = Application.builder().token(TOKEN).build()

    # Definir handlers para o bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ida", ida))
    application.add_handler(CommandHandler('volta', volta))
    application.add_handler(CommandHandler('bandeco', bandeco))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar o bot
    application.run_polling()

# Executar a função principal
if __name__ == '__main__':
    main()

'''
Lista de comandos no telegram:
start - Iniciar conversa
ida - Mostrar os horários de IDA da MORADIA até a UNICAMP
volta - Mostrar os horários de VOLTA da UNICAMP até a MORADIA
'''
