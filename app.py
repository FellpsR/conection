from flask import Flask, render_template, request, jsonify, redirect
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

# Rota principal com formulário de input de datas
@app.route('/consulta', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        consulta_tipo = request.form['consulta_tipo']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        if consulta_tipo == 'protocolo':
            query = "SELECT codigo, dominio, cadastro, tipo_protocolo FROM protocolo WHERE protocolo_externo IS NOT NULL AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'certidao':
            query = "SELECT codigo, dominio, cadastro, tipo_protocolo FROM protocolo WHERE protocolo_externo IS NOT NULL AND dominio='CERTIDAO_RI' AND status='FINALIZADO' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'intimacao':
            query = "SELECT codigo, dominio, cadastro, tipo_protocolo, numero_controle_externo FROM protocolo WHERE numero_controle_externo IS NOT NULL AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s"
        
        cursor.execute(query, (data_inicio, data_fim))
        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        if resultado:
            return render_template('result-list.html', resultado=resultado)
        else:
            return render-render_template('error.html')

    valor_DateInicial = datetime.now().date() - timedelta(days=1);
    valor_DateFinal = datetime.now().date();

    return render_template('index.html', vdi=valor_DateInicial, vdf=valor_DateFinal)

if __name__ == '__main__':
    app.run(debug=True)