# QA/tests/test_anamnese_bdd.py
import pytest
import httpx
from pytest_bdd import scenarios, given, when, then, parsers

BASE_URL_CLIENTES = "http://127.0.0.1:8000/api/v1/clientes"
BASE_URL_ANAMNESES = "http://127.0.0.1:8000/api/v1/anamneses"

# Carrega os cenários do Gherkin
scenarios("../features/anamnese.feature")

@pytest.fixture
def contexto():
    return {}

# =====================================================================
# DADO (GIVEN)
# =====================================================================
@given(parsers.parse('que existe um cliente cadastrado com ID "{id_cliente}" e nome "{nome}"'))
def garantir_cliente_cadastrado(id_cliente, nome):
    # Limpa antes para garantir estado limpo
    httpx.delete(f"{BASE_URL_CLIENTES}/{id_cliente}")
    
    payload = {
        "id_cliente": id_cliente,
        "nome_completo": nome,
        "nome_exibicao": nome.split()[0],
        "pronomes": "Ela/Dela",
        "identidade_genero": "Mulher Cisgênero",
        "autodescricao": "Cliente QA Anamnese",
        "sexo_equacao": "Feminino",
        "data_nascimento": "1995-05-15",
        "telefone": "(81) 98888-0000",
        "email": f"{id_cliente.lower()}@saf.com",
        "status": "Ativo"
    }
    response = httpx.post(BASE_URL_CLIENTES, json=payload)
    assert response.status_code in [200, 201, 400]

@given(parsers.parse('que não existe nenhum cliente cadastrado com o ID "{id_cliente}"'))
def garantir_cliente_inexistente(id_cliente):
    httpx.delete(f"{BASE_URL_CLIENTES}/{id_cliente}")

@given(parsers.parse('que eu preparo uma nova anamnese com ID "{id_anamnese}" para o cliente "{id_cliente}"'))
def preparar_payload_anamnese(contexto, id_anamnese, id_cliente):
    # Garante que essa anamnese não exista antes do teste
    httpx.delete(f"{BASE_URL_ANAMNESES}/{id_anamnese}")

    contexto["payload_anamnese"] = {
        "id_anamnese": id_anamnese,
        "id_cliente": id_cliente,
        "data_anamnese": "2026-08-04",
        "tipo_anamnese": "Inicial",
        "respondente": "Cliente",
        "profissional_responsavel": "Profissional QA",
        "instrumento_aplicado": "Sim",
        "nome_instrumento": "PAR-Q+",
        "objetivo_relatado": "Condicionamento físico",
        "atividade_fisica_atual": "Irregular",
        "condicao_saude": "Não",
        "uso_medicamentos": "Não",
        "lesao_cirurgia": "Não",
        "dor_atual": "Não",
        "restricao_recomendacao": "Não",
        "documento_apresentado": "Não",
        "tabagismo": "Nunca fumou",
        "consumo_alcool": "Não consome",
        "horas_sono_noite": 7.0,
        "qualidade_sono": "Regular",
        "estresse_percebido": 4,
        "modulo_crianca_adolescente": "Não",
        "modulo_autonomia_funcional": "Não",
        "modulo_gestacao": "Não",
        "modulo_acessibilidade": "Não",
        "modulo_performance": "Não",
        "modulo_retorno_afastamento": "Não",
        "encaminhamento": "Não identificado no momento",
        "conduta_inicial": "Prosseguir",
        "status_anamnese": "Completa",
        "auditoria_realizada": "Sim",
        "observacoes_auditoria": "Anamnese completa de teste QA"
    }

@given(parsers.parse('que já existe uma anamnese cadastrada com o ID "{id_anamnese}" para o cliente "{id_cliente}"'))
def garantir_anamnese_cadastrada(contexto, id_anamnese, id_cliente):
    httpx.delete(f"{BASE_URL_ANAMNESES}/{id_anamnese}")
    
    payload = {
        "id_anamnese": id_anamnese,
        "id_cliente": id_cliente,
        "data_anamnese": "2026-08-04",
        "tipo_anamnese": "Inicial",
        "respondente": "Cliente",
        "profissional_responsavel": "Profissional QA",
        "objetivo_relatado": "Condicionamento físico",
        "atividade_fisica_atual": "Irregular",
        "status_anamnese": "Completa",
        "auditoria_realizada": "Sim"
    }
    contexto["payload_anamnese"] = payload
    response = httpx.post(BASE_URL_ANAMNESES, json=payload)
    assert response.status_code in [200, 201]

