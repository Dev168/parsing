CREATE TABLE `Bookmakers` (
	`id` bigint NOT NULL,
	`Name` char(50),
	PRIMARY KEY (`id`)
);

CREATE TABLE `Countries` (
	`id` bigint NOT NULL,
	`name` char(100) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Leagues` (
	`id` bigint NOT NULL,
	`Country` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `LeagueNames` (
	`Name` char(250) NOT NULL AUTO_INCREMENT,
	`Bookmaker` bigint NOT NULL AUTO_INCREMENT,
	`League` bigint NOT NULL,
	PRIMARY KEY (`Name`,`Bookmaker`)
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
	`League` bigint NOT NULL,
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
	PRIMARY KEY (`FootballEvent`,`Bookmaker`)
);

ALTER TABLE `Leagues` ADD CONSTRAINT `Leagues_fk0` FOREIGN KEY (`Country`) REFERENCES `Countries`(`id`);

ALTER TABLE `LeagueNames` ADD CONSTRAINT `LeagueNames_fk0` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `LeagueNames` ADD CONSTRAINT `LeagueNames_fk1` FOREIGN KEY (`League`) REFERENCES `Leagues`(`id`);

ALTER TABLE `ParticipantNames` ADD CONSTRAINT `ParticipantNames_fk0` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `ParticipantNames` ADD CONSTRAINT `ParticipantNames_fk1` FOREIGN KEY (`Participant`) REFERENCES `Participants`(`id`);

ALTER TABLE `FootballEvents` ADD CONSTRAINT `FootballEvents_fk0` FOREIGN KEY (`League`) REFERENCES `Leagues`(`id`);

ALTER TABLE `FootballEvents` ADD CONSTRAINT `FootballEvents_fk1` FOREIGN KEY (`FirstParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `FootballEvents` ADD CONSTRAINT `FootballEvents_fk2` FOREIGN KEY (`SecondParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `FootballBets` ADD CONSTRAINT `FootballBets_fk0` FOREIGN KEY (`FootballEvent`) REFERENCES `FootballEvents`(`id`);

ALTER TABLE `FootballBets` ADD CONSTRAINT `FootballBets_fk1` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

