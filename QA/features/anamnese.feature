Feature: Gestão de Anamneses(tbAnamneses)
    Como administrado da plataforma SAF
    Quero gerenciar o cadastro de clientes na base de dados 
    para realizar avaliações físicas e manter o historico atualizado

Scenario: Cadastrar uma nova Anamneses com sucesso
    Dado que eu tenho um cliente com ID "CL0001"
    Quando eu envio uma requisição para cadastrar uma Anamnese
    Então o sistema deve retornar o status de sucesso 200

    
