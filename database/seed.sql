USE nodehire_db;

INSERT INTO Users (name, email, password_hash, role, bio, hourly_rate, is_pro, profile_score) VALUES
('Aarav Mehta', 'aarav@client.com', 'pwd123', 'Client', 'Tech Startup Founder looking for top talent', 0.00, TRUE, 0),
('Priya Sharma', 'priya@client.com', 'pwd123', 'Client', 'Creative Director at Digital Agency', 0.00, FALSE, 0),
('Rahul Verma', 'rahul@freelancer.com', 'pwd123', 'Freelancer', 'Senior Python Backend Developer', 45.00, TRUE, 95),
('Neha Gupta', 'neha@freelancer.com', 'pwd123', 'Freelancer', 'Frontend React Specialist', 35.00, FALSE, 88),
('Vikram Singh', 'vikram@freelancer.com', 'pwd123', 'Freelancer', 'Full Stack Data Scientist', 55.00, TRUE, 98);

INSERT INTO Jobs (client_id, title, description, project_type, budget, deadline, status) VALUES
(1, 'Build FastAPI Backend', 'Need a Python expert to build a secure API for our mobile app.', 'Fixed', 1200.00, '2026-06-15', 'Open'),
(1, 'Database Migration', 'Migrate legacy data from MongoDB to a structured MySQL database.', 'Hourly', 50.00, '2026-06-01', 'Open'),
(2, 'React UI Dashboard', 'Create a responsive dashboard UI for our internal analytics platform.', 'Fixed', 800.00, '2026-06-10', 'Open');

INSERT INTO Proposals (job_id, freelancer_id, bid_amount, timeline, cover_message, ai_relevance_score, status) VALUES
(1, 3, 1100.00, '2 weeks', 'I have extensive experience building scalable APIs using FastAPI and MySQL.', 92, 'Pending'),
(1, 5, 1200.00, '10 days', 'I can build the API and ensure the database architecture is highly optimized.', 85, 'Pending'),
(3, 4, 750.00, '1 week', 'React is my core specialty. I can deliver a pixel-perfect dashboard.', 95, 'Pending');

INSERT INTO Skills_Badges (freelancer_id, skill_name, is_verified) VALUES
(3, 'Python', TRUE),
(3, 'FastAPI', TRUE),
(4, 'React', TRUE),
(5, 'MySQL', TRUE);