CREATE DATABASE if not exists hospital;
use DATABASE hospital;

CREATE table IF NOT EXISTS user (
    id INT auto_increment primary key,
    age int,
    first_name varchar(255) not null,
    last_name VARCHAR(255) not null, 
    username VARCHAR(255) not null unique,
    password_hash VARCHAR(255) not null,
    user_role ENUM('admin', 'emergancy', 'dector', 'emergancy_doctor', 'drug_store', 'patient') not null,
    logged_in BOOLEAN DEFAULT FALSE
);

-- create table if not exists patient (
--     id int auto_increment primary key,
--     visit_date date,
--     stability ENUM(1, 2, 3, 4, 5),
--     doctor_id,
--     FOREIGN KEY (id) REFERENCES user(id) PRIMARY KEY on delete casade,
--     FOREIGN KEY (doctor_id) REFERENCES user(id) PRIMARY KEY ON user_role='doctor'
-- );