-- MySQL dump 10.9
--
-- Host: localhost    Database: ASV-Wortschatz-DB-Schema
-- ------------------------------------------------------
-- Server version	4.1.14-max ???
-- Based on default schema, default for corpora exports
-- tables: co_n, co_s, inv_w, inv_s, words, sentences, sentences_tok, sources, meta


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- CREATE Database
--

CREATE DATABASE `oci_community_2023`;

USE `oci_community_2023`;


--
-- Table structure for table `co_n`
--

DROP TABLE IF EXISTS `co_n`;
CREATE TABLE `co_n` (
  `w1_id` int(10) unsigned NOT NULL default '0',
  `w2_id` int(10) unsigned NOT NULL default '0',
  `freq` int(8) unsigned default NULL,
  `sig` float(8) default NULL,
  PRIMARY KEY `w1_w2` (`w1_id`,`w2_id`),
  KEY `w1_sig` (`w1_id`,`sig`),
  KEY `w2_sig` (`w2_id`,`sig`)
) ENGINE=MyISAM CHARSET=utf8mb4;


--
-- Table structure for table `co_s`
--

DROP TABLE IF EXISTS `co_s`;
CREATE TABLE `co_s` (
  `w1_id` int(10) unsigned NOT NULL default '0',
  `w2_id` int(10) unsigned NOT NULL default '0',
  `freq` int(8) unsigned default NULL,
  `sig` float(8) default NULL,
  PRIMARY KEY `w1_w2` (`w1_id`,`w2_id`),
  KEY `w1_sig` (`w1_id`,`sig`),
  KEY `w2_sig` (`w2_id`,`sig`)
) ENGINE=MyISAM CHARSET=utf8mb4;


--
-- Table structure for table `inv_so`
--

DROP TABLE IF EXISTS `inv_so`;
CREATE TABLE `inv_so` (
  `so_id` int(10) unsigned NOT NULL default '0',
  `s_id` int(10) unsigned NOT NULL default '0',
  KEY  `s_id` (`s_id`),
  KEY  `so_id` (`so_id`)
) ENGINE=MyISAM CHARSET=utf8mb4;


--
-- Table structure for table `inv_w`
--

DROP TABLE IF EXISTS `inv_w`;
CREATE TABLE `inv_w` (
  `w_id` int(10) unsigned NOT NULL default '0',
  `s_id` int(10) unsigned NOT NULL default '0',
  `pos` mediumint(2) unsigned NOT NULL default '0',
  KEY `w_id` (`w_id`),
  KEY `s_id` (`s_id`),
  KEY `w_s` (`w_id`,`s_id`)
) ENGINE=MyISAM CHARSET=utf8mb4;


--
-- Table structure for table `sentences`
--

DROP TABLE IF EXISTS `sentences`;
CREATE TABLE `sentences` (
  `s_id` int(10) unsigned NOT NULL auto_increment,
  `sentence` text NOT NULL,
  PRIMARY KEY `s_id` (`s_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sources`
--

DROP TABLE IF EXISTS `sources`;
CREATE TABLE `sources` (
  `so_id` int(10) unsigned NOT NULL auto_increment,
  `source` varchar(255) default NULL,
  `date` date default NULL,
  PRIMARY KEY `so_id` (`so_id`),
  KEY `date` (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
CREATE TABLE `words` (
  `w_id` int(10) unsigned NOT NULL auto_increment,
  `word` varchar(255) character set utf8mb4 collate utf8mb4_bin NOT NULL,
  `freq` int(10) unsigned default NULL,
  PRIMARY KEY `w_id` (`w_id`),
  UNIQUE KEY `word` (`word`(250))
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `meta`
--

DROP TABLE IF EXISTS `meta`;
CREATE TABLE `meta` (
  `run` mediumint(8) unsigned DEFAULT '0' NOT NULL,
  `attribute` varchar(255) binary DEFAULT '' NOT NULL,
  `value` varchar(255) binary DEFAULT '' NOT NULL,
  UNIQUE KEY `meta` (`run`, `attribute`(245))
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sentences_tagged`
--

DROP TABLE IF EXISTS `sentences_tagged`;
CREATE TABLE `sentences_tagged` (
  `s_id` int(10) unsigned NOT NULL,
  `sentence` text,
  PRIMARY KEY `s_id` (`s_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `words_pos_base`
--

DROP TABLE IF EXISTS `words_pos_base`;
CREATE TABLE `words_pos_base` (
  `w_id` int(10) unsigned NOT NULL DEFAULT '0',
  `word` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `pos` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `pos_ud17` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '',
  `base_form` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '',
  `freq` int(8) unsigned DEFAULT NULL,
  UNIQUE KEY `w_id` (`w_id`, `word`(92), `pos`, `base_form`(92)),
  KEY `i_w_id` (`w_id`),
  KEY `i_word` (`word`(191))
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `sim_w_co`
--

CREATE TABLE `sim_w_co` (
  `w1_id` int(10) unsigned NOT NULL DEFAULT '0',
  `w2_id` int(10) unsigned NOT NULL DEFAULT '0',
  `cos` decimal(4,3) DEFAULT NULL,
  KEY `w1_id` (`w1_id`),
  KEY `w2_id` (`w2_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


--
-- Disable keys for import
--

ALTER TABLE `co_n` DISABLE KEYS;
ALTER TABLE `co_s` DISABLE KEYS;
ALTER TABLE `inv_so` DISABLE KEYS;
ALTER TABLE `inv_w` DISABLE KEYS;
ALTER TABLE `sentences` DISABLE KEYS;
ALTER TABLE `sources` DISABLE KEYS;
ALTER TABLE `words` DISABLE KEYS;
ALTER TABLE `meta` DISABLE KEYS;
ALTER TABLE `sentences_tagged` DISABLE KEYS;
ALTER TABLE `words_pos_base` DISABLE KEYS;
ALTER TABLE `sim_w_co` DISABLE KEYS;


--
-- Load data from local files
--

LOAD DATA LOCAL INFILE 'oci_community_2023-words.txt' INTO TABLE words CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-sentences.txt' INTO TABLE sentences CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-co_s.txt' INTO TABLE co_s CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-co_n.txt' INTO TABLE co_n CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-inv_w.txt' INTO TABLE inv_w CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-inv_so.txt' INTO TABLE inv_so CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-sources.txt' INTO TABLE sources CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'oci_community_2023-meta.txt' INTO TABLE meta CHARACTER SET utf8mb4;


--
-- Enable keys after import
--

ALTER TABLE `co_n` ENABLE KEYS;
ALTER TABLE `co_s` ENABLE KEYS;
ALTER TABLE `inv_so` ENABLE KEYS;
ALTER TABLE `inv_w` ENABLE KEYS;
ALTER TABLE `sentences` ENABLE KEYS;
ALTER TABLE `sources` ENABLE KEYS;
ALTER TABLE `words` ENABLE KEYS;
ALTER TABLE `meta` ENABLE KEYS;
ALTER TABLE `sentences_tagged` ENABLE KEYS;
ALTER TABLE `words_pos_base` ENABLE KEYS;
ALTER TABLE `sim_w_co` ENABLE KEYS;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
