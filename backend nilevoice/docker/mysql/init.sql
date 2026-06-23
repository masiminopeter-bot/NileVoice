-- MySQL initialization SQL for NileVoice AI
-- This script creates the application database and schema with utf8mb4 support.

SET sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `nilevoice` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `nilevoice`;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `full_name` VARCHAR(255) NULL,
  `hashed_password` VARCHAR(255) NOT NULL,
  `email_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `verification_token` VARCHAR(128) NULL UNIQUE,
  `verification_sent_at` DATETIME NULL,
  `reset_password_token` VARCHAR(128) NULL UNIQUE,
  `reset_password_sent_at` DATETIME NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
  `last_login_at` DATETIME NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `ix_users_email` (`email`),
  INDEX `ix_users_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `roles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(80) NOT NULL UNIQUE,
  `description` TEXT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `ix_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `languages` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `code` VARCHAR(16) NOT NULL UNIQUE,
  `name` VARCHAR(128) NOT NULL,
  `native_name` VARCHAR(128) NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `description` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `ix_languages_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_roles` (
  `user_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `role_id`),
  CONSTRAINT `fk_user_roles_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_roles_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `translation_submissions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `source_language_id` INT NOT NULL,
  `target_language_id` INT NOT NULL,
  `submission_type` ENUM('word','phrase','sentence') NOT NULL DEFAULT 'word',
  `original_text` TEXT NOT NULL,
  `translated_text` TEXT NULL,
  `status` ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `notes` TEXT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `ix_translation_submissions_user_id` (`user_id`),
  INDEX `ix_translation_submissions_source_language_id` (`source_language_id`),
  INDEX `ix_translation_submissions_target_language_id` (`target_language_id`),
  INDEX `ix_translation_submissions_status` (`status`),
  CONSTRAINT `fk_translation_submissions_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_translation_submissions_source_language` FOREIGN KEY (`source_language_id`) REFERENCES `languages` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_translation_submissions_target_language` FOREIGN KEY (`target_language_id`) REFERENCES `languages` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `dictionary_entries` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `language_id` INT NOT NULL,
  `entry_type` ENUM('word','phrase','sentence') NOT NULL DEFAULT 'word',
  `term` VARCHAR(255) NOT NULL,
  `translation` VARCHAR(255) NOT NULL,
  `part_of_speech` VARCHAR(50) NULL,
  `example` TEXT NULL,
  `is_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `created_by_id` INT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_dictionary_entry_term_translation` (`language_id`, `term`, `translation`),
  INDEX `ix_dictionary_entries_language_id` (`language_id`),
  INDEX `ix_dictionary_entries_entry_type` (`entry_type`),
  INDEX `ix_dictionary_entries_term` (`term`),
  INDEX `ix_dictionary_entries_translation` (`translation`),
  INDEX `ix_dictionary_entries_created_by_id` (`created_by_id`),
  CONSTRAINT `fk_dictionary_entries_language` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_dictionary_entries_created_by` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `contacts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NULL,
  `phone` VARCHAR(50) NULL,
  `subject` VARCHAR(255) NULL,
  `message` TEXT NOT NULL,
  `is_resolved` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `ix_contacts_user_id` (`user_id`),
  CONSTRAINT `fk_contacts_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `audit_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `action` ENUM('create','update','delete','login','logout','token_refresh') NOT NULL,
  `resource_type` VARCHAR(128) NULL,
  `resource_id` VARCHAR(128) NULL,
  `changes` TEXT NULL,
  `ip_address` VARCHAR(45) NULL,
  `user_agent` VARCHAR(255) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `ix_audit_logs_user_id` (`user_id`),
  INDEX `ix_audit_logs_action` (`action`),
  CONSTRAINT `fk_audit_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `refresh_tokens` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `token` VARCHAR(255) NOT NULL UNIQUE,
  `issued_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expires_at` DATETIME NOT NULL,
  `revoked` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `ix_refresh_tokens_user_id` (`user_id`),
  CONSTRAINT `fk_refresh_tokens_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
