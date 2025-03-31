USE user;

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    password VARCHAR(255) NOT NULL,
    weight FLOAT NOT NULL,
    goal VARCHAR(20) NOT NULL
); 