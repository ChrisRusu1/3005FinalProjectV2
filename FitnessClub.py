#Christopher Rusu #101189532
import psycopg2
import configparser
import datetime

config = configparser.ConfigParser()
config.read('config.ini')
shift = 42
def connect_to_db(): # Connect to the PostgreSQL database
    connection = psycopg2.connect( # use the config file to connect to the database
        host=config['postgresql']['host'],
        dbname=config['postgresql']['dbname'],
        user=config['postgresql']['user'],
        password=config['postgresql']['password'],
        port=int(config['postgresql']['port'])
    )
    return connection

def caesar_encrypt(text, shift):
    """Encrypt text using a simple shift cipher (Caesar Cipher)."""
    result = ""

    for i in range(len(text)):
        char = text[i]
        
        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + shift - 97) % 26 + 97)

    return result

def caesar_decrypt(text, shift):
    """Decrypt text using a simple shift cipher (Caesar Cipher)."""
    return caesar_encrypt(text, -shift)

def reset_and_repopulate_database():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Read and execute DDL.sql to reset the database
    with open('FitnessClubDDL.sql', 'r') as file:
        ddl_sql = file.read()
        cursor.execute(ddl_sql)
        conn.commit()
    
    # Read and execute DML.sql to populate the database
    with open('FitnessClubDML.sql', 'r') as file:
        dml_sql = file.read()
        cursor.execute(dml_sql)
        conn.commit()
    
    print("Database has been reset and repopulated.")
    cursor.close()
    conn.close()





def main_menu():
    """ Display the main menu for different user types """
    while True:
        print("\nWelcome to the Health and Fitness Club Management System")
        print("1. Member Login")
        print("2. Member Registration")
        print("3. Trainer Login")
        print("4. Admin Login")
        print("5. Exit")
        choice = input("Enter option: ")

        if choice == '1':
            member_login()
        elif choice == '2':
            member_registration()
        elif choice == '3':
            trainer_login()
        elif choice == '4':
            admin_login()
        elif choice == '5':
            print("Exiting the system...")
            break
        elif choice == '6':  # Hidden option for resetting and repopulating the database
            reset_and_repopulate_database()
        else:
            print("Invalid option. Please enter a number between 1-4.")


#MEMBER FUNCTIONS

