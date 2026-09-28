import mysql.connector


# =========================================================
# DATABASE CONNECTION
# =========================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter mysql password:"),              # Apna MySQL password
    database="student_portal"
)

cursor = db.cursor(dictionary=True)


# =========================================================
# ADMIN LOGIN DETAILS
# =========================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@123"


# =========================================================
# MAIN STUDENT PORTAL
# =========================================================

print("\n==============================")
print("       STUDENT PORTAL")
print("==============================")

print("1. Student Login")
print("2. Admin Login")

login_type = input("Select Login Type: ")


# =========================================================
# STUDENT LOGIN
# =========================================================

if login_type == "1":

    print("\n========== STUDENT LOGIN ==========")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    query = """
    SELECT * FROM students
    WHERE username = %s AND password = %s
    """

    cursor.execute(query, (username, password))

    student = cursor.fetchone()

    if student:

        print("\nStudent Login Successful!")

        while True:

            print("\n========== STUDENT DASHBOARD ==========")
            print("1. View Profile")
            print("2. View Marks")
            print("3. View Attendance")
            print("4. Logout")

            choice = input("Enter Choice: ")


            # ---------------------------------------------
            # VIEW PROFILE
            # ---------------------------------------------

            if choice == "1":

                print("\n---------- PROFILE ----------")

                print("Name    :", student["name"])
                print("Roll No :", student["roll"])
                print("Age     :", student["age"])
                print("Course  :", student["course"])
                print("Address :", student["address"])


            # ---------------------------------------------
            # VIEW MARKS
            # ---------------------------------------------

            elif choice == "2":

                query = """
                SELECT * FROM marks
                WHERE roll = %s
                """

                cursor.execute(query, (student["roll"],))

                marks = cursor.fetchone()

                print("\n---------- MARKS ----------")

                if marks:

                    print("Python :", marks["python"])
                    print("DBMS   :", marks["dbms"])
                    print("DSA    :", marks["dsa"])
                    print("AI     :", marks["ai"])

                else:

                    print("Marks not available.")


            # ---------------------------------------------
            # VIEW ATTENDANCE
            # ---------------------------------------------

            elif choice == "3":

                attendance = student["attendance"]

                print("\n---------- ATTENDANCE ----------")

                print("Attendance :", attendance, "%")

                if attendance >= 75:
                    print("Status : Good Attendance")

                elif attendance >= 50:
                    print("Status : Attendance Low")

                else:
                    print("Status : Short Attendance")


            # ---------------------------------------------
            # STUDENT LOGOUT
            # ---------------------------------------------

            elif choice == "4":

                print("\nStudent Logout Successful!")
                break

            else:

                print("\nInvalid Choice!")


    else:

        print("\nInvalid Username or Password!")


# =========================================================
# ADMIN LOGIN
# =========================================================

elif login_type == "2":

    print("\n========== ADMIN LOGIN ==========")

    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        print("\nAdmin Login Successful!")

        while True:

            print("1. Add Student")
            print("2. Add Marks")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Logout")

            choice = input("Enter Choice: ")


            # =================================================
            # ADD STUDENT
            # =================================================

            if choice == "1":

                print("\n========== ADD STUDENT ==========")

                try:

                    roll = int(input("Enter Roll No: "))
                    name = input("Enter Name: ")
                    username = input("Enter Username: ")
                    password = input("Enter Password: ")
                    age = int(input("Enter Age: "))
                    course = input("Enter Course: ")
                    address = input("Enter Address: ")
                    attendance = float(input("Enter Attendance: "))


                    query = """
                    INSERT INTO students
                    (roll, name, username, password, age,
                     course, address, attendance)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (
                        roll,
                        name,
                        username,
                        password,
                        age,
                        course,
                        address,
                        attendance
                    )

                    cursor.execute(query, values)

                    db.commit()

                    print("\nStudent Added Successfully!")


                except ValueError:

                    print("\nInvalid Input!")
                    print("Roll No and Age must be numbers.")
                    print("Attendance example: 85.5")


                except mysql.connector.Error as err:

                    print("\nDatabase Error:", err)

                    db.rollback()


            # =================================================
            # ADD MARKS
            # =================================================

            elif choice == "2":

                print("\n========== ADD MARKS ==========")

                try:

                    roll = int(input("Enter Student Roll No: "))

                    python_marks = int(input("Enter Python Marks: "))
                    dbms_marks = int(input("Enter DBMS Marks: "))
                    dsa_marks = int(input("Enter DSA Marks: "))
                    ai_marks = int(input("Enter AI Marks: "))

                    # Check student exists
                    cursor.execute(
                        "SELECT * FROM students WHERE roll = %s",
                        (roll,)
                    )

                    student = cursor.fetchone()

                    if student is None:

                        print("\nStudent Roll No not found!")

                    else:

                        query = """
                        INSERT INTO marks
                        (roll, python, dbms, dsa, ai)
                        VALUES (%s, %s, %s, %s, %s)
                        """

                        values = (
                            roll,
                            python_marks,
                            dbms_marks,
                            dsa_marks,
                            ai_marks
                        )

                        cursor.execute(query, values)

                        db.commit()

                        print("\nMarks Added Successfully!")


                except ValueError:

                    print("\nPlease enter numbers only.")

                except mysql.connector.Error as err:

                    print("\nDatabase Error:", err)

                    db.rollback()
            # =================================================
            # SEARCH STUDENT
            # =================================================

            elif choice == "3":

                print("\nSearch Student feature will be added next.")


            # =================================================
            # UPDATE STUDENT
            # =================================================

            elif choice == "4":

                print("\nUpdate Student feature will be added next.")


            # =================================================
            # DELETE STUDENT
            # =================================================

            elif choice == "5":

                print("\nDelete Student feature will be added next.")


            # =================================================
            # ADMIN LOGOUT
            # =================================================

            elif choice == "6":

                print("\nAdmin Logout Successful!")
                break


            else:

                print("\nInvalid Choice!")


    else:

        print("\nInvalid Admin Username or Password!")


# =========================================================
# INVALID MAIN MENU CHOICE
# =========================================================

else:

    print("\nInvalid Login Type!")


# =========================================================
# CLOSE DATABASE
# =========================================================

cursor.close()
db.close()