# =====================================================================
# QUANDO (WHEN)
# =====================================================================
@when("eu envio uma requisição para cadastrar a anamnese")
def enviar_cadastro_anamnese(contexto):
    contexto["resposta"] = httpx.post(BASE_URL_ANAMNESES, json=contexto["payload_anamnese"])

@when(parsers.parse('eu tento cadastrar novamente uma anamnese com o ID "{id_anamnese}" para o cliente "{id_cliente}"'))
def tentar_cadastrar_duplicado(contexto, id_anamnese, id_cliente):
    contexto["resposta"] = httpx.post(BASE_URL_ANAMNESES, json=contexto["payload_anamnese"])

@when(parsers.parse('eu consulto as informações da anamnese "{id_anamnese}"'))
def consultar_anamnese(contexto, id_anamnese):
    contexto["resposta"] = httpx.get(f"{BASE_URL_ANAMNESES}/{id_anamnese}")

@when(parsers.parse('eu atualizo as horas de sono da anamnese "{id_anamnese}" para "{horas}" e qualidade para "{qualidade}"'))
def atualizar_anamnese(contexto, id_anamnese, horas, qualidade):
    payload_atualizacao = {
        "horas_sono_noite": float(horas),
        "qualidade_sono": qualidade
    }
    contexto["resposta"] = httpx.put(f"{BASE_URL_ANAMNESES}/{id_anamnese}", json=payload_atualizacao)

@when(parsers.parse('eu solicito a remoção do cliente "{id_cliente}"'))
def remover_cliente(contexto, id_cliente):
    contexto["resposta_remocao_cliente"] = httpx.delete(f"{BASE_URL_CLIENTES}/{id_cliente}")

# =====================================================================
# ENTÃO (THEN)
# =====================================================================
@then(parsers.parse('o sistema deve retornar o status de sucesso {status:d}'))
def validar_status_sucesso(contexto, status):
    print("\n--- QUEM RESPONDEU? ---")
    print("Headers:", contexto["resposta"].headers)
    print("Conteúdo:", contexto["resposta"].text[:100])
    assert contexto["resposta"].status_code == status

@then(parsers.parse('o sistema deve retornar o status de sucesso {status:d} para o cliente'))
def validar_status_remocao_cliente(contexto, status):
    assert contexto["resposta_remocao_cliente"].status_code == status

@then(parsers.parse('o sistema deve retornar o status de erro {status:d} com a mensagem "{mensagem}"'))
def validar_status_erro_exato(contexto, status, mensagem):
    resposta = contexto["resposta"]
    assert resposta.status_code == status
    assert resposta.json()["detail"] == mensagem

@then(parsers.parse('o sistema deve retornar o status de erro {status:d} com a mensagem contendo "{trecho_mensagem}"'))
def validar_status_erro_parcial(contexto, status, trecho_mensagem):
    resposta = contexto["resposta"]
    assert resposta.status_code == status
    assert trecho_mensagem.lower() in resposta.json()["detail"].lower()

@then(parsers.parse('a consulta à anamnese "{id_anamnese}" deve exibir o status de anamnese "{status_esperado}"'))
def validar_status_anamnese_salvo(id_anamnese, status_esperado):
    resposta = httpx.get(f"{BASE_URL_ANAMNESES}/{id_anamnese}")
    assert resposta.status_code == 200
    assert resposta.json()["status_anamnese"] == status_esperado

@then(parsers.parse('os dados da anamnese devem conter o objetivo relatado "{objetivo}"'))
def validar_objetivo_anamnese(contexto, objetivo):
    assert contexto["resposta"].json()["objetivo_relatado"] == objetivo

@then(parsers.parse('a consulta à anamnese "{id_anamnese}" deve exibir horas de sono "{horas}" e qualidade "{qualidade}"'))
def validar_sono_atualizado(id_anamnese, horas, qualidade):
    resposta = httpx.get(f"{BASE_URL_ANAMNESES}/{id_anamnese}")
    assert resposta.status_code == 200
    assert float(resposta.json()["horas_sono_noite"]) == float(horas)
    assert resposta.json()["qualidade_sono"] == qualidade

@then(parsers.parse('a consulta à anamnese "{id_anamnese}" deve retornar status de erro {status:d}'))
def validar_anamnese_removida_cascata(id_anamnese, status):
    resposta = httpx.get(f"{BASE_URL_ANAMNESES}/{id_anamnese}")
    assert resposta.status_code == status