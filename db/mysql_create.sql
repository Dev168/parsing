CREATE TABLE `Bookmakers` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(150),
	PRIMARY KEY (`id`),
	UNIQUE KEY(`Name`)
);

CREATE TABLE `Participants` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(150),
	PRIMARY KEY (`id`)
);

CREATE TABLE `ParticipantNames` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(250) NOT NULL,
	`Bookmaker` bigint NOT NULL,
	`Participant` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `href` (
	`id` bigint NOT NULL,
	`Bookmaker` bigint NOT NULL,
	`href` char(200) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `vs` (
	`id` bigint NOT NULL,
	`FirstParticipant` bigint NOT NULL,
	`SecondParticipant` bigint NOT NULL,
	`FirstWin` double NOT NULL,
	`SecondWin` double NOT NULL,
	`Draw` double NOT NULL,
	`OddsDate` DATETIME NOT NULL,
	`GameDate` DATETIME NOT NULL,
	`Live` BINARY NOT NULL,
	`LiveDate` DATETIME,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Handicap` (
	`id` bigint NOT NULL,
	`FristParticipant` bigint NOT NULL,
	`SecondParticipant` bigint NOT NULL,
	`FirstForward` bigint NOT NULL,
	`FirstWin` double NOT NULL,
	`SecondForward` bigint NOT NULL,
	`SecondWin` double NOT NULL,
	`OddsDate` DATETIME,
	`GameDate` DATETIME,
	`Live` BINARY NOT NULL,
	`LiveDate` DATETIME,
	`href` char(200)
	PRIMARY KEY (`id`)
);

CREATE TABLE `Forwards` (
	`id` bigint NOT NULL,
	`Value` double(3,2) NOT NULL UNIQUE,
	PRIMARY KEY (`id`)
);



ALTER TABLE `ParticipantNames` ADD CONSTRAINT `ParticipantNames_fk0` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `ParticipantNames` ADD CONSTRAINT `ParticipantNames_fk1` FOREIGN KEY (`Participant`) REFERENCES `Participants`(`id`);

ALTER TABLE `ParticipantNames` ADD UNIQUE `unique_index`(`Name`, `Bookmaker`);

ALTER TABLE `Participants` ADD UNIQUE `unique_index` (`Name`);

CREATE TABLE `sports` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(200),
	PRIMARY KEY (`id`),
    UNIQUE KEY(`Name`)
);

CREATE TABLE `sportnames` (
	`id` bigint NOT NULL,
	`Name` char(250) NOT NULL,
	`Bookmaker` bigint NOT NULL,
   	`Sport` bigint,
	PRIMARY KEY (`id`)
);

ALTER TABLE `sportnames` ADD CONSTRAINT `sportnames_fk0` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `sportnames` ADD CONSTRAINT `sportnames_fk1` FOREIGN KEY (`Sport`) REFERENCES `sports`(`id`);

ALTER TABLE `sportnames` ADD UNIQUE `unique_index`(`Name`, `Bookmaker`);

ALTER TABLE `href` ADD CONSTRAINT `href_fk0` FOREIGN KEY (`Bookmaker`) REFERENCES `Bookmakers`(`id`);

ALTER TABLE `vs` ADD CONSTRAINT `vs_fk0` FOREIGN KEY (`FirstParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `vs` ADD CONSTRAINT `vs_fk1` FOREIGN KEY (`SecondParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `Handicap` ADD CONSTRAINT `Handicap_fk0` FOREIGN KEY (`FristParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `Handicap` ADD CONSTRAINT `Handicap_fk1` FOREIGN KEY (`SecondParticipant`) REFERENCES `Participants`(`id`);

ALTER TABLE `Handicap` ADD CONSTRAINT `Handicap_fk2` FOREIGN KEY (`Forward`) REFERENCES `Forwards`(`id`);