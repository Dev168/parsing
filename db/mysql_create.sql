-- MySQL Script generated by MySQL Workbench
-- 07/14/16 17:44:32
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Schema betsdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `betsdb`.`bookmakers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `betsdb`.`bookmakers` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `name` CHAR(150) NULL DEFAULT NULL,
  `hostname` CHAR(250) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `Name` (`name` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `betsdb`.`sports`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `betsdb`.`sports` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `name` CHAR(250) NOT NULL,
  `bookmaker` BIGINT(20) NOT NULL,
  `uuid` CHAR(32) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_index` (`name` ASC, `bookmaker` ASC),
  INDEX `sportnames_fk0` (`bookmaker` ASC),
  CONSTRAINT `sportnames_fk0`
    FOREIGN KEY (`bookmaker`)
    REFERENCES `betsdb`.`bookmakers` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `betsdb`.`leagues`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `betsdb`.`leagues` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `name` CHAR(250) NOT NULL,
  `sport` BIGINT(20) NULL DEFAULT NULL,
  `bookmaker` BIGINT(20) NOT NULL,
  `uuid` CHAR(32) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_index` (`name` ASC, `sport` ASC),
  INDEX `leaguesnames_fk2_idx` (`sport` ASC),
  INDEX `leagues_bk_fk_idx` (`bookmaker` ASC),
  CONSTRAINT `Sport_fk`
    FOREIGN KEY (`sport`)
    REFERENCES `betsdb`.`sports` (`id`),
  CONSTRAINT `leagues_bk_fk`
    FOREIGN KEY (`bookmaker`)
    REFERENCES `betsdb`.`bookmakers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `betsdb`.`participants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `betsdb`.`participants` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `name` CHAR(250) NOT NULL,
  `league` BIGINT(20) NOT NULL,
  `bookmaker` BIGINT(20) NOT NULL,
  `uuid` CHAR(32) NULL,
  PRIMARY KEY (`id`),
  INDEX `League_fk_idx` (`league` ASC),
  UNIQUE INDEX `Unique_index_name_le` (`league` ASC, `name` ASC),
  INDEX `part_bk_fk_idx` (`bookmaker` ASC),
  CONSTRAINT `League_fk`
    FOREIGN KEY (`league`)
    REFERENCES `betsdb`.`leagues` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `part_bk_fk`
    FOREIGN KEY (`bookmaker`)
    REFERENCES `betsdb`.`bookmakers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `betsdb`.`handicaps`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `betsdb`.`handicaps` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `firstforward` DOUBLE NOT NULL,
  `firstwin` DOUBLE NOT NULL,
  `secondforward` DOUBLE NOT NULL,
  `secondwin` DOUBLE NOT NULL,
  `oddsdate` DATETIME NOT NULL,
  `live` TINYINT(1) NOT NULL,
  `href` CHAR(200) NULL DEFAULT NULL,
  `actual` TINYINT(1) NOT NULL,
  `firstparticipant` BIGINT(20) NOT NULL,
  `secondparticipant` BIGINT(20) NOT NULL,
  `bookmaker` BIGINT(20) NOT NULL,
  `sport` BIGINT(20) NOT NULL,
  `league` BIGINT(20) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FirstParticipant_fk_idx` (`firstparticipant` ASC),
  INDEX `SecondParticipant_fk_idx` (`secondparticipant` ASC),
  INDEX `Bookmaker_fk_idx` (`bookmaker` ASC),
  INDEX `Sport_fk3_idx` (`sport` ASC),
  INDEX `League_fk3_idx` (`league` ASC),
  CONSTRAINT `Bookmaker_fk`
    FOREIGN KEY (`bookmaker`)
    REFERENCES `betsdb`.`bookmakers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FirstParticipant_fk`
    FOREIGN KEY (`firstparticipant`)
    REFERENCES `betsdb`.`participants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SecondParticipant_fk`
    FOREIGN KEY (`secondparticipant`)
    REFERENCES `betsdb`.`participants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Sport_fk3`
    FOREIGN KEY (`sport`)
    REFERENCES `betsdb`.`sports` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `League_fk3`
    FOREIGN KEY (`league`)
    REFERENCES `betsdb`.`leagues` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `betsdb`.`moneylines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `betsdb`.`moneylines` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `firstwin` DOUBLE NOT NULL,
  `secondwin` DOUBLE NOT NULL,
  `draw` DOUBLE NULL DEFAULT NULL,
  `oddsdate` DATETIME NOT NULL,
  `live` TINYINT(1) NOT NULL,
  `href` CHAR(200) NULL,
  `actual` TINYINT(1) NOT NULL,
  `firstparticipant` BIGINT(20) NOT NULL,
  `secondparticipant` BIGINT(20) NOT NULL,
  `bookmaker` BIGINT(20) NOT NULL,
  `sport` BIGINT(20) NOT NULL,
  `league` BIGINT(20) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `ml_bk_fk_idx` (`bookmaker` ASC),
  INDEX `ml_fp_fk_idx` (`firstparticipant` ASC),
  INDEX `ml_sp_fk_idx` (`secondparticipant` ASC),
  INDEX `ml_leagues_fk_idx` (`league` ASC),
  INDEX `ml_sport_fk_idx` (`sport` ASC),
  CONSTRAINT `ml_bk_fk`
    FOREIGN KEY (`bookmaker`)
    REFERENCES `betsdb`.`bookmakers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ml_fp_fk`
    FOREIGN KEY (`firstparticipant`)
    REFERENCES `betsdb`.`participants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ml_sp_fk`
    FOREIGN KEY (`secondparticipant`)
    REFERENCES `betsdb`.`participants` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ml_leagues_fk`
    FOREIGN KEY (`league`)
    REFERENCES `betsdb`.`leagues` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ml_sport_fk`
    FOREIGN KEY (`sport`)
    REFERENCES `betsdb`.`sports` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

