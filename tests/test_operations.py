import unittest
from app.routes import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_consultar_saldo(self):
        response = self.app.get('/saldo/1')  # Consultar saldo da conta 1
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('saldo', data)

    def test_consultar_extrato(self):
        response = self.app.get('/extrato/1')  # Consultar extrato da conta 1
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('extrato', data)

    def test_transferencia_entre_contas_sucesso(self):
        dados_transferencia = {
            'conta_origem': 1,  # ID da conta origem
            'conta_destino': 2,  # ID da conta destino
            'valor': 200.0
        }
        response = self.app.post('/transferencia', json=dados_transferencia)
        self.assertEqual(response.status_code, 200)
        # Verifica se a transferência foi bem-sucedida

    def test_transferencia_entre_contas_titularidade_diferente(self):
            dados_transferencia = {
                'conta_origem': 1,  # ID da conta origem
                'conta_destino': 3,  # ID da conta destino com titularidade diferente
                'valor': 100.0
            }
            response = self.app.post('/transferencia', json=dados_transferencia)
            self.assertEqual(response.status_code, 400)
            # Verifica se a transferência foi recusada devido a titularidade diferente

    def test_transferencia_entre_contas_saldo_insuficiente(self):
        dados_transferencia = {
            'conta_origem': 1,  # ID da conta origem
            'conta_destino': 2,  # ID da conta destino
            'valor': 1500.0  # Valor maior que o saldo disponível
        }
        response = self.app.post('/transferencia', json=dados_transferencia)
        self.assertEqual(response.status_code, 400)
        # Verifica se a transferência foi recusada devido a saldo insuficiente

    def test_transferencia_entre_contas_invalidas(self):
        dados_transferencia = {
            'conta_origem': 1,  # ID da conta origem inválida
            'conta_destino': 7,  # ID da conta destino inválida
            'valor': 100.0
        }
        response = self.app.post('/transferencia', json=dados_transferencia)
        self.assertEqual(response.status_code, 400)
        # Verifica se a transferência foi recusada devido a contas inválidas

if __name__ == '__main__':
    unittest.main()
