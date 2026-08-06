# QA/tests/test_avaliacoes_bdd.py
import pytest
import httpx
from pytest_bdd import scenarios, given, when, then, parsers

# Certifique-se de usar a mesma porta em que seu FastAPI está rodando
BASE_URL_CLIENTES = "http://127.0.0.1:8000/api/v1/clientes"
BASE_URL_ANAMNESES = "http://127.0.0.1:8000/api/v1/anamneses"
BASE_URL_AVALIACOES = "http://127.0.0.1:8000/api/v1/avaliacoes"

scenarios("../features/avaliacoes.feature")

@pytest.fixture
def contexto():
    return {}

# =====================================================================
# DADO (GIVEN)
# =====================================================================
@given(parsers.parse('que existe um cliente cadastrado com ID "{id_cliente}" e nome "{nome}"'))
def garantir_cliente(id_cliente, nome):
    httpx.delete(f"{BASE_URL_CLIENTES}/{id_cliente}")
    payload = {
        "id_cliente": id_cliente,
        "nome_completo": nome,
        "nome_exibicao": nome.split()[0],
        "pronomes": "Ela/Dela",
        "identidade_genero": "Mulher Cisgênero",
        "autodescricao": "Cliente QA Avaliações",
        "sexo_equacao": "Feminino",
        "data_nascimento": "1995-05-15",
        "telefone": "(81) 98888-0000",
        "email": f"{id_cliente.lower()}@saf.com",
        "status": "Ativo"
    }
    httpx.post(BASE_URL_CLIENTES, json=payload)

@given(parsers.parse('que não existe nenhum cliente cadastrado com o ID "{id_cliente}"'))
def garantir_cliente_inexistente(id_cliente):
    httpx.delete(f"{BASE_URL_CLIENTES}/{id_cliente}")

@given(parsers.parse('que já existe uma anamnese cadastrada com o ID "{id_anamnese}" para o cliente "{id_cliente}"'))
def garantir_anamnese(id_anamnese, id_cliente):
    httpx.delete(f"{BASE_URL_ANAMNESES}/{id_anamnese}")
    payload = {
        "id_anamnese": id_anamnese,
        "id_cliente": id_cliente,
        "data_anamnese": "2026-08-06",
        "tipo_anamnese": "Inicial",
        "respondente": "Cliente",
        "profissional_responsavel": "Profissional QA",
        "objetivo_relatado": "Condicionamento físico",
        "atividade_fisica_atual": "Irregular",
        "status_anamnese": "Completa",
        "auditoria_realizada": "Sim"
    }
    httpx.post(BASE_URL_ANAMNESES, json=payload)

@given(parsers.parse('que eu preparo uma nova avaliação com ID "{id_avaliacao}" para o cliente "{id_cliente}" e anamnese "{id_anamnese}"'))
def preparar_avaliacao(contexto, id_avaliacao, id_cliente, id_anamnese):
    httpx.delete(f"{BASE_URL_AVALIACOES}/{id_avaliacao}")
    contexto["payload_avaliacao"] = {
        "id_avaliacao": id_avaliacao,
        "id_cliente": id_cliente,
        "id_anamnese": id_anamnese,
        "data_avaliacao": "2026-08-06",
        "profissional_responsavel": "Profissional QA",
        "status_avaliacao": "Em Andamento",
        "observacoes_gerais": "Avaliação inicial de teste BDD"
    }

@given(parsers.parse('que já existe uma avaliação cadastrada com o ID "{id_avaliacao}" para o cliente "{id_cliente}" e anamnese "{id_anamnese}"'))
def garantir_avaliacao_cadastrada(contexto, id_avaliacao, id_cliente, id_anamnese):
    httpx.delete(f"{BASE_URL_AVALIACOES}/{id_avaliacao}")
    payload = {
        "id_avaliacao": id_avaliacao,
        "id_cliente": id_cliente,
        "id_anamnese": id_anamnese,
        "data_avaliacao": "2026-08-06",
        "profissional_responsavel": "Profissional QA",
        "status_avaliacao": "Em Andamento",
        "observacoes_gerais": "Avaliação existente"
    }
    contexto["payload_avaliacao"] = payload
    response = httpx.post(BASE_URL_AVALIACOES, json=payload)
    assert response.status_code in [200, 201]

# =====================================================================
# QUANDO (WHEN)
# =====================================================================
@when("eu envio uma requisição para cadastrar a avaliação física")
def enviar_cadastro(contexto):
    contexto["resposta"] = httpx.post(BASE_URL_AVALIACOES, json=contexto["payload_avaliacao"])

@when(parsers.parse('eu atualizo o status da avaliação "{id_avaliacao}" para "{status_aval}" e observacao "{obs}"'))
def atualizar_avaliacao(contexto, id_avaliacao, status_aval, obs):
    payload = {
        "status_avaliacao": status_aval,
        "observacoes_gerais": obs
    }
    contexto["resposta"] = httpx.put(f"{BASE_URL_AVALIACOES}/{id_avaliacao}", json=payload)

@when(parsers.parse('eu solicito a remoção do cliente "{id_cliente}"'))
def remover_cliente(contexto, id_cliente):
    contexto["resposta_remocao"] = httpx.delete(f"{BASE_URL_CLIENTES}/{id_cliente}")

# =====================================================================
# ENTÃO (THEN)
# =====================================================================
@then(parsers.parse('o sistema deve retornar o status de sucesso {status:d}'))
def validar_status(contexto, status):
    assert contexto["resposta"].status_code == status

@then(parsers.parse('o sistema deve retornar o status de sucesso {status:d} para a remoção'))
def validar_status_remocao(contexto, status):
    assert contexto["resposta_remocao"].status_code == status

@then(parsers.parse('o sistema deve retornar o status de erro {status:d} com a mensagem contendo "{trecho}"'))
def validar_erro_parcial(contexto, status, trecho):
    resposta = contexto["resposta"]
    assert resposta.status_code == status
    assert trecho.lower() in resposta.json()["detail"].lower()

@then(parsers.parse('a consulta à avaliação "{id_avaliacao}" deve exibir o status de avaliação "{status_esperado}"'))
def validar_status_avaliacao_no_banco(id_avaliacao, status_esperado):
    res = httpx.get(f"{BASE_URL_AVALIACOES}/{id_avaliacao}")
    assert res.status_code == 200
    assert res.json()["status_avaliacao"] == status_esperado

@then(parsers.parse('a consulta à avaliação "{id_avaliacao}" deve retornar status de erro {status:d}'))
def validar_avaliacao_nao_encontrada(id_avaliacao, status):
    res = httpx.get(f"{BASE_URL_AVALIACOES}/{id_avaliacao}")
    assert res.status_code == status