
CREATE DATABASE IF NOT EXISTS task_manager;
USE task_manager;

CREATE TABLE IF NOT EXISTS Users (
    userId INT NOT NULL,
    FirstName VARCHAR(45) DEFAULT NULL,
    LastName VARCHAR(45) DEFAULT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (userId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS Tasks (
    taskId INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    DueDate DATE NOT NULL,
    UserId INT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (taskId),
    KEY fkuser_idx (UserId),
    CONSTRAINT fkUser FOREIGN KEY (UserId) REFERENCES Users (userId)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DELIMITER //
DROP TRIGGER IF EXISTS check_due_date//
CREATE TRIGGER check_due_date
BEFORE INSERT ON Tasks
FOR EACH ROW
BEGIN
    IF NEW.DueDate <= CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DueDate must be in the future.';
    END IF;
    SET NEW.done = 0;
END;
//
DELIMITER ;

INSERT IGNORE INTO Users (userId, FirstName, LastName, email) VALUES
(1, 'Aaditya', 'Yadav', 'aadi@example.com'),
(2, 'John', 'Smith', 'john@example.com'),
(3, 'Joe', 'Clark', 'joe@example.com'),
(4, 'Charlie', 'Brown', 'charlie@example.com'),
(5, 'Manish', 'Yadav', 'manish@example.com');


INSERT IGNORE INTO Tasks (taskId, Name, DueDate, UserId)
VALUES
(101, 'Submit Project', DATE_ADD(CURDATE(), INTERVAL 3 DAY), 1),
(102, 'Prepare Slides', DATE_ADD(CURDATE(), INTERVAL 2 DAY), 1),
(103, 'Do Homework', DATE_ADD(CURDATE(), INTERVAL 5 DAY), 2),
(104, 'Read Article', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 3),
(105, 'Workout', DATE_ADD(CURDATE(), INTERVAL 4 DAY), 4);

DELIMITER //
DROP FUNCTION IF EXISTS Pending//
CREATE FUNCTION Pending(uId INT, n INT) RETURNS INT
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE dueTasks INT;
    SELECT COUNT(*) INTO dueTasks
    FROM Tasks
    WHERE UserId = uId
      AND done = 0
      AND DueDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL n DAY);
    RETURN dueTasks;
END;
//
DELIMITER ;

CREATE TABLE IF NOT EXISTS ALERT LIKE Tasks;

DELIMITER //
DROP PROCEDURE IF EXISTS cleaning//
CREATE PROCEDURE cleaning()
BEGIN
    INSERT INTO ALERT
    SELECT *
    FROM Tasks
    WHERE DueDate <= CURDATE();
    DELETE FROM Tasks
    WHERE DueDate <= CURDATE();
END;
//
DELIMITER ;
