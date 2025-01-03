USE thesis_app_dev;

-- Drop existing tables (if any) to reset the database
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS theses;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       email VARCHAR(120) NOT NULL UNIQUE,
                       password VARCHAR(255) NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create theses table
CREATE TABLE theses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255) NOT NULL,
                        abstract TEXT,
                        status VARCHAR(50) DEFAULT 'In Progress',
                        submission_date DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id INT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);



-- Create forums table
CREATE TABLE posts (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       user_id INT NOT NULL,
                       title VARCHAR(255) NOT NULL,
                       description VARCHAR(255),
                       body TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert test data for users
INSERT INTO users (email, password) VALUES
                                        ('user1@example.com', 'hashed_password_1'),
                                        ('user2@example.com', 'hashed_password_2');

-- Insert test data for theses
INSERT INTO theses (user_id, title, author, abstract, status, submission_date) VALUES
                                                                                   (1, 'Thesis Title 1', 'John Doe', 'Abstract for thesis 1', 'In Progress', '2024-12-22'),
                                                                                   (2, 'Thesis Title 2', 'Jane Doe', 'Abstract for thesis 2', 'Completed', '2024-12-20');

-- Insert forums into forums table
INSERT INTO posts (user_id, title, description, body, created_at)
VALUES
    (1, 'Welcome to the Forum', 'Sample post 1','This is the first forum post!', NOW()),
    (2, 'Discussion about Thesis', 'Sample post 2', 'Share your ideas and feedback.', NOW());

