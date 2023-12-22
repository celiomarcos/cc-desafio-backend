from flask import Flask, jsonify, request, render_template
from .models import ContaBancaria
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

contas = [
    ContaBancaria(
        id=1,
        tipo="corrente",
        saldo=1000.0,
        extrato=[
            {'data': '01/12/2023', 'descricao': 'Compra', 'valor': 50.0},
            {'data': '05/12/2023', 'descricao': 'Depósito', 'valor': 200.0},
            {'data': '10/12/2023', 'descricao': 'Pagamento de conta', 'valor': -150.0},
            {'data': '15/12/2023', 'descricao': 'Transferência enviada', 'valor': -200.0},
            {'data': '20/12/2023', 'descricao': 'Depósito', 'valor': 300.0},
        ],
        titular="Maria da Silva"
    ),
    ContaBancaria(
        id=2,
        tipo="poupanca",
        saldo=1.0,
        extrato=[
            {'data': '01/12/2023', 'descricao': 'Transferência recebida', 'valor': 100.0},
            {'data': '05/12/2023', 'descricao': 'Compra', 'valor': -20.0},
            {'data': '10/12/2023', 'descricao': 'Depósito', 'valor': 50.0},
            {'data': '15/12/2023', 'descricao': 'Pagamento de conta', 'valor': -30.0},
            {'data': '20/12/2023', 'descricao': 'Transferência enviada', 'valor': -50.0},
        ],
        titular="Maria da Silva"
    ),
    ContaBancaria(
        id=3,
        tipo="corrente",
        saldo=500.0,
        extrato=[
            {'data': '01/12/2023', 'descricao': 'Compra', 'valor': 100.0},
            {'data': '05/12/2023', 'descricao': 'Depósito', 'valor': 300.0},
            {'data': '10/12/2023', 'descricao': 'Pagamento de conta', 'valor': -200.0},
            {'data': '15/12/2023', 'descricao': 'Transferência enviada', 'valor': -100.0},
            {'data': '20/12/2023', 'descricao': 'Depósito', 'valor': 200.0},
        ],
        titular="Pedro Santos"
    ),
    ContaBancaria(
        id=4,
        tipo="poupanca",
        saldo=2000.0,
        extrato=[
            {'data': '01/12/2023', 'descricao': 'Transferência recebida', 'valor': 500.0},
            {'data': '05/12/2023', 'descricao': 'Compra', 'valor': -100.0},
            {'data': '10/12/2023', 'descricao': 'Depósito', 'valor': 1000.0},
            {'data': '15/12/2023', 'descricao': 'Pagamento de conta', 'valor': -300.0},
            {'data': '20/12/2023', 'descricao': 'Transferência enviada', 'valor': -200.0},
        ],
        titular="Ana Oliveira"
    ),
    # outras contas
    
]

# Rotas
@app.route('/saldo/<int:num_conta>', methods=['GET'])
def consultar_saldo(num_conta):
    for conta in contas:
        if conta.id_conta == num_conta:
            return jsonify({'saldo': conta.saldo})
    
    return jsonify({'mensagem': 'Conta não encontrada'}), 404


@app.route('/extrato/<int:num_conta>', methods=['GET'])
def consultar_extrato(num_conta):
    for conta in contas:
        if conta.id_conta == num_conta:
            return jsonify({'extrato': conta.extrato})
    
    return jsonify({'mensagem': 'Conta não encontrada'}), 404


@app.route('/transferencia', methods=['POST'])
def transferir_entre_contas():
    data = request.json
    conta_origem_id = data.get('conta_origem')
    conta_destino_id = data.get('conta_destino')
    valor_transferencia = data.get('valor')

    # Verifica se as contas existem
    conta_origem = None
    conta_destino = None

    for conta in contas:
        if conta.id_conta == conta_origem_id:
            conta_origem = conta
        elif conta.id_conta == conta_destino_id:
            conta_destino = conta

    if conta_origem is None or conta_destino is None:
        return jsonify({'mensagem': 'Contas inválidas'}), 400

    # Verifica se as contas pertencem ao mesmo titular
    if conta_origem.titular != conta_destino.titular:
        return jsonify({'mensagem': 'As contas não pertencem ao mesmo titular'}), 400

    # Realiza a transferência
    if valor_transferencia <= conta_origem.saldo:
        conta_origem.saldo -= valor_transferencia
        conta_destino.saldo += valor_transferencia
        return jsonify({'mensagem': 'Transferência realizada com sucesso'})
    else:
        return jsonify({'mensagem': 'Saldo insuficiente para realizar a transferência'}), 400
    

# Rota para a documentação do Swagger
@app.route('/swagger', methods=['GET'])
def swagger_ui():
    
    swagger_url = '/static/swagger.json'
    swagger_blueprint = get_swaggerui_blueprint(swagger_url, '/static/', config={'app_name': "CondoConta API"})
    return render_template('swagger_ui.html', swagger_blueprint=swagger_blueprint)

# Rota para o arquivo Swagger JSON
@app.route('/static/swagger.json', methods=['GET'])
def swagger_json():
    swagger_info = {
        "openapi": "3.0.0",
        "info": {
            "title": "CondoConta API",
            "description": "Documentação da API CondoConta",
            "version": "1.0"
        },
        "paths": {
            "/saldo": {
                "get": {
                    "summary": "Consulta de saldo",
                    "description": "Endpoint para consultar o saldo das contas corrente e poupança.",
                    "responses": {
                        "200": {
                            "description": "Saldo consultado com sucesso",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "saldo_corrente": 1000.0,
                                        "saldo_poupanca": 1.0
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/extrato": {
                "get": {
                    "summary": "Consulta de extrato",
                    "description": "Endpoint para consultar o extrato bancário.",
                    "responses": {
                        "200": {
                            "description": "Extrato consultado com sucesso",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "extrato": [
                                            {"data": "01/12/2023", "descricao": "Compra", "valor": 50.0},
                                            {"data": "05/12/2023", "descricao": "Depósito", "valor": 200.0}
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/transferencia": {
                "post": {
                    "summary": "Realizar transferência entre contas",
                    "description": "Endpoint para realizar transferência entre contas corrente e poupança.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "conta_origem": {"type": "integer"},
                                        "conta_destino": {"type": "integer"},
                                        "valor": {"type": "number"}
                                    },
                                    "example": {
                                        "conta_origem": 1,
                                        "conta_destino": 2,
                                        "valor": 200.0
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Transferência realizada com sucesso",
                            "content": {
                                "application/json": {
                                    "example": {"mensagem": "Transferência realizada com sucesso"}
                                }
                            }
                        },
                        "400": {
                            "description": "Erro ao realizar transferência",
                            "content": {
                                "application/json": {
                                    "example": {"mensagem": "Saldo insuficiente para realizar a transferência"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(swagger_info)



if __name__ == '__main__':
    app.run(debug=True)
