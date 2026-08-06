# QA/tests/test_clientes_bdd.py
import pytest
import httpx
from pytest_bdd import scenarios, given, when, then, parsers

# URL base do nosso backend rodando localmente
BASE_URL = "http://127.0.0.1:8000/api/v1/clientes"

# Carrega os cenários do Gherkin na pasta QA/features
scenarios("../features/clientes.feature")

@pytest.fixture
def contexto():
    return {}

# =====================================================================
# DADO (GIVEN)
# =====================================================================
@given(parsers.parse('que eu tenho um novo cliente com ID "{id_cliente}" e nome "{nome}"'))
def novo_cliente_payload(contexto, id_cliente, nome):
    # Garanta que se o cliente já existir de testes anteriores, a gente limpe antes!
    httpx.delete(f"{BASE_URL}/{id_cliente}")
    
    contexto["payload"] = {
        "id_cliente": id_cliente,
        "nome_completo": nome,
        "nome_exibicao": nome.split()[0],
        "pronomes": "Ela/Dela",
        "identidade_genero": "Mulher Cisgênero",
        "autodescricao": "Cliente teste QA",
        "sexo_equacao": "Feminino",
        "data_nascimento": "1995-05-15",
        "telefone": "(81) 98888-0000",
        "email": "marina@email.com",
        "status": "Ativo"
    }

@given(parsers.parse('que já existe um cliente cadastrado com o ID "{id_cliente}"'))
def cadastrar_cliente_existente(contexto, id_cliente):
    payload = {
        "id_cliente": id_cliente,
        "nome_completo": "Marina Silva",
        "nome_exibicao": "Marina",
        "pronomes": "Ela/Dela",
        "identidade_genero": "Mulher Cisgênero",
        "autodescricao": "Cliente teste QA",
        "sexo_equacao": "Feminino",
        "data_nascimento": "1995-05-15",
        "telefone": "(81) 98888-0000",
        "email": "marina@email.com",
        "status": "Ativo"
    }
    contexto["payload"] = payload
    
    # Limpa se já existir e cria do zero
    httpx.delete(f"{BASE_URL}/{id_cliente}")
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code in [200, 400]

# =====================================================================
# QUANDO (WHEN)
# =====================================================================
@when("eu envio uma requisição para cadastrar o cliente")
def requisicao_cadastro(contexto):
    contexto["resposta"] = httpx.post(BASE_URL, json=contexto["payload"])

@when(parsers.parse('eu consulto as informações do cliente "{id_cliente}"'))
def consulta_cliente(contexto, id_cliente):
    contexto["resposta"] = httpx.get(f"{BASE_URL}/{id_cliente}")

@when(parsers.parse('eu atualizo o telefone do cliente "{id_cliente}" para "{novo_telefone}"'))
def atualiza_telefone(contexto, id_cliente, novo_telefone):
    payload_atualizacao = {"telefone": novo_telefone}
    contexto["resposta"] = httpx.put(f"{BASE_URL}/{id_cliente}", json=payload_atualizacao)

@when(parsers.parse('eu solicito a remoção do cliente "{id_cliente}"'))
def deletar_cliente(contexto, id_cliente):
    contexto["resposta"] = httpx.delete(f"{BASE_URL}/{id_cliente}")

# =====================================================================
# ENTÃO (THEN)
# =====================================================================
@then(parsers.parse('o sistema deve retornar o status de sucesso {status:d}'))
def valida_status_sucesso(contexto, status):
    print("\n--- QUEM RESPONDEU? ---")
    print("Headers:", contexto["resposta"].headers)
    print("Conteúdo:", contexto["resposta"].text[:100])

    assert contexto["resposta"].status_code == status

@then(parsers.parse('o sistema deve retornar o status de erro {status:d} com a mensagem "{mensagem}"'))
def valida_status_erro(contexto, status, mensagem):
    resposta = contexto["resposta"]
    assert resposta.status_code == status
    assert resposta.json()["detail"] == mensagem

@then(parsers.parse('o cliente "{id_cliente}" deve estar salvo com o nome "{nome}"'))
def valida_dados_salvos(id_cliente, nome):
    resposta = httpx.get(f"{BASE_URL}/{id_cliente}")
    assert resposta.status_code == 200
    assert resposta.json()["nome_completo"] == nome

@then(parsers.parse('os dados do cliente devem conter o email "{email}"'))
def valida_email_consultado(contexto, email):
    assert contexto["resposta"].json()["email"] == email

@then(parsers.parse('a consulta ao cliente "{id_cliente}" deve exibir o telefone "{telefone}"'))
def valida_telefone_atualizado(id_cliente, telefone):
    resposta = httpx.get(f"{BASE_URL}/{id_cliente}")
    assert resposta.json()["telefone"] == telefone

@then(parsers.parse('a consulta ao cliente "{id_cliente}" deve retornar status de erro {status:d}'))
def valida_cliente_removido(id_cliente, status):
    resposta = httpx.get(f"{BASE_URL}/{id_cliente}")
    assert resposta.status_code == status