def member_registration():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Collect member information
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    address = input("Enter your address: ")
    birth_date = input("Enter your birth date (YYYY-MM-DD): ")
    membership_type = input("Enter membership type (Premium/Basic): ")
    password = input("Enter your password: ")

    # Encrypt the password using Caesar Cipher with a shift of 42
    encrypted_password = caesar_encrypt(password, 42)

    try:
        # Insert the new member into the database
        member_query = """
        INSERT INTO Members (Name, Email, Address, BirthDate, MembershipType, Password)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING MemberID
        """
        cursor.execute(member_query, (name, email, address, birth_date, membership_type, encrypted_password))
        member_id = cursor.fetchone()[0]  # Fetch the new member's ID returned from the INSERT query

        # Assume a fixed amount for demonstration; adjust as necessary
        payment_amount = 100.00 if membership_type == "Basic" else 150.00
        payment_status = "Paid"
        payment_date = "2024-01-01"  # Example date, adjust as necessary

        # Insert a payment entry for the new member
        payment_query = """
        INSERT INTO Payments (MemberID, Date, Amount, Status)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(payment_query, (member_id, payment_date, payment_amount, payment_status))
        conn.commit()
        print("Member registered successfully with initial payment recorded!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while registering the member and recording payment:", error)
    finally:
        cursor.close()
        conn.close()


def member_login():
    conn = connect_to_db()
    cursor = conn.cursor()

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Encrypt the password using Caesar Cipher with a shift of 42
    encrypted_password = caesar_encrypt(password, 42)

    try:
        cursor.execute("SELECT MemberID, Name FROM Members WHERE Email = %s AND Password = %s", (email, encrypted_password))
        result = cursor.fetchone()
        if result:
            print(f"\nWelcome {result[1]}!")
            member_id = result[0]
            member_menu(member_id)
        else:
            print("Invalid login credentials.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while attempting to log in:", error)
    finally:
        cursor.close()
        conn.close()

def member_menu(member_id):
    while True:
        print("\nMember Menu")
        print("1. Profile Management")
        print("2. Dashboard Display")
        print("3. Schedule Management")
        print("4. Logout")

        choice = input("Enter option: ")
        if choice == '1':
            profile_management(member_id)
        elif choice == '2':
            dashboard_display(member_id)
        elif choice == '3':
            schedule_management(member_id)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid option. Please choose between 1-4.")

def profile_management(member_id):
    print("\nProfile Management")
    print("1. Update Profile")
    print("2. Fitness Goals")
    print("3. Health Metrics")
    print("4. Pay Bills")
    print("5. Back to Main Menu")

    choice = input("Enter option: ")
    if choice == '1':
        update_profile(member_id)
    elif choice == '2':
        update_fitness_goals(member_id)
    elif choice == '3':
        update_health_metrics(member_id)
    elif choice == '4':
        pay_bills(member_id)
    elif choice == '5':
        print("Returning to main menu.")
    else:
        print("Invalid option. Please choose between 1-5.")

def update_profile(member_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch current member details
    try:
        cursor.execute("SELECT Name, Email, Address, BirthDate FROM Members WHERE MemberID = %s", (member_id,))
        member = cursor.fetchone()
        if not member:
            print("Member not found.")
            return
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving member details:", error)
        return

    print("\nProfile Management")
    print("Current details:")
    print(f"1. Name: {member[0]}")
    print(f"2. Email: {member[1]}")
    print(f"3. Address: {member[2]}")
    print(f"4. Birth Date: {member[3]} (Cannot be changed)")
    print("Enter new details to update or press enter to keep current values.")

    # Get user inputs, allow blank to keep current
    new_name = input(f"New Name (current: {member[0]}): ") or member[0]
    new_email = input(f"New Email (current: {member[1]}): ") or member[1]
    new_address = input(f"New Address (current: {member[2]}): ") or member[2]

    # Update the database with new values
    update_query = """
    UPDATE Members SET Name = %s, Email = %s, Address = %s WHERE MemberID = %s
    """
    try:
        cursor.execute(update_query, (new_name, new_email, new_address, member_id))
        conn.commit()
        print("Profile updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error updating profile:", error)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def update_fitness_goals(member_id):
    """
    Updates the fitness goals for a given member.

    Args:
        member_id (int): The ID of the member.

    Returns:
        None
    """
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch current fitness goals
    try:
        cursor.execute("SELECT GoalID, GoalDescription, TargetDate, Status FROM FitnessGoals WHERE MemberID = %s", (member_id,))
        goals = cursor.fetchall()
        print("\nCurrent Fitness Goals:")
        if not goals:
            print("No fitness goals found. You can add some!")
            add_new_goal(member_id, cursor, conn)
            return
        for idx, goal in enumerate(goals, 1):
            print(f"{idx}. Description: {goal[1]}, Target Date: {goal[2]}, Status: {goal[3]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving fitness goals:", error)
        return

    print("\nOptions:")
    print("1. Add New Goal")
    print("2. Update Existing Goal")
    print("3. Mark Goal as Achieved")
    print("4. Back to Profile Management")

    choice = input("Enter option: ")
    if choice == '1':
        add_new_goal(member_id, cursor, conn)
    elif choice == '2':
        select_and_update_goal(goals, cursor, conn)
    elif choice == '3':
        select_and_mark_goal_as_achieved(goals, cursor, conn)
    elif choice == '4':
        return
    else:
        print("Invalid option. Please choose between 1-4.")

def add_new_goal(member_id, cursor, conn):
    description = input("Enter goal description: ")
    target_date = input("Enter target date (YYYY-MM-DD): ")
    status = "Pending"  # Default status when adding a new goal
    try:
        cursor.execute("INSERT INTO FitnessGoals (MemberID, GoalDescription, TargetDate, Status) VALUES (%s, %s, %s, %s)",
                       (member_id, description, target_date, status))
        conn.commit()
        print("New fitness goal added successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error adding new fitness goal:", error)
        conn.rollback()

def select_and_update_goal(goals, cursor, conn):
    goal_selection = int(input("Select the number for the goal you want to update: ")) -1
    selected_goal = goals[goal_selection]
    new_description = input("Enter new description or press enter to skip: ")
    new_target_date = input("Enter new target date (YYYY-MM-DD) or press enter to skip: ")
    updates = []
    params = []

    if new_description:
        updates.append("GoalDescription = %s")
        params.append(new_description)
    if new_target_date:
        updates.append("TargetDate = %s")
        params.append(new_target_date)
    params.append(selected_goal[0])

    if updates: # Only execute the update query if there are updates to be made
        update_query = "UPDATE FitnessGoals SET " + ", ".join(updates) + " WHERE GoalID = %s"
        try:
            cursor.execute(update_query, params)
            conn.commit()
            print("Fitness goal updated successfully!")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error updating fitness goal:", error)
            conn.rollback()

def select_and_mark_goal_as_achieved(goals, cursor, conn): # Mark a fitness goal as achieved
    goal_selection = int(input("Select the number for the goal you want to mark as achieved: ")) - 1
    selected_goal = goals[goal_selection]

    try:
        cursor.execute("UPDATE FitnessGoals SET Status = 'Achieved' WHERE GoalID = %s", (selected_goal[0],))
        conn.commit()
        print("Fitness goal marked as achieved!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error marking fitness goal as achieved:", error)
        conn.rollback()

def update_health_metrics(member_id):# Update the health metrics for a given member
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch and display the most recent health metrics for the member
    try:
        cursor.execute("""
        SELECT Date, Weight, HeartRate, BloodPressure
        FROM HealthMetrics
        WHERE MemberID = %s
        ORDER BY Date DESC
        LIMIT 1
        """, (member_id,)) # Fetch the most recent health metrics
        latest_metrics = cursor.fetchone()
        if latest_metrics:
            print("\nMost recent health metrics:")
            print(f"Date: {latest_metrics[0]}, Weight: {latest_metrics[1]} kg, Heart Rate: {latest_metrics[2]} bpm, Blood Pressure: {latest_metrics[3]}")
        else:
            print("\nNo previous health metrics found.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving health metrics:", error)
        cursor.close()
        conn.close()
        return  # Early return if we encounter an error

    print("\nPlease enter your new health metrics:")
    date = input("Date (YYYY-MM-DD): ")
    weight = float(input("Weight (in kg): "))
    heart_rate = int(input("Heart Rate (beats per minute): "))
    blood_pressure = input("Blood Pressure (systolic/diastolic): ")

    try: # Insert the new health metrics into the database
        query = """
        INSERT INTO HealthMetrics (MemberID, Date, Weight, HeartRate, BloodPressure)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (member_id, date, weight, heart_rate, blood_pressure))
        conn.commit()
        print("Health metrics updated successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error updating health metrics:", error)
    finally:
        cursor.close()
        conn.close()

