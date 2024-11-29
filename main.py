import mysql.connector
import bcrypt


# Handling Data Base management
class Database:

    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

# The user manager class   
class User:

    def __init__(self, db, id=None, firstname=None, lastname=None, username=None, age=None, role=None):
        self.db = db
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.age = age
        self.role = role

    def sign_up(self, id, firstname, lastname, username, password, age, role): #sign up method
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #hash the password for more security
        self.db.execute(
            "INSERT INTO user (id, firstname, lastname, username, password_hash, age, user_role) VALUES (%s, %s, %s, %s, %s, %s)",
            (id, firstname, lastname, username, password_hash, age, role)
        )
        self.db.execute("UPDATE user SET logged_in = FALSE")
        self.db.execute("UPDATE user SET logged_in = TRUE WHERE id = %s", (id,)) #save the signed up user as the main user for this device
        self.db.commit()
        print(f"Successfully signed up as {username}")

    def login(self, username, password): #login method
        cursor = self.db.execute("SELECT id, password_hash FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode(), user[1].encode()):
            self.db.execute("UPDATE user SET logged_in = FALSE")
            self.db.execute("UPDATE user SET logged_in = TRUE WHERE id = %s", (user[0],)) #save this user as the main user for this device
            self.db.commit()
            print(f"Successfully logged in as {username}")
            return True
        else:
            print("Invalid username or password!")
            return False

    def load_last_logged_in_user(self):
        cursor = self.db.execute("SELECT * FROM user WHERE logged_in = TRUE")
        user_data = cursor.fetchone()

        if user_data:
            return User(
                self.db,
                id=user_data[0],
                firstname=user_data[1],
                lastname=user_data[2],
                username=user_data[3],
                age=user_data[4],
                role=user_data[5],
            )

        return None

# The doctor's class
class Doctor(User):

    def __init__(self, db, id=None, firstname=None, lastname=None, username=None, age=None, role="doctor", specialty=None):
        super().__init__(db, id, firstname, lastname, username, age, role)
        self.specialty = specialty  # Additional attribute for doctors

    def view_patients(self):


    def prescribe_medicine(self, patient_id, medicine):
        print(f"Doctor {self.firstname} {self.lastname} is prescribing {medicine} to patient {patient_id}")
        # Example database interaction
        self.db.execute("INSERT INTO prescriptions (doctor_id, patient_id, medicine) VALUES (%s, %s, %s)",
                        (self.id, patient_id, medicine))
        self.db.commit()


# The patient class
class Patient(User):

    def __init__(self, db, id=None, firstname=None, lastname=None, username=None, age=None, role="patient", medical_history=None):
        super().__init__(db, id, firstname, lastname, username, age, role)
        self.medical_history = medical_history or []  # Default to an empty list

    def view_medical_history(self):
        print(f"Medical history for {self.firstname} {self.lastname}: {self.medical_history}")

class Pharmacy(User):
    
    def __init__(self, db, id=None, firstname=None, lastname=None, username=None, age=None, role="pharmacy", inventory=None):
        super().__init__(db, id, firstname, lastname, username, age, role) #pass the user attributes to the user management class
        self.inventory = inventory or []  # Default to an empty list

    def add_medicine(self, medicine, quantity):
        self.db.execute("INSERT INTO inventory (pharmacy_id, medicine, quantity) VALUES (%s, %s, %s)", (self.id, medicine, quantity))
        self.db.commit()
        print(f"Added {quantity} of {medicine} to inventory")



# The main 
if __name__ == "__main__":

    db = Database(host="localhost", user="root", password="sam@rad20", database="hospital")
    user_manager = User(db)
    
    user=user_manager.load_last_logged_in_user()            
    print("Welcome to SEP hospital .\n")
    while user==None:
        print("\n1. Sign Up\n2. Log In\n3. Exit")
        choose=int(input('choose an option .'))
        if choose == 1:
            id=int(input("Enter your national code"))
            firstname = input("Enter first name: ")
            lastname = input("Enter last name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            age = int(input("Enter age: "))
            role = input("Enter role: ")
            user=user_manager.sign_up(id, firstname, lastname, username, password, age, role)
        elif choose == 2:
            username = input("Enter username: ")
            password = input("Enter password: ")
            user=user_manager.login(username, password)
        elif choose == 3:
            break
        else:
            print('invalid entry')