import os

def listar_arquivos_com_extensao_recursivamente(diretorio, extensao):
    lista_arquivos = []
    for nome_arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, nome_arquivo)
        if os.path.isfile(caminho_completo) and nome_arquivo.endswith(extensao):
            lista_arquivos.append(caminho_completo)
        elif os.path.isdir(caminho_completo):
            lista_arquivos.extend(listar_arquivos_com_extensao_recursivamente(caminho_completo, extensao))
    return lista_arquivos

diretorio_inicial = 'P:\\Diversos\\0 - Setor Financeiro\\13.ONR - RELATÓRIO'
extensao_desejada = '.xls'

arquivos = listar_arquivos_com_extensao_recursivamente(diretorio_inicial, extensao_desejada)
for arquivo in arquivos:

    print(arquivo)
    
print(arquivos.__len__())