def pay_bills(member_id): # Pay all unpaid bills for a given member
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Retrieve all unpaid payments for the member
        cursor.execute("""
            SELECT PaymentID, Date, Amount
            FROM Payments
            WHERE MemberID = %s AND Status = 'Unpaid'
        """, (member_id,))
        unpaid_bills = cursor.fetchall()

        if unpaid_bills:
            print("\nUnpaid Bills:")
            for bill in unpaid_bills:
                print(f"Payment ID: {bill[0]}, Date: {bill[1]}, Amount: ${bill[2]}")

            # Ask user if they want to proceed with payment
            confirm = input("Do you want to pay all these bills? (yes/no): ")
            if confirm.lower() == 'yes':
                # Update the payment status to 'Paid'
                cursor.execute("""
                    UPDATE Payments
                    SET Status = 'Paid'
                    WHERE MemberID = %s AND Status = 'Unpaid'
                """, (member_id,))
                conn.commit()
                print("All due payments have been marked as paid.")
            else:
                print("No payments were made.")
        else:
            print("No unpaid bills to pay.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to update payment status:", error)
    finally:
        cursor.close()
        conn.close()

def dashboard_display(member_id): # Display the dashboard for a given member
    conn = connect_to_db()
    cursor = conn.cursor()

    print("\nDashboard Display")
    print("1. View Exercise Routines")
    print("2. View Fitness Achievements")
    print("3. View Health Statistics")
    print("4. Back to Member Menu")

    choice = input("Enter option: ")
    if choice == '1':
        view_exercise_routines(member_id, cursor)
    elif choice == '2':
        view_fitness_achievements(member_id)
    elif choice == '3':
        view_health_statistics(member_id)
    elif choice == '4':
        return
    else:
        print("Invalid option. Please choose between 1-4.")

def view_exercise_routines(member_id, cursor):
    try:
        cursor.execute("SELECT RoutineID, RoutineName, Description, DateCreated FROM ExerciseRoutines WHERE MemberID = %s ORDER BY DateCreated DESC", (member_id,)) #  Fetch all exercise routines for the member
        routines = cursor.fetchall()
        if routines:
            print("\nYour Exercise Routines:")
            for routine in routines:
                print(f"ID: {routine[0]}, Name: {routine[1]}, Description: {routine[2]}, Created On: {routine[3]}")
        else:
            print("No exercise routines found.")
            return

        print("\nOptions:")
        print("1. Add New Routine")
        print("2. Delete Routine")
        print("3. Return to Dashboard")
        
        choice = input("Enter option: ") # Allow the user to add or delete exercise routines
        if choice == '1':
            add_exercise_routine(member_id, cursor)
        elif choice == '2':
            delete_exercise_routine(cursor)
        elif choice == '3':
            return
        else:
            print("Invalid option. Please choose between 1-3.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving exercise routines:", error)


def add_exercise_routine(member_id, cursor): # Add a new exercise routine for a given member
    routine_name = input("Enter the name of the routine: ")
    description = input("Enter a description of the routine: ")
    date_created = datetime.date.today()  # Automatically capture the current date

    try:
        cursor.execute("INSERT INTO ExerciseRoutines (MemberID, RoutineName, Description, DateCreated) VALUES (%s, %s, %s, %s)",
                       (member_id, routine_name, description, date_created)) # Insert the new exercise routine into the database
        cursor.connection.commit()
        print("Exercise routine added successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error adding exercise routine:", error)
        cursor.connection.rollback()

def delete_exercise_routine(cursor): # Delete an exercise routine
    routine_id = input("Enter the ID of the routine to delete: ")
    try:
        cursor.execute("DELETE FROM ExerciseRoutines WHERE RoutineID = %s", (routine_id,))
        cursor.connection.commit()
        print("Exercise routine deleted successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error deleting exercise routine:", error)
        cursor.connection.rollback()

def view_fitness_achievements(member_id): # View fitness achievements for a given member
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT AchievementDescription, AchievementDate FROM FitnessAchievements WHERE MemberID = %s ORDER BY AchievementDate DESC", (member_id,)) # Fetch all fitness achievements for the member
        achievements = cursor.fetchall()
        if achievements:
            print("\nYour Fitness Achievements:")
            for achievement in achievements:
                print(f"Description: {achievement[0]}, Date: {achievement[1]}")
        else:
            print("No fitness achievements found.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving fitness achievements:", error)
    finally:
        cursor.close()
        conn.close()

def view_health_statistics(member_id): # View health statistics for a given member
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Fetch all health metrics for the member sorted by date
        cursor.execute("""
            SELECT Weight, HeartRate, BloodPressure, Date
            FROM HealthMetrics
            WHERE MemberID = %s
            ORDER BY Date
        """, (member_id,))
        metrics = cursor.fetchall()

        if metrics:
            print("\nYour Health Statistics:")
            # Display the earliest and the latest metrics
            first_metrics = metrics[0]
            last_metrics = metrics[-1]

            print("First recorded metrics:")
            print(f"Date: {first_metrics[3]}, Weight: {first_metrics[0]} kg, Heart Rate: {first_metrics[1]} bpm, Blood Pressure: {first_metrics[2]}")

            print("Most recent metrics:")
            print(f"Date: {last_metrics[3]}, Weight: {last_metrics[0]} kg, Heart Rate: {last_metrics[1]} bpm, Blood Pressure: {last_metrics[2]}")

            # Calculate changes
            weight_change = last_metrics[0] - first_metrics[0]
            heart_rate_change = last_metrics[1] - first_metrics[1]

            print("\nChanges over time:")
            print(f"Weight Change: {weight_change} kg")
            print(f"Heart Rate Change: {heart_rate_change} bpm")
            # Blood pressure is complex to compare simply as a number, so it's displayed as first and last values.

        else:
            print("No health metrics found. Start tracking your health metrics to see statistics.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving health statistics:", error)
    finally:
        cursor.close()
        conn.close()











