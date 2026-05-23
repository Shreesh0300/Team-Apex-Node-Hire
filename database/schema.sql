CREATE DATABASE nodehire_db;
USE nodehire_db;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    bio TEXT,
    hourly_rate DECIMAL(10, 2),
    is_pro BOOLEAN DEFAULT FALSE,
    profile_score INT DEFAULT 0
);

CREATE TABLE Jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50),
    budget DECIMAL(10, 2),
    deadline DATE,
    status VARCHAR(50),
    FOREIGN KEY (client_id) REFERENCES Users(id)
);

CREATE TABLE Proposals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    freelancer_id INT NOT NULL,
    bid_amount DECIMAL(10, 2),
    timeline VARCHAR(255),
    cover_message TEXT,
    ai_relevance_score INT,
    status VARCHAR(50),
    FOREIGN KEY (job_id) REFERENCES Jobs(id),
    FOREIGN KEY (freelancer_id) REFERENCES Users(id)
);

CREATE TABLE Skills_Badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    freelancer_id INT NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (freelancer_id) REFERENCES Users(id)
);

CREATE TABLE Portfolios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    freelancer_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    tech_stack VARCHAR(255),
    project_url VARCHAR(255),
    FOREIGN KEY (freelancer_id) REFERENCES Users(id)
);

CREATE TABLE Milestones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    deliverable_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2),
    status VARCHAR(50),
    FOREIGN KEY (job_id) REFERENCES Jobs(id)
);