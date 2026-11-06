
-- Optional sample data for local testing
USE task_manager;

INSERT IGNORE INTO Users VALUES
(6, 'Alex', 'Taylor', 'alex@example.com'),
(7, 'Jane', 'Doe', 'jane@example.com');

INSERT IGNORE INTO Tasks (taskId, Name, DueDate, UserId)
VALUES
(106, 'Test Task', DATE_ADD(CURDATE(), INTERVAL 3 DAY), 6),
(107, 'Project Work', DATE_ADD(CURDATE(), INTERVAL 5 DAY), 7);
