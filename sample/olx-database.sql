-- MySQL Script generated by MySQL Workbench
-- Sun Mar 27 21:09:16 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema olx_database
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema olx_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `olx_database` DEFAULT CHARACTER SET utf8 ;
USE `olx_database` ;

-- -----------------------------------------------------
-- Table `olx_database`.`DM_TEMPO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `olx_database`.`DM_TEMPO` (
  `ID_TEMPO` INT NOT NULL AUTO_INCREMENT,
  `ANO` INT NULL,
  `MES` INT NULL,
  `DIA` INT NULL,
  `HORA` INT NULL,
  PRIMARY KEY (`ID_TEMPO`))
ENGINE = MyISAM;

#INSERT INTO `olx_database`.`dm_tempo` VALUES(1,2022,02,03,23), (2, 2021,01,04,19);

-- -----------------------------------------------------
-- Table `olx_database`.`DM_LOCAL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `olx_database`.`DM_LOCAL` (
  `ID_LOCAL` INT NOT NULL AUTO_INCREMENT,
  `ESTADO` VARCHAR(45) NULL,
  `CIDADE` VARCHAR(45) NULL,
  `BAIRRO` VARCHAR(45) NULL,
  PRIMARY KEY (`ID_LOCAL`))
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `olx_database`.`DM_CELULAR`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `olx_database`.`DM_CELULAR` (
  `ID_CELULAR` INT NOT NULL AUTO_INCREMENT,
  `MARCA` VARCHAR(45) NULL,
  `MODELO` VARCHAR(45) NULL,
  `COR` VARCHAR(45) NULL,
  `ESTADO` VARCHAR(45) NULL,
  PRIMARY KEY (`ID_CELULAR`))
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `olx_database`.`DM_ANUNCIANTE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `olx_database`.`DM_ANUNCIANTE` (
  `ID_ANUNCIANTE` INT NOT NULL AUTO_INCREMENT,
  `NOME` VARCHAR(45) NULL,
  `TIPO` VARCHAR(45) NULL,
  PRIMARY KEY (`ID_ANUNCIANTE`))
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `olx_database`.`DM_FATO_ANUNCIOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `olx_database`.`DM_FATO_ANUNCIOS` (
  `ID_TEMPO` INT NOT NULL,
  `ID_LOCAL` INT NOT NULL,
  `ID_CELULAR` INT NOT NULL,
  `ID_ANUNCIANTE` INT NOT NULL,
  `PRECO` FLOAT NULL,
  `DM_TEMPO_ID_TEMPO` INT NOT NULL,
  `ANUNCIANTE_ID_ANUNCIANTE` INT NOT NULL,
  `DM_LOCAL_ID_LOCAL` INT NOT NULL,
  `DM_CELULAR_ID_CELULAR` INT NOT NULL,
  PRIMARY KEY (`ID_TEMPO`, `ID_LOCAL`, `ID_CELULAR`, `ID_ANUNCIANTE`, `DM_TEMPO_ID_TEMPO`, `ANUNCIANTE_ID_ANUNCIANTE`, `DM_LOCAL_ID_LOCAL`, `DM_CELULAR_ID_CELULAR`),
  INDEX `fk_DM_FATO_ANUNCIOS_DM_TEMPO_idx` (`DM_TEMPO_ID_TEMPO` ASC) VISIBLE,
  INDEX `fk_DM_FATO_ANUNCIOS_ANUNCIANTE1_idx` (`ANUNCIANTE_ID_ANUNCIANTE` ASC) VISIBLE,
  INDEX `fk_DM_FATO_ANUNCIOS_DM_LOCAL1_idx` (`DM_LOCAL_ID_LOCAL` ASC) VISIBLE,
  INDEX `fk_DM_FATO_ANUNCIOS_DM_CELULAR1_idx` (`DM_CELULAR_ID_CELULAR` ASC) VISIBLE)
ENGINE = MyISAM;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
