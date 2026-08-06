Feature: Gestão de Avaliações Físicas (tbAvaliacoes)
  Como profissional da plataforma SAF
  Quero registrar e gerenciar cabeçalhos de sessões de avaliação física
  Para vincular anamneses vigentes e permitir a coleta de medidas no sistema

  Scenario: Cadastrar uma avaliação física com sucesso
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    E que eu preparo uma nova avaliação com ID "AV0001" para o cliente "CL0001" e anamnese "AN0001"
    Quando eu envio uma requisição para cadastrar a avaliação física
    Então o sistema deve retornar o status de sucesso 201
    E a consulta à avaliação "AV0001" deve exibir o status de avaliação "Em Andamento"

  Scenario: Impedir cadastro de avaliação para cliente inexistente
    Dado que não existe nenhum cliente cadastrado com o ID "CL9999"
    E que eu preparo uma nova avaliação com ID "AV0002" para o cliente "CL9999" e anamnese "AN0001"
    Quando eu envio uma requisição para cadastrar a avaliação física
    Então o sistema deve retornar o status de erro 400 com a mensagem contendo "não encontrado"

  Scenario: Impedir cadastro de avaliação para anamnese inexistente
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que eu preparo uma nova avaliação com ID "AV0003" para o cliente "CL0001" e anamnese "AN9999"
    Quando eu envio uma requisição para cadastrar a avaliação física
    Então o sistema deve retornar o status de erro 400 com a mensagem contendo "não encontrada"

  Scenario: Impedir vincular anamnese de outro cliente na avaliação
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que existe um cliente cadastrado com ID "CL0002" e nome "Carlos Souza"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    E que eu preparo uma nova avaliação com ID "AV0004" para o cliente "CL0002" e anamnese "AN0001"
    Quando eu envio uma requisição para cadastrar a avaliação física
    Então o sistema deve retornar o status de erro 400 com a mensagem contendo "pertence a outro cliente"

  Scenario: Atualizar o status e observações de uma avaliação
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    E que já existe uma avaliação cadastrada com o ID "AV0001" para o cliente "CL0001" e anamnese "AN0001"
    Quando eu atualizo o status da avaliação "AV0001" para "Concluida" e observacao "Coleta finalizada"
    Então o sistema deve retornar o status de sucesso 200
    E a consulta à avaliação "AV0001" deve exibir o status de avaliação "Concluida"

  Scenario: Remover um cliente deve apagar suas avaliações físicas em cascata
    Dado que existe um cliente cadastrado com ID "CL0001" e nome "Marina Silva"
    E que já existe uma anamnese cadastrada com o ID "AN0001" para o cliente "CL0001"
    E que já existe uma avaliação cadastrada com o ID "AV0001" para o cliente "CL0001" e anamnese "AN0001"
    Quando eu solicito a remoção do cliente "CL0001"
    Então o sistema deve retornar o status de sucesso 204 para a remoção
    E a consulta à avaliação "AV0001" deve retornar status de erro 404