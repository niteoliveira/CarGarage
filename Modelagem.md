# CarGarage

📘 Modelagem Conceitual e Relacional — Sistema de Alocação de Veículos
🔶 1. Modelagem Conceitual (Diagrama Entidade-Relacionamento)
📌 Entidades principais
Entidade	Atributos
Usuário	id, nome, email, perfil, bloqueado
Veículo	id, placa, modelo, categoria, status
Reserva	id, usuario_id, veiculo_id, início, fim, status
Alocação	id, reserva_id, km_saida, km_retorno, data_saida, data_retorno
Multa	id, usuario_id, motivo, valor, data
Categoria de Veículo	id, nome, descrição
🔗 Relacionamentos

Usuário 1:N Reserva

Reserva 1:1 Alocação

Usuário 1:N Multa

Veículo 1:N Reserva

Categoria de Veículo 1:N Veículo

🧾 Justificativas

Um usuário pode fazer várias reservas, mas cada reserva pertence a um único usuário.

Cada reserva pode gerar no máximo uma alocação, representando o uso real do veículo.

Um veículo pode ser reservado muitas vezes, mas pertence a uma única categoria.

Um usuário pode receber várias multas por diferentes infrações.

Cada veículo pertence a apenas uma categoria, mas uma categoria pode agrupar vários veículos.