def schedule_management(member_id): # Manage the schedule for a given member
    conn = connect_to_db()
    cursor = conn.cursor()

    print("\nSchedule Management")
    print("1. View My Schedule")
    print("2. Book a Session/Class")
    print("3. Cancel a Session/Class")
    print("4. Return to Member Menu")

    choice = input("Enter option: ")
    if choice == '1':
        view_schedule(member_id, cursor)
    elif choice == '2':
        book_session_or_class(member_id, cursor, conn)
    elif choice == '3':
        cancel_session_or_class(member_id, cursor, conn)
    elif choice == '4':
        return
    else:
        print("Invalid option. Please choose between 1-4.")

def view_schedule(member_id, cursor):
    try:
        # Fetch both personal training sessions and fitness classes for the member
        cursor.execute("""
            SELECT 'Session' as Type, p.SessionID as ID, p.TrainerID, p.StartTime as StartDateTime, p.EndTime as EndDateTime 
            FROM PersonalTrainingSessions p
            WHERE p.MemberID = %s AND p.SessionStatus = 'Booked'
            UNION ALL
            SELECT 'Class' as Type, f.ClassID as ID, f.TrainerID, b.BookingDate as StartDateTime, b.BookingDate as EndDateTime
            FROM FitnessClasses f
            JOIN ClassBookings b ON f.ClassID = b.ClassID
            WHERE b.MemberID = %s
            ORDER BY StartDateTime
        """, (member_id, member_id)) # Fetch all upcoming sessions and classes for the member
        schedule = cursor.fetchall()
        if schedule:
            print("\nYour Upcoming Schedule:")
            for item in schedule:
                print(f"Type: {item[0]}, ID: {item[1]}, Trainer ID: {item[2]}, Start Time: {item[3]}, End Time: {item[4]}")
        else:
            print("No upcoming sessions or classes found.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving schedule:", error)



def book_session_or_class(member_id, cursor, conn): # Book a session or class for a given
    print("\nBooking Options:")
    print("1. Book a Fitness Class")
    print("2. Book a Personal Training Session")
    choice = input("Enter option (1 or 2): ")

    if choice == '1':# Book a fitness class
        # Retrieve the membership type of the member
        cursor.execute("SELECT MembershipType FROM Members WHERE MemberID = %s", (member_id,)) # Fetch the membership type of the member
        membership_type = cursor.fetchone()[0]

        # Retrieve available classes not already booked by the member
        cursor.execute("""
            SELECT ClassID, ClassName, Cost 
            FROM FitnessClasses
            WHERE NOT EXISTS (
                SELECT 1
                FROM ClassBookings
                WHERE ClassBookings.ClassID = FitnessClasses.ClassID
                  AND ClassBookings.MemberID = %s
            )
        """, (member_id,)) # Fetch all available classes not already booked by the member
        classes = cursor.fetchall()
        if not classes:
            print("No available classes to book.")
            return
        print("\nAvailable Fitness Classes:")
        for cls in classes:
            cost_display = "Free" if membership_type == "Premium" else f"Cost: ${cls[2]}"
            print(f"Class ID: {cls[0]}, Name: {cls[1]}, {cost_display}") 

        # Allow member to book a class
        class_id = input("Enter Class ID to book: ")
        cursor.execute("INSERT INTO ClassBookings (ClassID, MemberID) VALUES (%s, %s)", (class_id, member_id)) # Book the class for the member
        conn.commit()
        print("Fitness class booked successfully.")
    
    elif choice == '2':# Book a personal training session
        # Retrieve and display available personal training sessions
        cursor.execute("""
            SELECT SessionID, TrainerID, StartTime, EndTime
            FROM PersonalTrainingSessions
            WHERE MemberID IS NULL AND SessionStatus = 'Available'
        """) # Fetch all available personal training sessions
        sessions = cursor.fetchall()
        print("\nAvailable Personal Training Sessions:")
        for session in sessions:
            print(f"Session ID: {session[0]}, Trainer ID: {session[1]}, Start: {session[2]}, End: {session[3]}")

        # Allow member to book a personal training session
        session_id = input("Enter Session ID to book: ")
        cursor.execute("""
            UPDATE PersonalTrainingSessions
            SET MemberID = %s, SessionStatus = 'Booked'
            WHERE SessionID = %s
        """, (member_id, session_id)) # Book the session for the member
        conn.commit()
        print("Personal training session booked successfully.")

def cancel_session_or_class(member_id, cursor, conn):
    print("\nCancellation Options:")
    print("1. Cancel a Fitness Class")
    print("2. Cancel a Personal Training Session")
    choice = input("Enter option (1 or 2): ")

    if choice == '1':# Cancel a fitness class
        # Show the member their current class bookings
        cursor.execute("""
            SELECT b.BookingID, f.ClassName, f.ClassID
            FROM ClassBookings b
            JOIN FitnessClasses f ON b.ClassID = f.ClassID
            WHERE b.MemberID = %s
        """, (member_id,)) # Fetch all fitness classes booked by the member
        bookings = cursor.fetchall()
        if not bookings:
            print("You have no fitness classes to cancel.")
            return
        print("\nYour Booked Fitness Classes:")
        for booking in bookings:
            print(f"Booking ID: {booking[0]}, Class Name: {booking[1]}, Class ID: {booking[2]}")
        
        booking_id = input("Enter Booking ID of the class to cancel: ")
        cursor.execute("DELETE FROM ClassBookings WHERE BookingID = %s AND MemberID = %s", (booking_id, member_id))
        conn.commit()
        print("Fitness class booking cancelled successfully.")

    elif choice == '2': # Cancel a personal training session
        # Show the member their current personal training sessions
        cursor.execute("""
            SELECT SessionID, StartTime, TrainerID
            FROM PersonalTrainingSessions
            WHERE MemberID = %s AND SessionStatus = 'Booked'
        """, (member_id,)) # Fetch all personal training sessions booked by the member
        sessions = cursor.fetchall()
        if not sessions:
            print("You have no personal training sessions to cancel.")
            return
        print("\nYour Booked Personal Training Sessions:")
        for session in sessions:
            print(f"Session ID: {session[0]}, Start Time: {session[1]}, Trainer ID: {session[2]}")

        session_id = input("Enter Session ID of the session to cancel: ")
        cursor.execute("""
            UPDATE PersonalTrainingSessions
            SET MemberID = NULL, SessionStatus = 'Available'
            WHERE SessionID = %s AND MemberID = %s
        """, (session_id, member_id))# Cancel the session for the member
        conn.commit()
        print("Personal training session cancelled successfully.")





#TRAINER FUNCTIONS
def trainer_login():# Login for a trainer
    conn = connect_to_db()
    cursor = conn.cursor()

    print("\nTrainer Login")
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    encrypted_password = caesar_encrypt(password, 42)

    try:
        # Verify trainer credentials
        cursor.execute("""
            SELECT EmployeeID, Name
            FROM Employees
            WHERE Name = %s AND Password = %s AND Type = 'Trainer'
        """, (name, encrypted_password)) # Fetch the trainer details
        result = cursor.fetchone()
        if result:
            print(f"\nWelcome {result[1]}!")
            trainer_id = result[0]
            trainer_menu(trainer_id)
        else:
            print("Invalid login credentials. Please try again.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error during login:", error)
    finally:
        cursor.close()
        conn.close()

def trainer_menu(trainer_id):
    while True:
        print("\nTrainer Menu")
        print("1. View My Schedule")
        print("2. Manage Member Profiles")
        print("3. Logout")

        choice = input("Enter option: ")
        if choice == '1':
            view_trainer_schedule(trainer_id)
        elif choice == '2':
            manage_member_profiles(trainer_id)
        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Invalid option. Please choose between 1-3.")

def view_trainer_schedule(trainer_id):# View the schedule for a given trainer
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT SessionID, MemberID, StartTime, EndTime, SessionStatus
            FROM PersonalTrainingSessions
            WHERE TrainerID = %s
            ORDER BY CASE WHEN SessionStatus = 'Available' THEN 1 ELSE 2 END, StartTime
        """, (trainer_id,)) # Fetch all personal training sessions for the trainer
        sessions = cursor.fetchall()
        if sessions:
            print("\nYour Scheduled Sessions:")
            for session in sessions:
                status = 'Available' if session[4] == 'Available' else f'Booked by Member ID: {session[1]}'
                print(f"Session ID: {session[0]}, Status: {status}, Start Time: {session[2]}, End Time: {session[3]}")
            # Provide options to manage schedule
            manage_schedule_options(trainer_id, conn)
        else:
            print("No sessions currently scheduled.")
            # Provide option to add a new session
            print("Do you want to add a new session? (yes/no): ")
            if input().lower() == 'yes':
                add_session(trainer_id, conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving schedule:", error)
    finally:
        cursor.close()
        conn.close()

def manage_schedule_options(trainer_id, conn): # Provide options to manage the trainer's schedule 
    print("Options: [1] Delete a Session, [2] Add New Session, [3] Return")
    choice = input("Enter option: ")
    if choice == '1':
        delete_session(trainer_id, conn)
    elif choice == '2':
        add_session(trainer_id, conn)
    elif choice == '3':
        return


def delete_session(trainer_id, conn):
    cursor = conn.cursor()
    session_id = input("Enter Session ID to delete: ")
    try:
        cursor.execute("""
            DELETE FROM PersonalTrainingSessions
            WHERE SessionID = %s AND TrainerID = %s
        """, (session_id, trainer_id))# Delete the session
        conn.commit()
        print("Session deleted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error deleting session:", error)
    finally:
        cursor.close()

def add_session(trainer_id, conn):
    cursor = conn.cursor()
    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
    try:
        cursor.execute("""
            INSERT INTO PersonalTrainingSessions (TrainerID, StartTime, EndTime, SessionStatus)
            VALUES (%s, %s, %s, 'Available')
        """, (trainer_id, start_time, end_time)) # Add a new session
        conn.commit()
        print("New session added successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error adding new session:", error)
    finally:
        cursor.close()

def manage_member_profiles(trainer_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # List all members assigned to this trainer with their latest health metric
        cursor.execute("""
            SELECT m.MemberID, m.Name, m.MembershipType, h.Date, h.Weight, h.HeartRate, h.BloodPressure
            FROM Members m
            LEFT JOIN HealthMetrics h ON m.MemberID = h.MemberID
            WHERE EXISTS (
                SELECT 1 FROM PersonalTrainingSessions
                WHERE TrainerID = %s AND MemberID = m.MemberID
            )
            AND h.Date = (
                SELECT MAX(Date) FROM HealthMetrics WHERE MemberID = m.MemberID
            )
        """, (trainer_id,)) # Fetch all members assigned to the trainer
        members = cursor.fetchall()
        if members: # Display the members and their latest health metrics
            print("\nMembers under your training with latest health metrics:")
            for member in members:
                print(f"Member ID: {member[0]}, Name: {member[1]}, Membership Type: {member[2]}, Latest Metrics Date: {member[3]}, Weight: {member[4]}, Heart Rate: {member[5]}, Blood Pressure: {member[6]}")
            # Provide option to add fitness achievements
            add_achievement_option(cursor, conn)
        else:
            print("No members assigned or no recent health metrics available.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error managing member profiles:", error)
    finally:
        cursor.close()
        conn.close()

def add_achievement_option(cursor, conn): # Provide option to add fitness achievements for a member
    print("Do you want to add a fitness achievement for a member? (yes/no): ")
    if input().lower() == 'yes':
        member_id = input("Enter the Member ID to add achievement for: ")
        description = input("Enter the achievement description: ")
        achievement_date = input("Enter the date of achievement (YYYY-MM-DD): ")
        try:
            cursor.execute("""
                INSERT INTO FitnessAchievements (MemberID, AchievementDescription, AchievementDate)
                VALUES (%s, %s, %s)
            """, (member_id, description, achievement_date)) # Add the fitness achievement
            conn.commit()
            print("Fitness achievement added successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error adding fitness achievement:", error)





#ADMIN FUNCTIONS
def admin_login():# Login for an admin
    conn = connect_to_db()
    cursor = conn.cursor()

    print("\nAdmin Login")
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    encrypted_password = caesar_encrypt(password, 42)

    try:
        # Verify admin credentials
        cursor.execute("""
            SELECT EmployeeID, Name
            FROM Employees
            WHERE Name = %s AND Password = %s AND Type = 'Admin'
        """, (name, encrypted_password))
        result = cursor.fetchone()
        if result:
            print(f"\nWelcome {result[1]}!")
            admin_id = result[0]
            admin_menu(admin_id)
        else:
            print("Invalid login credentials. Please try again.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error during login:", error)
    finally:
        cursor.close()
        conn.close()

def admin_menu(admin_id):
    while True:
        print("\nAdmin Menu")
        print("1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Class Schedule Updating")
        print("4. Billing and Payment Processing")
        print("5. Logout")

        choice = input("Enter option: ")
        if choice == '1':
            manage_room_bookings()
        elif choice == '2':
            monitor_equipment_maintenance()
        elif choice == '3':
            update_class_schedule()
        elif choice == '4':
            process_payments()
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid option. Please choose between 1-5.")

def manage_room_bookings():
    conn = connect_to_db()
    cursor = conn.cursor()
    while True:
        print("\nRoom Booking Management")
        print("1. View Current Bookings")
        print("2. Add New Booking")
        print("3. Delete Booking")
        print("4. Return to Admin Menu")

        choice = input("Enter option: ")
        if choice == '1':
            view_current_bookings(cursor)
        elif choice == '2':
            add_new_booking(cursor, conn)
        elif choice == '3':
            delete_booking(cursor, conn)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please choose between 1-4.")

    cursor.close()
    conn.close()

def view_current_bookings(cursor):
    print("\nCurrent Room Bookings:")
    # Fetch and display bookings for classes
    cursor.execute("""
        SELECT f.ClassID, f.ClassName, r.RoomName, f.StartTime, f.EndTime
        FROM FitnessClasses f
        JOIN Rooms r ON f.RoomID = r.RoomID
    """) # Fetch all fitness classes
    classes = cursor.fetchall()
    print("\nFitness Classes:")
    for cls in classes:
        print(f"Class ID: {cls[0]}, Name: {cls[1]}, Room: {cls[2]}, Start Time: {cls[3]}, End Time: {cls[4]}")

    # Fetch and display bookings for personal training sessions
    cursor.execute("""
        SELECT p.SessionID, e.Name, p.StartTime, p.EndTime, r.RoomName
        FROM PersonalTrainingSessions p
        JOIN Rooms r ON p.RoomID = r.RoomID
        JOIN Employees e ON p.TrainerID = e.EmployeeID
    """) # Fetch all personal training sessions
    sessions = cursor.fetchall()
    print("\nPersonal Training Sessions:")
    for session in sessions:
        print(f"Session ID: {session[0]}, Trainer: {session[1]}, Start Time: {session[2]}, End Time: {session[3]}, Room: {session[4]}")

def add_new_booking(cursor, conn):
    # This function will add new bookings for rooms based on input
    room_id = input("Enter Room ID to book: ")
    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
    # Determine if booking is for a class or session
    booking_type = input("Is this booking for a class or session? (class/session): ")
    if booking_type.lower() == 'class':
        class_name = input("Enter Class Name: ")
        trainer_id = input("Enter Trainer ID: ")
        cost = input("Enter Cost: ")
        cursor.execute("""
            INSERT INTO FitnessClasses (ClassName, TrainerID, RoomID, StartTime, EndTime, Cost)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (class_name, trainer_id, room_id, start_time, end_time, cost))
    elif booking_type.lower() == 'session':
        trainer_id = input("Enter Trainer ID: ")
        cursor.execute("""
            INSERT INTO PersonalTrainingSessions (TrainerID, RoomID, StartTime, EndTime, SessionStatus)
            VALUES (%s, %s, %s, %s, 'Available')
        """, (trainer_id, room_id, start_time, end_time)) # Add a new session
    else:
        print("Invalid booking type entered.")
        return
    conn.commit()
    print("New booking added successfully.")

