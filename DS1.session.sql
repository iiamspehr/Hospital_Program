CREATE DATABASE IF NOT EXISTS hospital;  
USE hospital;  

CREATE TABLE IF NOT EXISTS user (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    first_name VARCHAR(255) NOT NULL,  
    last_name VARCHAR(255) NOT NULL,   
    username VARCHAR(255) NOT NULL UNIQUE,  
    password_hash VARCHAR(255) NOT NULL,  
    age INT,  
    user_role ENUM("admin", "emergency", "doctor", "emergency_doctor", "drug_store", "patient") NOT NULL,  
    logged_in BOOLEAN DEFAULT FALSE  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
