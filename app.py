from flask import Flask, render_template, request
from decouple import config
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Consulta ao banco de dados
        if consulta_tipo == "protocolo":
            query = "SELECT codigo, dominio, cadastro, tipo_protocolo, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'certidao':
            query = "SELECT codigo, dominio, cadastro, tipo_protocolo, protocolo_externo, valor_total, saldo FROM protocolo WHERE protocolo_externo IS NOT NULL AND dominio='CERTIDAO_RI' AND status='FINALIZADO' AND cast(cadastro as date) BETWEEN %s AND %s"
        elif consulta_tipo == 'intimacao':
            query = "SELECT codigo, dominio, cadastro, tipo_protocolo, numero_controle_externo, valor_total, saldo FROM protocolo WHERE numero_controle_externo IS NOT NULL AND dominio='PROTOCOLO_RI' AND cast(cadastro as date) BETWEEN %s AND %s"
        
        cursor.execute(query, (data_inicio, data_fim))
        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        if resultado:
            return render_template("result-list.html", resultado=resultado)
        else:
            return render_template("error.html")

    valorDateInicial = ultimoDiaUtil(datetime.now().date() - timedelta(days=1));
    valorDateFinal = datetime.now().date();

    return render_template("index.html", vdi=valorDateInicial, vdf=valorDateFinal)

if __name__ == "__main__":
    app.run(debug=True)