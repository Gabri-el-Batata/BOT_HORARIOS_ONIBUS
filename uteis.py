from datetime import datetime
import pandas as pd

'''
Funções que auxiliam o paradigma de clean code ao trabalhar com o algoritmo do bot do telegram.
'''
NOME_PLANILHA = 'HORARIO MORADIA.xlsx'
NOME_PLANILHA_SAB = 'HORARIO_MORADIA_SABADO.xlsx'
NOME_PLANILHA_DOM = 'HORARIO_MORADIA_DOMINGO.xlsx'
SAIDA_MORAS = "IDA\nSaída da Moradia para o Campus"
SAIDA_UNICAMP = "VOLTA\nSaída do Campus para a Moradia"

def carregar_cardapio(arquivo:str) -> list:
    # Lê o arquivo e separa o conteúdo baseado no marcador "DIA: "
    with open(arquivo, 'r', encoding='utf-8') as arq:
        conteudo = arq.read()
    
    # Dividindo o conteúdo em blocos por dias
    blocos = conteudo.split("DIA: ")
    
    # Remove blocos vazios e ajusta os dados
    cardapio = []
    for bloco in blocos:
        if bloco.strip():  # Ignora blocos vazios
            cardapio.append("DIA: " + bloco.strip())
    
    return cardapio


def filtrar_por_dia(cardapio, dia) -> list:
    # Filtra os blocos que contêm o dia especificado
    resultados = [bloco for bloco in cardapio if bloco.startswith(f"DIA: {dia}")]

    resultados2 = []
    for bloco in resultados:
        bloco = bloco.replace(f"DIA: {dia}", "")
        resultados2.append(bloco)
        
    return resultados2

def detecta_dia_semana() -> list[str]:
    data_atual = datetime.today()
    dia_da_semana = data_atual.weekday()
    
    dias_semana = ['SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO', 'DOMINGO']
    
    return dias_semana[dia_da_semana]

def separa_planilha(dia_da_semana:int):
    
    df = pd.read_excel(NOME_PLANILHA)
    resposta_dia_da_semana = "DIA ÚTIL"
    
    if dia_da_semana == 5:
        df = pd.read_excel('HORARIO_MORADIA_SABADO.xlsx')
        resposta_dia_da_semana = 'SABADO'
    elif dia_da_semana == 6:
        resposta_dia_da_semana = 'DOMINGO'
        df = pd.read_excel('HORARIO_MORADIA_DOMINGO.xlsx')
    
    return  df, resposta_dia_da_semana,


def main_debug(nome_arquivo:str, dia:str) -> list:
    return filtrar_por_dia(carregar_cardapio(nome_arquivo), dia)

def pre_processamento(df):
    # Processando os horários da Moradia para o Campus (IDA)
    for i in range(len(df[SAIDA_MORAS])):
        df.at[i, SAIDA_MORAS] = df.at[i, SAIDA_MORAS].replace('h', ':')
        df.at[i, SAIDA_MORAS] = ''.join([c for c in df.at[i, SAIDA_MORAS] if c.isdigit() or c == ':'])

    # Processando os horários do Campus para a Moradia (VOLTA)
    for i in range(len(df[SAIDA_UNICAMP])):
        df.at[i, SAIDA_UNICAMP] = str(df.at[i, SAIDA_UNICAMP])
        if df.at[i, SAIDA_UNICAMP] != "NaN":
            df.at[i, SAIDA_UNICAMP] = df.at[i, SAIDA_UNICAMP].replace('h', ':')
            df.at[i, SAIDA_UNICAMP] = ''.join([c for c in df.at[i, SAIDA_UNICAMP] if c.isdigit() or c == ':'])
    
    # Convertendo os horários para o formato datetime.time
    df[SAIDA_MORAS] = pd.to_datetime(df[SAIDA_MORAS], format='%H:%M').dt.time
    df[SAIDA_UNICAMP] = pd.to_datetime(df[SAIDA_UNICAMP], format='%H:%M').dt.time
    
    return df

def prox_horario(choice:str, df)->list:
    """Função para buscar os próximos horários disponíveis."""
    
    horario_atual = datetime.now().time()
    
    if choice == "IDA":
        proximos_horarios = [h for h in df[SAIDA_MORAS] if (pd.notna(h)) and (h > horario_atual)]
    elif choice == "VOLTA":
        proximos_horarios = [h for h in df[SAIDA_UNICAMP] if (pd.notna(h)) and (h > horario_atual)]
    else:
        print("Obrigado por utilizar o programa!\n")
        exit()
    
    # Ordenar os horários e pegar os 3 primeiros
    return sorted(proximos_horarios)[:3]
