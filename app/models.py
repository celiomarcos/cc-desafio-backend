class ContaBancaria:
    def __init__(self, id, tipo, saldo, extrato=[], titular=None):
        self.id_conta = id
        self.tipo = tipo
        self.saldo = saldo
        self.extrato = extrato
        self.titular = titular

    def debitar(self, valor):
        self.saldo -= valor

    def creditar(self, valor):
        self.saldo += valor

class TransacaoContas:
    def __init__(self, data, descricao, valor, conta_origem, conta_destino):
        self.data = data
        self.descricao = descricao
        self.valor = valor
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino