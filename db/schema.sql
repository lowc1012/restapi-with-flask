DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) COLLATE utf8_bin NOT NULL COMMENT 'task name',
  `status` BOOLEAN DEFAULT 0 NOT NULL COMMENT 'task status',
  PRIMARY KEY  (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;