# CarGarage

📘 Modelagem Conceitual e Relacional — Sistema de Alocação de Veículos

🔶 1. Modelagem Conceitual (Diagrama Entidade-Relacionamento)

🗞️ Regras de negócio

- Gerar multa por atraso: Atrasos na devolução do veículo geram penalidade ou impedem novas alocações por X dias. (50 reais/dia)
- Checklist de estado: Na retirada e devolução do veículo, devem ser registrados quilometragem e etc
- Um veículo só pode ser alocado se tiver uma reserva já prevista cadastrada
- O final de reserva e alocação não pode anteceder o começo.

📌 Entidades principais

| Entidade          | Atributos                                  |
|-------------------|--------------------------------------------|
| Usuário           | id, nome, email, perfil, bloqueado         |
| Veículo           | id, placa, modelo, categoria, disponível    |
| Reserva           | id, usuario_id, veiculo_id, inicio_previsto, final_previsto, status|
| Alocação          | id, reserva_id, km_saida, km_retorno, data_saida, data_retorno |
| Multa             | id, alocacao_id, motivo, valor, data        |

> reserva.status = (previsto, cancelada, realizada)

Usuário: dados dos clientes da locadora
Veículo: dados dos veículos disponíveis
Reserva: Reserva feita com antecedência para alugar um veículo
Alocação: Dados sobre o carro na retirada do veículo e no retorno
Multa: campo gerado caso haja atraso na devolutiva da alocação

🔗 Relacionamentos

- Usuário 1:N Reserva = um usuário pode fazer várias reservas.
- Veículo 1:N Reserva = um veículo pode ser reservado várias vezes (em períodos distintos).
- Reserva 1:1 Alocação = cada reserva pode gerar no máximo uma alocação.
- Alocação 1:N Multa = uma alocação pode ter várias multas.

<img width="1119" height="453" alt="cargarage_1" src="https://github.com/user-attachments/assets/f137b58d-1e6d-42ad-906d-a4bf7fe61529" />

Feito em DBDesigner
