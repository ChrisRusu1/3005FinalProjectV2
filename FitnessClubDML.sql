-- Insert Employees (Trainers and Admins)
INSERT INTO Employees (Name, Type, Specialization, Role, Salary, Password) VALUES
('John Doe', 'Trainer', 'Cardio Specialist', NULL, 50000, 'fqiimehtuvw'), -- password123 encrypted
('Jane Smith', 'Trainer', 'Strength Training', NULL, 52000, 'fqiimehtuvw'),
('Alice Johnson', 'Admin', NULL, 'Operations Manager', 55000, 'fqiimehtuvw');

-- Insert Members
INSERT INTO Members (Name, Email, Address, BirthDate, MembershipStartDate, MembershipType, Password) VALUES
('Tom Brown', 'tombrown@example.com', '1234 Maple St', '1985-08-15', '2023-01-01', 'Premium', 'fqiimehtuvw'),
('Sara Connor', 'saraconnor@example.com', '5678 Oak Ave', '1990-09-25', '2023-01-10', 'Basic', 'fqiimehtuvw'),
('Mike Tyson', 'miketyson@example.com', '91011 Pine Rd', '1980-07-30', '2023-01-20', 'Premium', 'fqiimehtuvw'),
('Chris Redfield', 'chrisredfield@example.com', '1012 Umbrella St', '1986-11-29', '2023-02-01', 'None', 'fqiimehtuvw');

-- Inserting data into Rooms
INSERT INTO Rooms (RoomName, Capacity) VALUES
('Cardio Room', 10),
('Weight Room', 15),
('Yoga Studio', 12);

-- Inserting data into Equipment
INSERT INTO Equipment (EquipmentType, PurchaseDate, LastMaintenanceDate, RoomID) VALUES
('Treadmill', '2022-01-01', '2024-04-01', 1),
('Dumbbells', '2022-02-15', '2024-04-10', 2),
('Yoga Mats', '2023-01-01', '2024-04-15', 3);

-- Inserting data into Fitness Classes with assigned rooms and times
INSERT INTO FitnessClasses (ClassName, TrainerID, RoomID, Cost, StartTime, EndTime) VALUES
('Morning Yoga', 1, 3, 15.00, '2024-05-01 08:00:00', '2024-05-01 09:00:00'),
('Power Lifting', 2, 2, 20.00, '2024-05-01 10:00:00', '2024-05-01 11:00:00'),
('High-Intensity Cardio', 3, 1, 18.00, '2024-05-01 12:00:00', '2024-05-01 13:00:00');

-- Inserting data into Personal Training Sessions with assigned rooms
INSERT INTO PersonalTrainingSessions (TrainerID, RoomID, StartTime, EndTime, SessionStatus) VALUES
(1, 1, '2024-05-01 08:00:00', '2024-05-01 09:00:00', 'Available'),
(2, 2, '2024-05-01 10:00:00', '2024-05-01 11:00:00', 'Available'),
(3, 3, '2024-05-01 12:00:00', '2024-05-01 13:00:00', 'Available');

-- Insert Health Metrics for a member
INSERT INTO HealthMetrics (MemberID, Date, Weight, HeartRate, BloodPressure) VALUES
(1, '2023-12-01', 78.5, 72, '120/80'),
(2, '2023-12-05', 65.0, 75, '118/79');

-- Insert Fitness Goals
INSERT INTO FitnessGoals (MemberID, GoalDescription, TargetDate, Status) VALUES
(1, 'Lose 5 kg by June', '2024-06-01', 'Pending'),
(2, 'Run a 5k without stopping', '2024-05-15', 'Pending');

-- Insert Fitness Achievements
INSERT INTO FitnessAchievements (MemberID, AchievementDescription, AchievementDate) VALUES
(1, 'Completed first marathon', '2023-11-10'),
(2, 'Lifted personal best in bench press', '2023-11-20');

-- Insert example exercise routines for members
INSERT INTO ExerciseRoutines (MemberID, RoutineName, Description, DateCreated) VALUES
(1, 'Cardio Blast', 'A high-intensity routine focused on improving cardiovascular health. Includes 30 minutes of running, 15 minutes of cycling, and 15 minutes of HIIT.', '2023-01-01'),
(1, 'Strength Training', 'Comprehensive weight training session targeting all major muscle groups. Includes 3 sets of bench presses, squats, deadlifts, and overhead presses.', '2023-01-08'),
(2, 'Beginner Yoga', 'Gentle yoga routine for beginners, focusing on flexibility and mindfulness. Includes basic poses like downward dog, warrior, and tree pose.', '2023-01-15'),
(3, 'Marathon Prep', 'A progressive running plan designed to prepare for a half marathon. Includes long-distance runs, sprints, and rest days.', '2023-01-20');

-- Insert ClassBookings for existing members
INSERT INTO ClassBookings (ClassID, MemberID, BookingDate) VALUES
(1, 1, '2024-04-12 09:00:00'),
(2, 1, '2024-04-13 10:00:00'),
(3, 2, '2024-04-14 11:00:00'),
(1, 3, '2024-04-15 12:00:00');

-- Insert booked PersonalTrainingSessions for existing members
INSERT INTO PersonalTrainingSessions (TrainerID, StartTime, EndTime, MemberID, SessionStatus) VALUES
(1, '2024-04-12 09:00:00', '2024-04-12 10:00:00', 1, 'Booked'),
(2, '2024-04-12 11:00:00', '2024-04-12 12:00:00', 2, 'Booked'),
(1, '2024-04-13 09:00:00', '2024-04-13 10:00:00', 3, 'Booked'),
(2, '2024-04-14 14:00:00', '2024-04-14 15:00:00', 1, 'Booked');

-- Insert initial payments for members based on their membership type
INSERT INTO Payments (MemberID, Date, Amount, Status)
SELECT MemberID, CURRENT_DATE, 
       CASE WHEN MembershipType = 'Premium' THEN 150.00
            WHEN MembershipType = 'Basic' THEN 100.00
            ELSE 120.00 -- default price if not Premium or Basic
       END, 
       'Unpaid'
FROM Members;

-- Inserting payroll data for staff members
INSERT INTO PayrollPayments (EmployeeID, PaymentDate, Amount, Status) VALUES
-- Assuming EmployeeIDs from 1 to 3 are valid and correspond to existing staff members in the Employees table
(1, '2024-04-01', 3000.00, 'Paid'),
(1, '2024-05-01', 3000.00, 'Unpaid'),
(2, '2024-04-01', 2500.00, 'Paid'),
(2, '2024-05-01', 2500.00, 'Unpaid'),
(3, '2024-04-01', 3500.00, 'Paid'),
(3, '2024-05-01', 3500.00, 'Unpaid');

