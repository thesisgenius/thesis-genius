-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: capstone-db-1.cvyq6wyucy8t.us-east-2.rds.amazonaws.com    Database: thesis_app_dev
-- ------------------------------------------------------
-- Server version	8.0.39
-- Check if the validate_password component exists and remove it if loaded
SELECT COUNT(*) INTO @component_exists
FROM mysql.component
WHERE component_urn = 'file://component_validate_password';

-- Dynamically construct the UNINSTALL command if the component exists
SET @uninstall_component_cmd = IF(@component_exists > 0,
                                  'UNINSTALL COMPONENT "file://component_validate_password";',
                                  'SELECT "Component not loaded, skipping UNINSTALL";'
                               );

-- Execute the dynamically constructed command
PREPARE stmt FROM @uninstall_component_cmd;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

DROP DATABASE IF EXISTS thesis_app_dev;
CREATE DATABASE IF NOT EXISTS thesis_app_dev;
CREATE USER IF NOT EXISTS 'thesis_dev'@'localhost' IDENTIFIED BY 'dev_password';
GRANT ALL PRIVILEGES ON thesis_app_dev.* TO 'thesis_dev'@'localhost';
FLUSH PRIVILEGES;

USE thesis_app_dev;

-- Table structure for table `roles`

DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
                         `role_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for roles',
                         `role_name` VARCHAR(20) NOT NULL COMMENT 'Role name',
                         PRIMARY KEY (`role_id`),
                         UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `users`

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
                         `user_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for users',
                         `first_name` VARCHAR(255) NOT NULL COMMENT 'First name',
                         `last_name` VARCHAR(255) NOT NULL COMMENT 'Last name',
                         `email` VARCHAR(255) NOT NULL UNIQUE COMMENT 'Email address',
                         `username` VARCHAR(255) NOT NULL UNIQUE COMMENT 'Username',
                         `password` VARCHAR(255) NOT NULL COMMENT 'Password',
                         `role_id` INT NOT NULL COMMENT 'Foreign key to roles',
                         `is_admin` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Admin flag',
                         `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Active flag',
                         `is_authenticated` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Authenticated flag',
                         `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Created timestamp',
                         `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated timestamp',
                         PRIMARY KEY (`user_id`),
                         FOREIGN KEY (`role_id`) REFERENCES `roles`(`role_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# The schema sets the username field to a blank value ('') rather than defaulting it to the email field.
# MySQL doesn't support dynamic default values that depend on other fields directly in the schema.
# However, you can achieve this behavior with a trigger (see below).
# This will ensure that, if the username field is not explicitly provided during an INSERT operation,
# it will default to the value of the email field.
DELIMITER $$

CREATE TRIGGER set_default_username
    BEFORE INSERT ON `users`
    FOR EACH ROW
BEGIN
    IF NEW.username IS NULL OR NEW.username = '' THEN
        SET NEW.username = NEW.email;
    END IF;
END$$

DELIMITER ;
-- Table structure for table `theses`

DROP TABLE IF EXISTS `theses`;
CREATE TABLE `theses` (
                          `thesis_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for theses',
                          `title` VARCHAR(255) NOT NULL COMMENT 'Thesis title',
                          `abstract` TEXT COMMENT 'Thesis abstract',
                          `status` VARCHAR(255) NOT NULL COMMENT 'Thesis status',
                          `student_id` INT NOT NULL COMMENT 'Foreign key to users',
                          `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Created timestamp',
                          `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated timestamp',
                          PRIMARY KEY (`thesis_id`),
                          FOREIGN KEY (`student_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `posts`

DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
                         `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for posts',
                         `user_id` INT NOT NULL COMMENT 'Foreign key to users',
                         `title` VARCHAR(255) NOT NULL COMMENT 'Post title',
                         `description` TEXT COMMENT 'Post description',
                         `content` TEXT NOT NULL COMMENT 'Post content',
                         `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Created timestamp',
                         `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated timestamp',
                         PRIMARY KEY (`id`),
                         FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `post_comments`

DROP TABLE IF EXISTS `post_comments`;
CREATE TABLE `post_comments` (
                                 `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for comments',
                                 `user_id` INT NOT NULL COMMENT 'Foreign key to users',
                                 `post_id` INT NOT NULL COMMENT 'Foreign key to posts',
                                 `content` TEXT NOT NULL COMMENT 'Comment content',
                                 `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Created timestamp',
                                 `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated timestamp',
                                 PRIMARY KEY (`id`),
                                 FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
                                 FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `session_log`

DROP TABLE IF EXISTS `session_log`;
CREATE TABLE `session_log` (
                               `session_id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for session log',
                               `user_id` INT NOT NULL COMMENT 'Foreign key to users',
                               `login_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Login timestamp',
                               PRIMARY KEY (`session_id`),
                               FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `settings`

DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings` (
                            `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Primary key for settings',
                            `name` VARCHAR(255) NOT NULL UNIQUE COMMENT 'Setting name',
                            `value` TEXT COMMENT 'Setting value',
                            PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
