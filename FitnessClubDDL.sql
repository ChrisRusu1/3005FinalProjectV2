-- Drop existing tables to ensure the script can run multiple times without errors
DROP TABLE IF EXISTS FitnessAchievements CASCADE;
DROP TABLE IF EXISTS FitnessGoals CASCADE;
DROP TABLE IF EXISTS HealthMetrics CASCADE;
DROP TABLE IF EXISTS PayrollPayments CASCADE;
DROP TABLE IF EXISTS Payments CASCADE;
DROP TABLE IF EXISTS PersonalTrainingSessions CASCADE;
DROP TABLE IF EXISTS ClassBookings CASCADE;
DROP TABLE IF EXISTS FitnessClasses CASCADE;
DROP TABLE IF EXISTS Members CASCADE;
DROP TABLE IF EXISTS Employees CASCADE;
DROP TABLE IF EXISTS ExerciseRoutines CASCADE;
DROP TABLE IF EXISTS Equipment CASCADE;
DROP TABLE IF EXISTS Rooms CASCADE;

-- Create Employees table (renamed from Trainers for consistency, can adjust as needed)
CREATE TABLE Employees (
    EmployeeID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(50),  -- 'Trainer' or 'Admin'
    Specialization VARCHAR(255) NULL,  -- NULL for Admin
    Role VARCHAR(255) NULL,  -- NULL for Trainers
    Salary DECIMAL(10, 2),
    Password VARCHAR(255)
);

-- Create Members table
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Address VARCHAR(255),
    BirthDate DATE,
    MembershipStartDate DATE,
    MembershipType VARCHAR(50),
    Password VARCHAR(255)
);

-- Create Rooms table
CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255),
    Capacity INT
);

-- Create Fitness Classes table
CREATE TABLE FitnessClasses (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255),
    TrainerID INT REFERENCES Employees(EmployeeID),
    RoomID INT REFERENCES Rooms(RoomID),  -- Linking classes to rooms
    Cost DECIMAL(10, 2),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP
);

-- Create ClassBookings table for managing class members (many-to-many relationship)
CREATE TABLE ClassBookings (
    BookingID SERIAL PRIMARY KEY,
    ClassID INT REFERENCES FitnessClasses(ClassID),
    MemberID INT REFERENCES Members(MemberID),
    BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Personal Training Sessions table
CREATE TABLE PersonalTrainingSessions (
    SessionID SERIAL PRIMARY KEY,
    TrainerID INT REFERENCES Employees(EmployeeID),
    RoomID INT REFERENCES Rooms(RoomID),  -- Linking sessions to rooms
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    MemberID INT REFERENCES Members(MemberID) NULL,  -- Initially NULL, set when a member books the session
    SessionStatus VARCHAR(20) DEFAULT 'Available'
);

-- Create Equipment table
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentType VARCHAR(255),
    PurchaseDate DATE,
    LastMaintenanceDate DATE,
    RoomID INT REFERENCES Rooms(RoomID)  -- Equipment linked to specific rooms
);

-- Create Payments table for members
CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    Date DATE,
    Amount DECIMAL(10, 2),
    Status VARCHAR(50)
);

-- Create Payroll Payments table for employees
CREATE TABLE PayrollPayments (
    PayrollID SERIAL PRIMARY KEY,
    EmployeeID INT REFERENCES Employees(EmployeeID),
    PaymentDate DATE,
    Amount DECIMAL(10, 2),
    Status VARCHAR(50)
);

-- Health metrics table to store various health data points for members
CREATE TABLE HealthMetrics (
    MetricID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    Date DATE,
    Weight DECIMAL(5, 2),
    HeartRate INT,  -- Measured in beats per minute
    BloodPressure VARCHAR(50)  -- Stored as a string, e.g., "120/80"
);

-- Fitness goals table for tracking personal fitness objectives
CREATE TABLE FitnessGoals (
    GoalID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    GoalDescription TEXT,
    TargetDate DATE,
    Status VARCHAR(50)  -- For example, "Pending", "Achieved", "Cancelled"
);

-- Fitness achievements table to record notable achievements
CREATE TABLE FitnessAchievements (
    AchievementID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    AchievementDescription TEXT,
    AchievementDate DATE
);

-- Create ExerciseRoutines table
CREATE TABLE ExerciseRoutines (
    RoutineID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    RoutineName VARCHAR(255),
    Description TEXT,
    DateCreated DATE
);