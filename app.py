from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)
CAMPOS_DE_BUSCA = [
    'Nome_Fantasia',
    'Razao_Social',
    'Regiao_de_Comercializacao',
    'Modalidade',
    'Cidade',
    'UF',
    'Bairro'
]

def carregar_dados():
    dados = []
    with open("resources/Relatorio_cadop.csv", newline="", encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            dados.append({k: v.strip() if isinstance(v, str) else v for k, v in row.items()})
    return dados

@app.route("/operadoras", methods=["GET"])
def buscar_operadoras():
    termo_busca = unquote(request.args.get('busca', '')).lower().strip()
    dados = carregar_dados()
    
    if not termo_busca:
        return jsonify(dados)
    
    resultados = []
    
    for registro in dados:
        for campo in CAMPOS_DE_BUSCA:
            valor = str(registro.get(campo, '')).lower().strip()
            if not valor:
                continue
                
            elif termo_busca in valor:
                resultados.append(registro)
       
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
