# backend/services/calculadora_fisica.py
import uuid
from sqlalchemy.orm import Session
import models

def processar_calculos_automaticos(db: Session, id_avaliacao: str):
    """
    Varre as medidas da avaliação no formato longo, executa fórmulas biológicas
    e salva ou atualiza automaticamente as medidas calculadas na tbMedidas.
    """
    # 1. Busca todas as medidas cadastradas para esta avaliação
    medidas_da_sessao = db.query(models.Medida).filter(
        models.Medida.id_avaliacao == id_avaliacao
    ).all()

    # Cria um dicionário prático para leitura rápida: {"PESO": 72.5, "ALTURA": 178.0, ...}
    valores_brutos = {m.id_variavel: m.valor_revisado for m in medidas_da_sessao}

    # =========================================================================
    # CÁLCULO 1: ÍNDICE DE MASSA CORPORAL (IMC)
    # Fórmula: Peso (kg) / [Altura (m)]^2
    # =========================================================================
    if "PESO" in valores_brutos and "ALTURA" in valores_brutos:
        peso = valores_brutos["PESO"]
        altura_cm = valores_brutos["ALTURA"]

        # Evita divisão por zero caso digitem altura errada
        if altura_cm > 0:
            altura_m = altura_cm / 100.0
            imc_calculado = round(peso / (altura_m ** 2), 2)

            # Verifica se já existe um IMC calculado nessa avaliação para atualizar ou criar
            medida_imc = db.query(models.Medida).filter_by(
                id_avaliacao=id_avaliacao,
                id_variavel="IMC"
            ).first()

            if medida_imc:
                # Se já existia, só atualiza o valor caso o peso ou altura tenham sido editados
                medida_imc.valor_revisado = imc_calculado
            else:
                # Se não existia, gera uma ID curta e cadastra a nova medida longo
                id_gerado = f"CALC-{uuid.uuid4().hex[:6].upper()}"
                novo_imc = models.Medida(
                    id_medida=id_gerado,
                    id_avaliacao=id_avaliacao,
                    id_variavel="IMC",
                    valor_revisado=imc_calculado,
                    unidade="kg/m2",
                    origem="Calculado",
                    qualidade="Aprovado"
                )
                db.add(novo_imc)

            db.commit()

    # =========================================================================
    # CÁLCULO 2 (EXEMPLO FUTURO): GORDURA CORPORAL OU VO2 MAX
    # Aqui você poderá plugar as fórmulas de Jackson & Pollock e Teste de Cooper!
    # =========================================================================