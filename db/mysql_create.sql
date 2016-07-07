CREATE TABLE `bookmakers` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(150),
	PRIMARY KEY (`id`),
	UNIQUE KEY(`Name`),
	`hostname` char(250)
);

CREATE TABLE `participants` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(150),
	`League` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `participantNames` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(250) NOT NULL,
	`Bookmaker` bigint NOT NULL,
	`Participant` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `leagues` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(150),
	`Sport` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `leaguesNames` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(250) NOT NULL,
	`Bookmaker` bigint NOT NULL,
	`League` bigint,
	PRIMARY KEY (`id`)
);

CREATE TABLE `vs` (
	`id` bigint NOT NULL AUTO_INCREMENT,
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

CREATE TABLE `handicaps` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`firstparticipant` bigint NOT NULL,
	`secondparticipant` bigint NOT NULL,
	`firstforward` double NOT NULL,
	`firstwin` double NOT NULL,
	`secondforward` double NOT NULL,
	`secondwin` double NOT NULL,
	`oddsdate` DATETIME NOT NULL,
	`gamedate` DATETIME,
	`live` BOOLEAN NOT NULL,
	`href` char(200),
	`actual` BOOLEAN NOT NULL,
	`bookmaker` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `sports` (
	`id` bigint NOT NULL AUTO_INCREMENT,
	`Name` char(200),
	PRIMARY KEY (`id`),
    UNIQUE KEY(`Name`)
);

CREATE TABLE `sportnames` (
	`id` bigint NOT  AUTO_INCREMENT,
	`Name` char(250) NOT NULL,
	`Bookmaker` bigint NOT NULL,
   	`Sport` bigint,
	PRIMARY KEY (`id`)
);

ALTER TABLE `participantNames` ADD CONSTRAINT `ParticipantNames_fk0` FOREIGN KEY (`bookmaker`) REFERENCES `bookmakers`(`id`);

ALTER TABLE `participantNames` ADD CONSTRAINT `ParticipantNames_fk1` FOREIGN KEY (`participant`) REFERENCES `participants`(`id`);

ALTER TABLE `participantNames` ADD UNIQUE `unique_index`(`Name`, `Bookmaker`);


ALTER TABLE `participants` ADD UNIQUE `unique_index` (`Name`);

ALTER TABLE `participants` ADD CONSTRAINT `participants_fk1` FOREIGN KEY (`league`) REFERENCES `leagues`(`id`);


ALTER TABLE `leagues` ADD CONSTRAINT `leagues_fk1` FOREIGN KEY (`sport`) REFERENCES `sports`(`id`);


ALTER TABLE `leaguesNames` ADD UNIQUE `unique_index`(`Name`, `Bookmaker`);

ALTER TABLE `leaguesNames` ADD CONSTRAINT `leaguesnames_fk1` FOREIGN KEY (`league`) REFERENCES `leagues`(`id`);


ALTER TABLE `sportnames` ADD CONSTRAINT `sportnames_fk0` FOREIGN KEY (`bookmaker`) REFERENCES `bookmakers`(`id`);

ALTER TABLE `sportnames` ADD CONSTRAINT `sportnames_fk1` FOREIGN KEY (`sport`) REFERENCES `sports`(`id`);

ALTER TABLE `sportnames` ADD UNIQUE `unique_index`(`Name`, `Bookmaker`);


ALTER TABLE `vs` ADD CONSTRAINT `vs_fk0` FOREIGN KEY (`firstparticipant`) REFERENCES `participants`(`id`);

ALTER TABLE `vs` ADD CONSTRAINT `vs_fk1` FOREIGN KEY (`secondparticipant`) REFERENCES `participants`(`id`);


ALTER TABLE `handicaps` ADD CONSTRAINT `Handicap_fk0` FOREIGN KEY (`firstparticipant`) REFERENCES `participants`(`id`);

ALTER TABLE `handicaps` ADD CONSTRAINT `Handicap_fk1` FOREIGN KEY (`SecondParticipant`) REFERENCES `participants`(`id`);

ALTER TABLE `handicaps` ADD CONSTRAINT `handicaps_fk2` FOREIGN KEY (`bookmaker`) REFERENCES `bookmakers`(`id`);