def delete_booking(cursor, conn): # Delete a booking for a room
    # This function will delete bookings based on input
    booking_type = input("Is this booking for a class or session? (class/session): ")
    booking_id = input("Enter an ID to delete: ")
    if booking_type.lower() == 'class':
        cursor.execute("DELETE FROM FitnessClasses WHERE ClassID = %s", (booking_id,)) # Delete the class
    elif booking_type.lower() == 'session':
        cursor.execute("DELETE FROM PersonalTrainingSessions WHERE SessionID = %s", (booking_id,)) # Delete the session
    else:
        print("Invalid booking type entered.")
        return
    conn.commit()
    print("Booking deleted successfully.")

def monitor_equipment_maintenance():
    conn = connect_to_db()
    cursor = conn.cursor()
    while True:
        print("\nEquipment Maintenance Monitoring")
        print("1. View Equipment Status")
        print("2. Update Maintenance Record")
        print("3. Return to Admin Menu")

        choice = input("Enter option: ")
        if choice == '1':
            view_equipment_status(cursor)
        elif choice == '2':
            update_maintenance_record(cursor, conn)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please choose between 1-3.")

    cursor.close()
    conn.close()

def view_equipment_status(cursor):
    print("\nCurrent Equipment Status:")
    cursor.execute("""
        SELECT EquipmentID, EquipmentType, LastMaintenanceDate, RoomID
        FROM Equipment
        ORDER BY LastMaintenanceDate
    """) # Fetch all equipment
    equipment = cursor.fetchall()
    if equipment:
        for item in equipment:
            print(f"Equipment ID: {item[0]}, Type: {item[1]}, Last Maintenance: {item[2]}, Room ID: {item[3]}")
    else:
        print("No equipment records found.")

def update_maintenance_record(cursor, conn):
    equipment_id = input("Enter Equipment ID to update: ")
    new_maintenance_date = input("Enter new maintenance date (YYYY-MM-DD): ")
    try:
        cursor.execute("""
            UPDATE Equipment
            SET LastMaintenanceDate = %s
            WHERE EquipmentID = %s
        """, (new_maintenance_date, equipment_id)) # Update the maintenance record
        conn.commit()
        print("Maintenance record updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to update maintenance record:", error)

def update_class_schedule():
    conn = connect_to_db()
    cursor = conn.cursor()
    while True:
        print("\nClass Schedule Updating")
        print("1. View Current Class Schedule")
        print("2. Add New Class")
        print("3. Update Existing Class")
        print("4. Delete Class")
        print("5. Return to Admin Menu")

        choice = input("Enter option: ")
        if choice == '1':
            view_class_schedule(cursor)
        elif choice == '2':
            add_new_class(cursor, conn)
        elif choice == '3':
            update_existing_class(cursor, conn)
        elif choice == '4':
            delete_class(cursor, conn)
        elif choice == '5':
            break
        else:
            print("Invalid option. Please choose between 1-5.")

    cursor.close()
    conn.close()

def view_class_schedule(cursor):
    print("\nCurrent Class Schedule:")
    cursor.execute("""
        SELECT ClassID, ClassName, TrainerID, RoomID, StartTime, EndTime, Cost
        FROM FitnessClasses
        ORDER BY StartTime
    """) # Fetch all fitness classes
    classes = cursor.fetchall()
    if classes:
        for cls in classes:
            print(f"Class ID: {cls[0]}, Name: {cls[1]}, Trainer ID: {cls[2]}, Room ID: {cls[3]}, Start: {cls[4]}, End: {cls[5]}, Cost: ${cls[6]}")
    else:
        print("No classes found.")

