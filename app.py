from flask import Flask, jsonify
from datetime import datetime, timedelta
import psycopg2

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_config = {
    'host': '192.168.25.37',
    'database': 'asgard',
    'user': 'homologacaoUser',
    'password': 'Cartorio-2024',
    'port': '5432',
}



# Rota para consultar um protocolo por número
@app.route('/consulta_protocolo/')
def consulta_protocolo():
    try:

        # Conecta ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)

        # Cria um cursor para executar consultas
        cursor = conn.cursor()

        # Exemplo de consulta filtrando pelo número do protocolo
        cursor.execute("SELECT codigo, dominio, cadastro, tipo_protocolo FROM protocolo WHERE protocolo_externo is not null and dominio='PROTOCOLO_RI' and cast (cadastro as date) between '2023-11-01' and '2023-11-29'")

        # Obtém os resultados da consulta
        resultado = cursor.fetchall()

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()

        # Se o protocolo existir, converte para um formato JSON e o retorna
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({'mensagem': 'Protocolo não encontrado'}), 404

    except Exception as e:
        return f"Erro na consulta: {str(e)}"
    

@app.route('/consulta_certidao/')
def consulta_certidao():
    try:
        # Conecta ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)

        # Cria um cursor para executar consultas
        cursor = conn.cursor()

        # Exemplo de consulta filtrando pelo número da certidão
        cursor.execute("SELECT codigo, dominio, cadastro, tipo_protocolo FROM protocolo WHERE protocolo_externo is not null and dominio='CERTIDAO_RI' and status='FINALIZADO' and cast (cadastro as date) between '2023-11-01' and '2023-11-15'")

        # Obtém os resultados da consulta
        resultado = cursor.fetchall()

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()

        # Se o protocolo existir, converte para um formato JSON e o retorna
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({'mensagem': 'Protocolo não encontrado'}), 404

    except Exception as e:
        return f"Erro na consulta: {str(e)}"

@app.route('/consulta_intimacao/')
def consulta_intimacao():
    try:
        # Conecta ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)

        # Cria um cursor para executar consultas
        cursor = conn.cursor()

        # Exemplo de consulta filtrando pelo número do protocolo de intimação
        cursor.execute("SELECT codigo, dominio, cadastro, tipo_protocolo, numero_controle_externo FROM protocolo WHERE numero_controle_externo is not null and dominio='PROTOCOLO_RI' and cast (cadastro as date) between '2023-11-01' and '2023-11-15'")

        # Obtém os resultados da consulta
        resultado = cursor.fetchall()

        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()

        # Se o protocolo existir, converte para um formato JSON e o retorna
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({'mensagem': 'Protocolo não encontrado'}), 404

    except Exception as e:
        return f"Erro na consulta: {str(e)}"    

if __name__ == '__main__':
    app.run(debug=True)