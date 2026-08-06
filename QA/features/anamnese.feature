Feature: Gestão de Anamneses (tbAnamneses)
  Como profissional da plataforma SAF
  Quero registrar e gerenciar anamneses dos clientes
  Para fundamentar a avaliação física e manter rastreabilidade longitudinal

  Scenario: Cadastrar uma nova anamnese com sucesso para um cliente existente
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que eu preparo uma nova anamnese com ID "AN0001" para o cliente "CL0001"
    Quando eu envio uma requisição para cadastrar a anamnese
    Então o sistema deve retornar o status de sucesso 201
    E a consulta à anamnese "AN0001" deve exibir o status de anamnese "Completa"

  Scenario: Impedir cadastro de anamnese para cliente inexistente
    Dado que não existe nenhum cliente cadastrado com o ID "CL9999"
    E que eu preparo uma nova anamnese com ID "AN0002" para o cliente "CL9999"
    Quando eu envio uma requisição para cadastrar a anamnese
    Então o sistema deve retornar o status de erro 400 com a mensagem contendo "não encontrado"

  Scenario: Impedir cadastro com ID de anamnese duplicado
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    Quando eu tento cadastrar novamente uma anamnese com o ID "AN0001" para o cliente "CL0001"
    Então o sistema deve retornar o status de erro 400 com a mensagem "ID Anamnese já cadastrado. IDs são únicos e não reutilizados."

  Scenario: Consultar uma anamnese por ID
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    Quando eu consulto as informações da anamnese "AN0001"
    Então o sistema deve retornar o status de sucesso 200
    E os dados da anamnese devem conter o objetivo relatado "Condicionamento físico"

  Scenario: Atualizar dados de uma anamnese existente
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    Quando eu atualizo as horas de sono da anamnese "AN0001" para "8.0" e qualidade para "Boa"
    Então o sistema deve retornar o status de sucesso 200
    E a consulta à anamnese "AN0001" deve exibir horas de sono "8.0" e qualidade "Boa"

  Scenario: Remover um cliente deve apagar sua anamnese em cascata
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    Quando eu solicito a remoção do cliente "CL0001"
    Então o sistema deve retornar o status de sucesso 204 para o cliente
    E a consulta à anamnese "AN0001" deve retornar status de erro 404