def add_new_class(cursor, conn):
    class_name = input("Enter class name: ")
    trainer_id = input("Enter trainer ID: ")
    room_id = input("Enter room ID: ")
    start_time = input("Enter start time (YYYY-MM-DD HH:MM): ")
    end_time = input("Enter end time (YYYY-MM-DD HH:MM): ")
    cost = input("Enter cost: ")
    try:
        cursor.execute("""
            INSERT INTO FitnessClasses (ClassName, TrainerID, RoomID, StartTime, EndTime, Cost)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (class_name, trainer_id, room_id, start_time, end_time, cost)) # Add a new class
        conn.commit()
        print("New class added successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to add new class:", error)

def update_existing_class(cursor, conn):
    # First, display all the current classes
    print("\nAvailable Classes:")
    cursor.execute("""
        SELECT ClassID, ClassName, TrainerID, RoomID, StartTime, EndTime, Cost
        FROM FitnessClasses
        ORDER BY StartTime
    """) # Fetch all fitness classes
    classes = cursor.fetchall()
    if not classes:
        print("No classes available to update.")
        return

    for cls in classes:
        print(f"Class ID: {cls[0]}, Name: {cls[1]}, Trainer: {cls[2]}, Room: {cls[3]}, Starts: {cls[4]}, Ends: {cls[5]}, Cost: ${cls[6]}")

    # Ask the admin to enter the class ID they wish to update
    class_id = input("Enter the Class ID of the class you want to update: ")

    # Fetch the specific class details to show current values (optional, can enhance UX)
    cursor.execute("""
        SELECT ClassName, StartTime, EndTime, Cost
        FROM FitnessClasses
        WHERE ClassID = %s
    """, (class_id,)) # Fetch the specific class details
    class_info = cursor.fetchone()
    if not class_info:
        print("Class not found.")
        return

    print(f"Updating class: {class_info[0]}")
    print(f"Current Start Time: {class_info[1]}, End Time: {class_info[2]}, Cost: {class_info[3]}")

    # Prompt for updates
    new_name = input("Enter new class name or press enter to skip: ")
    new_start_time = input("Enter new start time (YYYY-MM-DD HH:MM) or press enter to skip: ")
    new_end_time = input("Enter new end time (YYYY-MM-DD HH:MM) or press enter to skip: ")
    new_cost = input("Enter new cost or press enter to skip: ")
    updates = []
    params = []

    if new_name:
        updates.append("ClassName = %s")
        params.append(new_name)
    if new_start_time:
        updates.append("StartTime = %s")
        params.append(new_start_time)
    if new_end_time:
        updates.append("EndTime = %s")
        params.append(new_end_time)
    if new_cost:
        updates.append("Cost = %s")
        params.append(new_cost)
    params.append(class_id)

    if updates: # If there are updates to be made
        update_query = "UPDATE FitnessClasses SET " + ", ".join(updates) + " WHERE ClassID = %s"
        try:
            cursor.execute(update_query, params)
            conn.commit()
            print("Class updated successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error updating class:", error)
            conn.rollback()

def delete_class(cursor, conn):
    class_id = input("Enter class ID to delete: ")
    
    # First, attempt to delete any bookings associated with the class
    try:
        cursor.execute("DELETE FROM ClassBookings WHERE ClassID = %s", (class_id,))
        conn.commit()
        print("All associated class bookings deleted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error deleting associated class bookings:", error)
        # Roll back any changes if error occurs
        conn.rollback()
        return  # Exit the function if we can't delete the bookings

    # Now attempt to delete the class itself
    try:
        cursor.execute("DELETE FROM FitnessClasses WHERE ClassID = %s", (class_id,))
        conn.commit()
        print("Class deleted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error deleting class:", error)
        # Roll back any changes if error occurs
        conn.rollback()

def process_payments(): # Process payments for outstanding bills and payroll
    conn = connect_to_db()
    cursor = conn.cursor()
    while True:
        print("\nBilling and Payment Processing")
        print("1. View Member Outstanding Bills")
        print("2. View and Manage Payroll")
        print("3. Return to Admin Menu")

        choice = input("Enter option: ")
        if choice == '1':
            view_member_outstanding_bills(cursor)
        elif choice == '2':
            manage_payroll(cursor, conn)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please choose between 1-3.")

    cursor.close()
    conn.close()

def view_member_outstanding_bills(cursor): # View outstanding bills for members
    print("\nOutstanding Member Bills:")
    cursor.execute("""
        SELECT m.MemberID, m.Name, p.PaymentID, p.Date, p.Amount, p.Status
        FROM Members m
        JOIN Payments p ON m.MemberID = p.MemberID
        WHERE p.Status = 'Unpaid'
        ORDER BY p.Date
    """) # Fetch all outstanding bills
    bills = cursor.fetchall()
    if bills:
        for bill in bills:
            print(f"Member ID: {bill[0]}, Name: {bill[1]}, Payment ID: {bill[2]}, Date: {bill[3]}, Amount Due: ${bill[4]}, Status: {bill[5]}")
    else:
        print("No outstanding bills.")

def manage_payroll(cursor, conn): # Manage payroll for employees
    print("\nPayroll Management:")
    cursor.execute("""
        SELECT Employees.EmployeeID, Employees.Name, Employees.Salary, PayrollPayments.PayrollID,
               PayrollPayments.PaymentDate, PayrollPayments.Amount, PayrollPayments.Status
        FROM Employees
        JOIN PayrollPayments ON Employees.EmployeeID = PayrollPayments.EmployeeID
        WHERE PayrollPayments.Status = 'Unpaid'
        ORDER BY PayrollPayments.PaymentDate
    """) # Fetch all unpaid payroll data
    payroll = cursor.fetchall()
    print("Payroll Details for Unpaid Staff:")
    if payroll:
        for pay in payroll:
            print(f"Payroll ID: {pay[3]}, Employee ID: {pay[0]}, Name: {pay[1]}, Date: {pay[4]}, Amount Due: ${pay[5]}, Status: {pay[6]}")
        
        # Ask if they want to process a payment
        if input("\nWould you like to process a payment? (yes/no): ").lower() == 'yes':
            payroll_id = input("Enter the Payroll ID of the staff member to pay: ")
            process_staff_payment(payroll_id, cursor, conn)
    else:
        print("No unpaid payroll data found.")

def process_staff_payment(payroll_id, cursor, conn):
    try:
        # Update the status to 'Paid'
        cursor.execute("""
            UPDATE PayrollPayments
            SET Status = 'Paid'
            WHERE PayrollID = %s
        """, (payroll_id,))
        conn.commit()
        print("Payment processed successfully for Payroll ID:", payroll_id)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to process payment:", error)
        conn.rollback()




if __name__ == '__main__':
    conn = connect_to_db()
    if conn is not None:
        main_menu()
        conn.close()
