from flask import Flask, render_template, request
from decouple import config
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify
import psycopg2
import os
import pandas as pd
import uuid

app = Flask(__name__)

# Configuração do banco de dados
DB_URI = config("DATABASE_ONR")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

# Configurações do banco de dados PostgreSQL
db_config = {
    'host': config("HOST1"),
    'database': config("DATABASE1"),
    'user': config("USER1"),
    'password': config("PASSWORD1"),
    'port': config("PORT1"),
}

# Função para encontrar o último dia útil
def ultimo_dia_util(data):
    while data.weekday() >= 5:  # 5 = sábado, 6 = domingo
        data -= timedelta(days=1)
    return data

# Rota principal com formulário de input de datas
@app.route("/consulta", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obter dados do formulário
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]
        consulta_tipo = request.form["consulta_tipo"]

        # Verificar se a data inicial é menor que a data final
        if data_inicio > data_fim:
            error_message = "Data inicial não pode ser maior que a data final."
            return render_template("index.html", error_message=error_message)

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Dicionário de consultaSQL à base do ASGARD
        queries = {
            'protocolo': "SELECT id, codigo, dominio, status, cadastro, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND protocolo_externo <> '' AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s order by cadastro asc",
            'certidao': "SELECT id, codigo, dominio, status, cadastro, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND protocolo_externo <> '' AND dominio='CERTIDAO_RI' AND status='FINALIZADO' AND cast(cadastro as date) BETWEEN %s AND %s order by cadastro asc",
            'intimacao': "SELECT id, codigo, dominio, status, cadastro, numero_controle_externo, valor_total, saldo FROM protocolo WHERE numero_controle_externo IS NOT NULL AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s order by cadastro asc",
            'pesquisa_qualificada': "SELECT id, codigo, dominio, status, cadastro, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND protocolo_externo <> '' AND dominio='CERTIDAO_RI' AND status='FINALIZADO' AND cast(cadastro as date) BETWEEN %s AND %s order by cadastro asc"
        }
        
        query = queries.get(consulta_tipo)

        # Se a consulta for nula, retornar erro
        if query is None:
            return render_template("error.html")

        # Executar a consulta SQL
        cursor.execute(query, (data_inicio, data_fim))
        resultado = cursor.fetchall()

        cursor.close()
        conn.close()


        # Configurações para leitura de arquivos da pasta
        diretorio_path = config('caminhoDiretorio')
        extensao_desejada = '.xls'

        # Chamar a função para obter a lista de arquivos
        arquivos = lista_arquivos_com_extensao_e_datas(diretorio_path, extensao_desejada, data_inicio, data_fim)

        print(arquivos)
        print(f'Tamanho Resultados: {len(arquivos)}')


        # Retornar os resultados da consulta à planilha
        if resultado:
            try:
                conn = psycopg2.connect(config("DATABASE_ONR"))
                cursor = conn.cursor()

                # Criar um DataFrame vazio para armazenar dados consolidados de todos os arquivos
                df_consolidado = pd.DataFrame()

                for arquivo in arquivos:
                    # Usar o pandas para ler os arquivos XLS
                    df_arquivo = pd.read_excel(arquivo)
                
                    # Criar um DataFrame temporário para armazenar os dados do arquivo atual
                    df_temp = df_arquivo.copy()

                    # Remover as colunas específicas da tabela consolidada
                    remover_coluna = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 12', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 23']

                    # Remover linhas e colunas que contêm valores NaN
                    df_temp = df_temp.drop(columns=remover_coluna)
                    df_temp = df_temp.drop(index=range(0,7))
                    df_temp = df_temp.dropna(axis=1, how='all')
                    df_temp = df_temp.where(pd.notna(df_temp), None)

                    # Concatenar o DataFrame atual com o DataFrame consolidado
                    df_consolidado = pd.concat([df_consolidado, df_temp], ignore_index=True)

                
                # Adicionar dados ao banco de dados
                for _, row in df_consolidado.iterrows():

                    #Gerar um UUID aleatório
                    id_aleatorio = str(uuid.uuid4())
                    data_importacao = datetime.now()

                    #Verificar se o protocolo já existe no banco de dados
                    query = "SET datestyle = dmy; SELECT id FROM protocolo_onr WHERE data_cadastro = %s AND protocolo_saec = %s order by data_cadastro asc" 
                    values = (row.iloc[0], row.iloc[2],)
                    cursor.execute(query, values)
                    df_exist_record = cursor.fetchone()


                    # Se não existir, inserir no banco de dados
                    if not df_exist_record:
                        query = "SET datestyle = dmy; INSERT INTO protocolo_onr (id, data_cadastro, data_resposta, data_importacao, protocolo_saec, valor, confirmado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        values = (id_aleatorio, row.iloc[0], row.iloc[1], data_importacao, row.iloc[2], row.iloc[3], False)
                        cursor.execute(query, values)



                
                    # Commitar as mudanças no banco de dados
                    conn.commit()
            except Exception as e:
                print(f"Erro durante a inserção: {e}")
                # Fazer rollback em caso de erro


            # Retornar os resultados da consulta
            for protocolo in resultado:
                try:
                    # Verificar se o protocolo já existe protocolo_asgard
                    query = "SELECT id FROM protocolo_asgard WHERE protocolo = %s"
                    values = (protocolo[1],)
                    cursor.execute(query, values)
                    existing_record = cursor.fetchone()

                    # Se não existir, inserir no banco de dados
                    if not existing_record:
                        query = "INSERT INTO protocolo_asgard (id, protocolo, tipo, status, cadastro, saec, valor_total, saldo, confirmado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        values = (protocolo[0], protocolo[1], protocolo[2], protocolo[3], protocolo[4], protocolo[5], protocolo[6], protocolo[7], False)
                        cursor.execute(query, values)

                        
                    # Se existir, atualizar os campos passíveis de atualização
                    else:
                        query = "UPDATE protocolo_asgard SET status = %s, valor_total = %s, saldo = %s WHERE protocolo = %s"
                        values = (protocolo[3], protocolo[6], protocolo[7], protocolo[1])
                        cursor.execute(query, values)
                        
                    # Commitar as mudanças no banco de dados
                    conn.commit()
                except Exception as e:
                    print(f"Erro durante a inserção: {e}")
                    # Fazer rollback em caso de erro

            # Feche a conexão com o banco de dados
            cursor.close()
            conn.close()

            return render_template("result-list.html", resultado=resultado)
        
        else:
            return render_template("error.html")
        

    valor_data_inicial = ultimo_dia_util(datetime.now().date() - timedelta(days=1));
    valor_data_final = datetime.now().date();

    return render_template("index.html", vdi=valor_data_inicial, vdf=valor_data_final)

