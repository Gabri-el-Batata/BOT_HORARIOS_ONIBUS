import pandas as pd
from datetime import datetime

# Constantes
saida_moras = "IDA\nSaída da Moradia para o Campus"
saida_unicamp = "VOLTA\nSaída do Campus para a Moradia"
horario_atual = datetime.now().time()

def pre_processamento(df):
    # Processando os horários da Moradia para o Campus (IDA)
    for i in range(len(df[saida_moras])):
        df.at[i, saida_moras] = df.at[i, saida_moras].replace('h', ':')
        df.at[i, saida_moras] = ''.join([c for c in df.at[i, saida_moras] if c.isdigit() or c == ':'])

    # Processando os horários do Campus para a Moradia (VOLTA)
    for i in range(len(df[saida_unicamp])):
        df.at[i, saida_unicamp] = str(df.at[i, saida_unicamp])
        if df.at[i, saida_unicamp] != "NaN":
            df.at[i, saida_unicamp] = df.at[i, saida_unicamp].replace('h', ':')
            df.at[i, saida_unicamp] = ''.join([c for c in df.at[i, saida_unicamp] if c.isdigit() or c == ':'])
    
    # Convertendo os horários para o formato datetime.time
    df[saida_moras] = pd.to_datetime(df[saida_moras], format='%H:%M').dt.time
    df[saida_unicamp] = pd.to_datetime(df[saida_unicamp], format='%H:%M').dt.time
    
    return df

def prox_horario(choice, df):
    """Função para buscar os próximos horários disponíveis."""
    if choice == "IDA":
        proximos_horarios = [h for h in df[saida_moras] if (pd.notna(h)) and (h > horario_atual)]
    elif choice == "VOLTA":
        proximos_horarios = [h for h in df[saida_unicamp] if (pd.notna(h)) and (h > horario_atual)]
    else:
        print("Obrigado por utilizar o programa!\n")
        exit()
    
    # Ordenar os horários e pegar os 3 primeiros
    return sorted(proximos_horarios)[:3]

def main_horarios(choice:str):
    # Carregar a planilha
    df = pd.read_excel('HORARIO MORADIA.xlsx')
    df_sabado = pd.read_excel('HORARIO_MORADIA_SABADO.xlsx')
    df_domingo = pd.read_excel('HORARIO_MORADIA_DOMINGO.xlsx')

    # Pré-processamento dos dados
    df = pre_processamento(df)
    df_sabado = pre_processamento(df_sabado)
    df_domingo = pre_processamento(df_domingo)

    # Exibir as opções para o usuário
    print("Olá! Como vai?\nDigite IDA para saber os próximos 3 horários para ir da MORAS até a UNICAMP\nDigite VOLTA para saber os próximos 3 horários para ir da UNICAMP até a MORAS\n")

    data_atual =  datetime.today()
    dia_da_semana = data_atual.weekday()
    
    df_escolhido = df
    
    if dia_da_semana == 5: # sabado
        print("OBS: O ônibus esta sujeito aos horários de Sabádo")
        df_escolhido = df_sabado
    elif dia_da_semana == 6:
        print("OBS: O ônibus esta sujeito aos horários de Domingo")
        df_escolhido = df_domingo

    proximos_3_horarios = prox_horario(choice, df_escolhido)

    if len(proximos_3_horarios) > 0:
        print("Esses são os 3 próximos horários de ônibus para sua escolha:")
        for horario in proximos_3_horarios:
            print(horario)
    else:
        print("Nenhum horário disponível para sua escolha. Os próximos horários em dia útil serão:")
        if choice == "IDA":
            for i in range(3):
                print(df_escolhido.at[i, saida_moras])
        else:
            for i in range(3):
                print(df_escolhido.at[i, saida_unicamp])

    return proximos_3_horarios

# Rodar a função principal
if __name__ == '__main__':
    main_horarios('IDA')
