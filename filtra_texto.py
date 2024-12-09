def carregar_cardapio(arquivo):
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


def filtrar_por_dia(cardapio, dia):
    # Filtra os blocos que contêm o dia especificado
    resultados = [bloco for bloco in cardapio if bloco.startswith(f"DIA: {dia}")]
    return resultados


def main_debug(nome_arquivo, dia):
    return filtrar_por_dia(carregar_cardapio(nome_arquivo), dia)