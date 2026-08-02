Feature: Gestão de Clientes (tbClientes)
  Como administrador da plataforma SAF
  Quero gerenciar o cadastro de clientes na base de dados
  Para realizar avaliações físicas e manter o histórico atualizado

  Scenario: Cadastrar um novo cliente com sucesso
    Dado que eu tenho um novo cliente com ID "CL0001" e nome "Marina Silva"
    Quando eu envio uma requisição para cadastrar o cliente
    Então o sistema deve retornar o status de sucesso 200
    E o cliente "CL0001" deve estar salvo com o nome "Marina Silva"

  Scenario: Impedir cadastro com ID duplicado
    Dado que já existe um cliente cadastrado com o ID "CL0001"
    Quando eu envio uma requisição para cadastrar o cliente
    Então o sistema deve retornar o status de erro 400 com a mensagem "ID Cliente já cadastrado. IDs são únicos e não reutilizados."

  Scenario: Consultar um cliente por ID
    Dado que já existe um cliente cadastrado com o ID "CL0001"
    Quando eu consulto as informações do cliente "CL0001"
    Então o sistema deve retornar o status de sucesso 200
    E os dados do cliente devem conter o email "marina@email.com"

  Scenario: Atualizar o telefone de um cliente existente
    Dado que já existe um cliente cadastrado com o ID "CL0001"
    Quando eu atualizo o telefone do cliente "CL0001" para "(81) 99999-9999"
    Então o sistema deve retornar o status de sucesso 200
    E a consulta ao cliente "CL0001" deve exibir o telefone "(81) 99999-9999"

  Scenario: Remover um cliente do banco de dados
    Dado que já existe um cliente cadastrado com o ID "CL0001"
    Quando eu solicito a remoção do cliente "CL0001"
    Então o sistema deve retornar o status de sucesso 204
    E a consulta ao cliente "CL0001" deve retornar status de erro 404