# Função para listar arquivos com extensão e datas específicas
def lista_arquivos_com_extensao_e_datas(diretorio, extensao, data_inicio, data_fim):
    try:
        lista_arquivos = []

        for nome_arquivo in os.listdir(diretorio):
            caminho_completo = os.path.join(diretorio, nome_arquivo)

            if os.path.isfile(caminho_completo) and nome_arquivo.endswith(extensao):
                if nome_arquivo.startswith("RelAnalitico_") and nome_arquivo.endswith(".xls"):
                    partes_nome = nome_arquivo.split('_')

                    if len(partes_nome) >= 3:
                        data_arquivo_str = partes_nome[2].replace('.xls', '')
                        data_arquivo = data_arquivo_str

                        if data_inicio <= data_arquivo <= data_fim:
                            lista_arquivos.append(caminho_completo)

            elif os.path.isdir(caminho_completo):
                lista_arquivos.extend(lista_arquivos_com_extensao_e_datas(caminho_completo, extensao, data_inicio, data_fim))

        return lista_arquivos
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return []
     
@app.route("/conciliar", methods=["POST"])
def conciliar():
    try:
        #Obtenha os dados da tabela resultados a serem conciliados
        confirmados = request.form.getlist("confirmado[]")

        print(confirmados)

        #Conecta ao Banco de Dados
        conn = psycopg2.connect(config("DATABASE_ONR"))
        cursor = conn.cursor()

        for confirmado in confirmados:
            #Consulta campos no Banco de dados Finance
            query_onr = "SELECT * FROM protocolo_onr WHERE confirmado = %s"
            cursor.execute(query_onr, (confirmado,))
            protocolo_conciliado = cursor.fetchone()

            if protocolo_conciliado:
                #Insere os dados na tabela do Asgard
                query_asgard = "UPDATE protocolo_asgard SET confirmado = %s WHERE True = %s"
                values_asgard = (True)

                cursor.execute(query_asgard, values_asgard)

                #Insere os dados na tabela do ONR
                query_onr = "UPDATE protocolo_onr SET confirmado = %s WHERE True = %s"
                values_onr = (True)

                cursor.execute(query_onr, values_onr)

        #Commita as mudanças no Banco de Dados
        conn.commit()

        return jsonify({"success": True, "message": "Conciliação realizada com sucesso."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    finally:
        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)