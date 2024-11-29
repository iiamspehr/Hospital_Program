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

CREATE TABLE doctor (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);


CREATE TABLE patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medical_history TEXT, -- Stores history as a JSON or text string
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE pharmacy (
    pharmacy_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    inventory TEXT, -- Stores inventory as a JSON or text string
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
        