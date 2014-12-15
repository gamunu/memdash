CREATE TABLE IF NOT EXISTS `Servers` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(500) NOT NULL,
    `port` INT(6) NOT NULL,
    CONSTRAINT pk_servers PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `Statistics` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `server_id` INT(11) NOT NULL,
    `get_hits` INT NOT NULL,
    `get_misses` INT NOT NULL,
    `set_cmd` INT NOT NULL,
    `get_cmd` INT NOT NULL,
    `cached_items` INT NOT NULL,
    `response_time` DECIMAL(8,2) NOT NULL,
    `memory` decimal(10,2) NOT NULL,
    `record` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_stats PRIMARY KEY (`id`),
    CONSTRAINT fk_servers FOREIGN KEY (`server_id`) REFERENCES `Servers`(`id`) ON DELETE CASCADE
);