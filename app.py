from flask import Flask, render_template, request
from decouple import config
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config("DATABASE_ONR")
db = SQLAlchemy(app)

# Configurações do banco de dados PostgreSQL
db_config = {
    'host': config("HOST1"),
    'database': config("DATABASE1"),
    'user': config("USER1"),
    'password': config("PASSWORD1"),
    'port': config("PORT1"),
}

# Definindo último dia útil (looping até encontrar o último dia útil)
def ultimoDiaUtil(data):
    while data.weekday() >= 5: # 5 = sábado, 6 = domingo
        data -= timedelta(days=1)
    return data


# Rota principal com formulário de input de datas
@app.route("/consulta", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]
        consulta_tipo = request.form["consulta_tipo"]
       
        # Verificação tratativa de datas no input Inicial menor que a data final
        if data_inicio > data_fim:
            error_message = "Data inicial não pode ser maior que a data final."
            return render_template("index.html", error_message=error_message)

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Consulta ao banco de dados Asgard
        if consulta_tipo == "protocolo":
            query = "SELECT id, codigo, dominio, status, cadastro, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND protocolo_externo <> '' AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'certidao':
            query = "SELECT id, codigo, dominio, status, cadastro, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND protocolo_externo <> '' AND dominio='CERTIDAO_RI' AND status='FINALIZADO' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'intimacao':
            query = "SELECT id, codigo, dominio, status, cadastro, numero_controle_externo, valor_total, saldo FROM protocolo WHERE numero_controle_externo IS NOT NULL AND numero_controle_externo <> '' AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'pesquisa_qualificada':
            query = "SELECT id, codigo, dominio, status, cadastro, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND protocolo_externo <> '' AND dominio='CERTIDAO_RI' AND status='FINALIZADO' AND cast(cadastro as date) BETWEEN %s AND %s"
        
        cursor.execute(query, (data_inicio, data_fim))
        resultado = cursor.fetchall()

        cursor.close()
        conn.close()
        
        #Função para consultar dados da pasta local
        def listar_arquivos_com_extensao_recursivamente(diretorio, extensao):

            try:
                # Use a função listdir para obter a lista de arquivos no diretório
                lista_arquivos = []
                
                for nome_arquivo in os.listdir(diretorio):
                    caminho_completo = os.path.join(diretorio, nome_arquivo)
                    if os.path.isfile(caminho_completo) and nome_arquivo.endswith(extensao):
                        lista_arquivos.append(caminho_completo)
                    elif os.path.isdir(caminho_completo):
                        lista_arquivos.extend(listar_arquivos_com_extensao_recursivamente(caminho_completo, extensao))
                return lista_arquivos
                    

            except Exception as e:
                print(f"Erro ao listar arquivos: {e}")
                return []
   
        diretorio_inicial = config('caminhoDiretorio')
        extensao_desejada = '.xls'

        #Função para ler os arquivos da pasta
        arquivos = listar_arquivos_com_extensao_recursivamente(diretorio_inicial, extensao_desejada)

        print(arquivos)
        print(f'Tamanho Resultados: {len(arquivos)}')
             

        #Retornará os resultados da consulta caso         
        if resultado:
            
            #Detalhes de conexão PostgreSQL
            conn = psycopg2.connect(config("DATABASE_ONR"))
            cursor = conn.cursor()
            
            for protocolo in resultado:

                #Verificação se já consta no banco de dados
                cursor.execute("SELECT id FROM protocolo_asgard WHERE protocolo = %s", (protocolo[1],))
                existing_record = cursor.fetchone()

                #Se não constar, insere no banco de dados
                if not existing_record:
                                                       
                    query = "INSERT INTO protocolo_asgard (id, protocolo, tipo, status, cadastro, saec, valor_total, saldo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (protocolo[0], protocolo[1], protocolo[2], protocolo[3], protocolo[4], protocolo [5], protocolo[6], protocolo[7])

                    cursor.execute(query, values)

                #Se já constar no banco de dados, atualiza os campos passíveis de atualização
                else:
                    query = "UPDATE protocolo_asgard SET status = %s, valor_total = %s, saldo = %s WHERE protocolo = %s"
                    values = (protocolo[3], protocolo[6], protocolo[7], protocolo[1])
                    
                    cursor.execute(query, values)

            try:
                # Certifique-se de commitar para persistir as mudanças
                conn.commit()

            except Exception as e:
                print(f"Erro durante a inserção: {e}")
                #Fazer um rollback das transações
                conn.rollback()

            # Feche a conexão
            cursor.close()
            conn.close()

            return render_template("result-list.html", resultado=resultado)
        
        else:
            return render_template("error.html")
        

    valorDateInicial = ultimoDiaUtil(datetime.now().date() - timedelta(days=1));
    valorDateFinal = datetime.now().date();

    return render_template("index.html", vdi=valorDateInicial, vdf=valorDateFinal)

if __name__ == "__main__":
    app.run(debug=True)