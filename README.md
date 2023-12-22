# CondoConta BackEnd

Este projeto consiste em uma API para operações bancárias básicas.

## Configuração

Certifique-se de ter o Python 3.10 ou superior instalado.

### Clone este repositório:

```bash
git clone https://github.com/celiomarcos/cc-backend.git
cd cc-backend
```

### Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
# No Windows: venv\Scripts\activate
# No macOS e Linux: source venv/bin/activate
```

### Instale as dependências

```bash
pip install -r requirements.txt
```

### Configure Flask

```bash
export FLASK_APP=app.routes  # Linux/Mac
# or
set FLASK_APP=app.routes    # Windows (Command Prompt)
```

### Execute aplicação Flask

```bash
flask run
```

## Uso da API

### Consultar Saldo

Para consultar o saldo de uma conta específica, faça uma requisição GET para:

```bash
curl -X GET http://localhost:5000/saldo/<id_conta>
```

Substitua <id_conta> pelo número da conta desejada.

### Consultar Extrato

Para consultar o saldo de uma conta específica, faça uma requisição GET para:

```bash
curl -X GET http://localhost:5000/extrato/<id_conta>
```

Substitua <id_conta> pelo número da conta desejada.

### Realizar Transferência

Para realizar uma transferência entre contas, faça uma requisição POST contendo um JSON com os dados da transferência, por exemplo:

```bash
http://localhost:5000/transferencia -H "Content-Type: application/json"
-d '{
"conta_origem_id": 1,
"conta_destino_id": 2,
"valor": 100
}'
```

Substitua os valores de conta_origem, conta_destino e valor pelos dados da transferência desejada.

## Testes

Para executar os testes, utilize o seguinte comando:

```bash
python -m unittest tests.test_operations
```

## Autor

[Celio Marcos Moreira Santiago](mailto:celiomarcos@gmail.com)
