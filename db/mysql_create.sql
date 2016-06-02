CREATE TABLE `Bookmakers` (
	`id` bigint NOT NULL,
	`Name` char(50),
	PRIMARY KEY (`id`)
);

CREATE TABLE `Participants` (
	`id` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `ParticipantNames` (
	`id` bigint NOT NULL,
	`Name` char(250) NOT NULL,
	`Bookmaker` bigint NOT NULL,
	`Participant` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `FootballEvents` (
	`id` bigint NOT NULL,
	`FirstParticipant` bigint NOT NULL,
	`SecondParticipant` bigint NOT NULL,
	`EventDate` DATETIME NOT NULL,
	`Current` BINARY NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `FootballBets` (
	`id` bigint NOT NULL,
	`FootballEvent` bigint NOT NULL,
	`Bookmaker` bigint NOT NULL,
	`FirstWin` double NOT NULL,
	`SecondWin` double NOT NULL,
	`Draw` double NOT NULL,
	`Handicap` bigint NOT NULL,
	`Total` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Handicap` (
	`id` bigint NOT NULL,
	`ForwardValue` double NOT NULL,
	`Coff` double NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Total` (
	`id` bigint NOT NULL,
	`Total_under` bool NOT NULL,
	`TotalValue` double NOT NULL,
	`Coff` double NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `ParticipantNames` ADD CONSTRAINT `ParticipantNames_fk0` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `ParticipantNames` ADD CONSTRAINT `ParticipantNames_fk1` FOREIGN KEY (`Participant`) REFERENCES `Participants`(`id`);

ALTER TABLE `FootballEvents` ADD CONSTRAINT `FootballEvents_fk0` FOREIGN KEY (`FirstParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `FootballEvents` ADD CONSTRAINT `FootballEvents_fk1` FOREIGN KEY (`SecondParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `FootballBets` ADD CONSTRAINT `FootballBets_fk0` FOREIGN KEY (`FootballEvent`) REFERENCES `FootballEvents`(`id`);

ALTER TABLE `FootballBets` ADD CONSTRAINT `FootballBets_fk1` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `FootballBets` ADD CONSTRAINT `FootballBets_fk2` FOREIGN KEY (`Handicap`) REFERENCES `Handicap`(`id`);

ALTER TABLE `FootballBets` ADD CONSTRAINT `FootballBets_fk3` FOREIGN KEY (`Total`) REFERENCES `Total`(`id`);

ALTER TABLE `ParticipantNames` ADD UNIQUE `unique_index`(`Name`, `Bookmaker`);

ALTER TABLE `FootballBets` ADD UNIQUE `unique_index`(`FootballEvent`, `Bookmaker`);