def calcular_imc(peso: float, altura: float) -> float:
    """
    Motor matemático para cálculo do Índice de Massa Corporal.
    """
    imc = peso / (altura ** 2)
    return round(imc, 2)

