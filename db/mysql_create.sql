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
	`Name` char(250) NOT NULL AUTO_INCREMENT,
	`Bookmaker` bigint NOT NULL AUTO_INCREMENT,
	`Participant` bigint NOT NULL,
	PRIMARY KEY (`Name`,`Bookmaker`)
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
	`FootballEvent` bigint NOT NULL AUTO_INCREMENT,
	`Bookmaker` bigint NOT NULL AUTO_INCREMENT,
	`FirstWin` double NOT NULL,
	`SecondWin` double NOT NULL,
	`Draw` double NOT NULL,
	`Handicap` bigint NOT NULL,
	`Total` bigint NOT NULL,
	PRIMARY KEY (`FootballEvent`,`Bookmaker`)
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
