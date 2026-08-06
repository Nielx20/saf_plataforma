# backend/seed.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

def popular_banco_saf(db: Session):
    print("🌱 Iniciando o seed dos catálogos e domínios do SAF...")

    # =========================================================================
    # POPULAR CLIENTE(tbClientes)
    # =========================================================================
    clientes_data = [
        {
            "id_cliente": "CL0001",
            "nome_completo": "Adeilson Fárias da Silva",
            "nome_exibicao": "Adeilson",
            "pronomes": "ele/dele",
            "identidade_genero": "Homem",
            "autodescricao": "",
            "sexo_equacao": "Masculino",
            "data_nascimento": "1998-04-15",
            "telefone": "(00)90000-0001",
            "email": "adeilson.teste@example.com",
            "status": "Ativo"
        },
        {
             "id_cliente": "CL0002",
             "nome_completo": "Janiel Nícacio",
             "nome_exibicao": "Janiel",
             "pronomes": "ele/dele",
             "identidade_genero": "Homem",
             "autodescricao": "",
             "sexo_equacao": "Masculino",
             "data_nascimento": "1999-07-09",
             "telefone": "(81)90000-0001",
             "email": "janiel.teste@example.com",
             "status": "Ativo"
         }       
    ]

    for item in clientes_data:
        existe = db.query(models.Cliente).filter_by(id_cliente=item["id_cliente"]).first()
        if not existe:
            db.add(models.Cliente(**item))
    db.commit()
    print("✅ Clientes (tbClientes) sincronizados.")

    # =========================================================================
    # POPULAR ANAMNESES (tbAnamneses)
    # =========================================================================

    anamneses_data = [

        {
            "id_cliente": "CL0001",
            "data_anamnese": "2026-11-24",
            "tipo_anamnese": "Periódica",
            "id_anamnese_anterior": "",
            "respondente": "Cliente",
            "profissional_responsavel": "Adeilson da Silva Farias",
            "instrumento_aplicado": "Não",
            "nome_instrumento": "",
            "objetivo_relatado": "Hipertrofia muscular e ganho de força.",
            "expectativa_relatada": "Aumentar a intensidade dos treinos e melhorar a composição corporal.",
            "experiencia_previa_af": "Praticando musculação de forma contínua nos últimos 4 meses.",
            "atividade_fisica_atual": "Musculação e treinos cardiorrespiratórios estruturados.",
            "frequencia_relatada": "3 a 4 vezes por semana",
            "duracao_sessao_min": 60,
            "observacoes_rotina": "Rotina de trabalho ainda sentada, mas realiza pausas ativas a cada 2 horas.",
            "condicao_saude": "Não",
            "detalhe_condicoes": "",
            "uso_medicamentos": "Não",
            "detalhe_medicamentos": "",
            "lesao_cirurgia": "Não",
            "detalhe_lesao": "",
            "dor_atual": "Não",
            "local_dor": "",
            "intensidade_dor": 0,
            "restricao_recomendacao": "Não",
            "detalhe_restricao": "",
            "documento_apresentado": "Não",
            "tabagismo": "Nunca fumou",
            "consumo_alcool": "Menos de 1 vez por semana",
            "horas_sono_noite": 7.5,
            "qualidade_sono": "Muito Boa",
            "estresse_percebido": 3,
            "modulo_crianca_adolescente": "Não",
            "detalhe_crianca_adolescente": "",
            "modulo_autonomia_funcional": "Não",
            "detalhe_autonomia": "",
            "modulo_gestacao": "Não",
            "detalhe_gestacao": "",
            "modulo_acessibilidade": "Não",
            "detalhe_acessibilidade": "",
            "modulo_performance": "Sim",
            "detalhe_performance": "Avaliação de carga máxima e progressão de volume de treino realizada.",
            "modulo_retorno_afastamento": "Não",
            "detalhe_retorno": "",
            "encaminhamento": "Não identificado no momento",
            "motivo_encaminhamento": "",
            "conduta_inicial": "Progressão de carga e ajuste no volume do treino de força",
            "detalhe_conduta": "Inserção de técnicas avançadas de hipertrofia nos membros inferiores.",
            "adaptacoes_previstas": "Ajuste na planilha se houver relato de fadiga excessiva.",
            "status_anamnese": "Completa",
            "data_arquivamento": "2026-11-26",
            "auditoria_realizada": "Sim",
            "observacoes_auditoria": "Reavaliação arquivada com sucesso e vinculada ao histórico anterior.",
            "id_anamnese": "AN0001"
        },
        {        
            "id_cliente": "CL0002",
            "data_anamnese": "2026-11-24",
            "tipo_anamnese": "Periódica",
            "id_anamnese_anterior": "",
            "respondente": "Cliente",
            "profissional_responsavel": "Janiel Nícacio da Silva",
            "instrumento_aplicado": "Não",
            "nome_instrumento": "",
            "objetivo_relatado": "Hipertrofia muscular e ganho de força.",
            "expectativa_relatada": "Aumentar a intensidade dos treinos e melhorar a composição corporal.",
            "experiencia_previa_af": "Praticando musculação de forma contínua nos últimos 4 meses.",
            "atividade_fisica_atual": "Musculação e treinos cardiorrespiratórios estruturados.",
            "frequencia_relatada": "3 a 4 vezes por semana",
            "duracao_sessao_min": 60,
            "observacoes_rotina": "Rotina de trabalho ainda sentada, mas realiza pausas ativas a cada 2 horas.",
            "condicao_saude": "Não",
            "detalhe_condicoes": "",
            "uso_medicamentos": "Não",
            "detalhe_medicamentos": "",
            "lesao_cirurgia": "Não",
            "detalhe_lesao": "",
            "dor_atual": "Não",
            "local_dor": "",
            "intensidade_dor": 0,
            "restricao_recomendacao": "Não",
            "detalhe_restricao": "",
            "documento_apresentado": "Não",
            "tabagismo": "Nunca fumou",
            "consumo_alcool": "Menos de 1 vez por semana",
            "horas_sono_noite": 7.5,
            "qualidade_sono": "Muito Boa",
            "estresse_percebido": 3,
            "modulo_crianca_adolescente": "Não",
            "detalhe_crianca_adolescente": "",
            "modulo_autonomia_funcional": "Não",
            "detalhe_autonomia": "",
            "modulo_gestacao": "Não",
            "detalhe_gestacao": "",
            "modulo_acessibilidade": "Não",
            "detalhe_acessibilidade": "",
            "modulo_performance": "Sim",
            "detalhe_performance": "Avaliação de carga máxima e progressão de volume de treino realizada.",
            "modulo_retorno_afastamento": "Não",
            "detalhe_retorno": "",
            "encaminhamento": "Não identificado no momento",
            "motivo_encaminhamento": "",
            "conduta_inicial": "Progressão de carga e ajuste no volume do treino de força",
            "detalhe_conduta": "Inserção de técnicas avançadas de hipertrofia nos membros inferiores.",
            "adaptacoes_previstas": "Ajuste na planilha se houver relato de fadiga excessiva.",
            "status_anamnese": "Completa",
            "data_arquivamento": "2026-11-26",
            "auditoria_realizada": "Sim",
            "observacoes_auditoria": "Reavaliação arquivada com sucesso e vinculada ao histórico anterior.",
            "id_anamnese": "AN0002"
        }     
    ]

    for item in anamneses_data:
        existe = db.query(models.Anamnese).filter_by(id_anamnese=item["id_anamnese"]).first()
        if not existe:
            db.add(models.Anamnese(**item))
    db.commit()
    print("✅ Anamneses (tbAnamneses) sincronizadas.")

    # =========================================================================
    # 1. POPULAR DOMÍNIOS DE AVALIAÇÃO (tbDominiosAvaliacao)
    # =========================================================================
    dominios_data = [
        {
            "id_dominio": "ANT",
            "nome_dominio": "Antropometria",
            "descricao": "Medidas de peso, altura, circunferências e diâmetros ósseos."
        },
        {
            "id_dominio": "CC",
            "nome_dominio": "Composição Corporal",
            "descricao": "Estimativas de gordura corporal, massa magra e densidade via dobras ou bioimpedância."
        },
        {
            "id_dominio": "CR",
            "nome_dominio": "Cardiorrespiratória",
            "descricao": "Aferição de capacidade aeróbia, VO2 Máximo e limiares de frequência cardíaca."
        },
        {
            "id_dominio": "FR",
            "nome_dominio": "Força e Resistência Muscular",
            "descricao": "Testes de força máxima, força de preensão e testes submáximos de repetição."
        }
    ]

    for item in dominios_data:
        existe = db.query(models.DominioAvaliacao).filter_by(id_dominio=item["id_dominio"]).first()
        if not existe:
            db.add(models.DominioAvaliacao(**item))
    db.commit()
    print("✅ Domínios (tbDominiosAvaliacao) sincronizados.")

    # =========================================================================
    # 2. POPULAR PROTOCOLOS CIENTÍFICOS (tbProtocolos)
    # =========================================================================
    protocolos_data = [
        {
            "id_protocolo": "ANT-GERAL",
            "id_dominio": "ANT",
            "nome_metodo": "Aferição Antropométrica Padrão ISAK",
            "publicacao_referencia": "ISAK Manual (2019)",
            "formula_aplicada": "Coleta direta de peso, estatura e envergadura."
        },
        {
            "id_protocolo": "CC-JP3",
            "id_dominio": "CC",
            "nome_metodo": "Jackson & Pollock (3 Dobras Cutâneas)",
            "publicacao_referencia": "Jackson, A.S., & Pollock, M.L. (1978 / 1980)",
            "formula_aplicada": "Densidade Corporal -> Equação de Siri (1956)"
        },
        {
            "id_protocolo": "CC-JP7",
            "id_dominio": "CC",
            "nome_metodo": "Jackson & Pollock (7 Dobras Cutâneas)",
            "publicacao_referencia": "Jackson, A.S., & Pollock, M.L. (1978 / 1980)",
            "formula_aplicada": "Densidade Corporal -> Equação de Siri (1956)"
        },
        {
            "id_protocolo": "CR-COOPER12",
            "id_dominio": "CR",
            "nome_metodo": "Teste de Cooper - Corrida/Caminhada de 12 Minutos",
            "publicacao_referencia": "Cooper, K.H. (1968)",
            "formula_aplicada": "VO2 Max = (Distância metros - 504.9) / 44.73"
        }
    ]

    for item in protocolos_data:
        existe = db.query(models.Protocolo).filter_by(id_protocolo=item["id_protocolo"]).first()
        if not existe:
            db.add(models.Protocolo(**item))
    db.commit()
    print("✅ Protocolos (tbProtocolos) sincronizados.")

    # =========================================================================
    # 3. POPULAR CATÁLOGO DE VARIÁVEIS / MEDIDAS (tbCatalogoMedidas)
    # =========================================================================
    variaveis_data = [
        # --- Medidas Antropométricas Brutas ---
        {
            "id_variavel": "PESO",
            "id_protocolo": "ANT-GERAL",
            "nome_variavel": "Massa Corporal Total",
            "unidade_medida": "kg",
            "tipo_medida": "Bruta",
            "valor_minimo": 20.0,
            "valor_maximo": 300.0
        },
        {
            "id_variavel": "ALTURA",
            "id_protocolo": "ANT-GERAL",
            "nome_variavel": "Estatura (Altura)",
            "unidade_medida": "cm",
            "tipo_medida": "Bruta",
            "valor_minimo": 50.0,
            "valor_maximo": 250.0
        },
        {
            "id_variavel": "CIRC_CINTURA",
            "id_protocolo": "ANT-GERAL",
            "nome_variavel": "Circunferência da Cintura",
            "unidade_medida": "cm",
            "tipo_medida": "Bruta",
            "valor_minimo": 30.0,
            "valor_maximo": 200.0
        },
        # --- Dobras Cutâneas (mm) ---
        {
            "id_variavel": "DC_TRICEPS",
            "id_protocolo": "CC-JP7",
            "nome_variavel": "Dobra Cutânea - Tríceps",
            "unidade_medida": "mm",
            "tipo_medida": "Bruta",
            "valor_minimo": 2.0,
            "valor_maximo": 80.0
        },
        {
            "id_variavel": "DC_SUBESCAPULAR",
            "id_protocolo": "CC-JP7",
            "nome_variavel": "Dobra Cutânea - Subescapular",
            "unidade_medida": "mm",
            "tipo_medida": "Bruta",
            "valor_minimo": 2.0,
            "valor_maximo": 80.0
        },
        {
            "id_variavel": "DC_ABDOMINAL",
            "id_protocolo": "CC-JP7",
            "nome_variavel": "Dobra Cutânea - Abdominal",
            "unidade_medida": "mm",
            "tipo_medida": "Bruta",
            "valor_minimo": 2.0,
            "valor_maximo": 90.0
        },
        # --- Variáveis Calculadas pelo Sistema ---
        {
            "id_variavel": "IMC",
            "id_protocolo": "ANT-GERAL",
            "nome_variavel": "Índice de Massa Corporal",
            "unidade_medida": "kg/m2",
            "tipo_medida": "Calculada",
            "valor_minimo": 10.0,
            "valor_maximo": 70.0
        },
        {
            "id_variavel": "GORDURA_PERC",
            "id_protocolo": "CC-JP7",
            "nome_variavel": "Percentual de Gordura Corporal",
            "unidade_medida": "%",
            "tipo_medida": "Calculada",
            "valor_minimo": 2.0,
            "valor_maximo": 60.0
        }
    ]

    for item in variaveis_data:
        existe = db.query(models.CatalogoMedida).filter_by(id_variavel=item["id_variavel"]).first()
        if not existe:
            db.add(models.CatalogoMedida(**item))
    db.commit()
    print("✅ Variáveis de Catálogo (tbCatalogoMedidas) sincronizadas.")
    print("🏁 Seed finalizado com sucesso!\n")

if __name__ == "__main__":
    # Garante que as tabelas existam antes de injetar os dados
    Base.metadata.create_all(bind=engine)
    
    sessao = SessionLocal()
    try:
        popular_banco_saf(sessao)
    finally:
        sessao.close()