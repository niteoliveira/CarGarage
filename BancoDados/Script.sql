CREATE TABLE IF NOT EXISTS `Usuario` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`nome` varchar(255) NOT NULL,
	`email` varchar(255) NOT NULL UNIQUE,
	`bloqueado` boolean NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Veiculo` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`modelo` varchar(255) NOT NULL,
	`placa` varchar(255) NOT NULL,
	`categoria` varchar(255) NOT NULL,
	`disponivel` boolean NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Reserva` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`usuario_id` int NOT NULL,
	`veiculo_id` int NOT NULL,
	`inicio_previsto` date NOT NULL,
	`final_previsto` date NOT NULL,
	`status` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Alocacao` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`reserva_id` int NOT NULL,
	`km_saida` float NOT NULL,
	`km_retorno` float NOT NULL,
	`data_saida` date NOT NULL,
	`data_retorno` date NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Multa` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`alocacao_id` int NOT NULL,
	`motivo` varchar(255) NOT NULL,
	`valor` float NOT NULL,
	`data` date NOT NULL,
	PRIMARY KEY (`id`)
);



ALTER TABLE `Reserva` ADD CONSTRAINT `Reserva_fk1` FOREIGN KEY (`usuario_id`) REFERENCES `Usuario`(`id`);

ALTER TABLE `Reserva` ADD CONSTRAINT `Reserva_fk2` FOREIGN KEY (`veiculo_id`) REFERENCES `Veiculo`(`id`);
ALTER TABLE `Alocacao` ADD CONSTRAINT `Alocacao_fk1` FOREIGN KEY (`reserva_id`) REFERENCES `Reserva`(`id`);
ALTER TABLE `Multa` ADD CONSTRAINT `Multa_fk1` FOREIGN KEY (`alocacao_id`) REFERENCES `Alocacao`(`id`);
