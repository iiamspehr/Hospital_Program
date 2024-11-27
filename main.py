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
class UserManager:

    def __init__(self, db):
        self.db = db

    def sign_up(self, id, firstname, lastname, username, password, age, role): #sign up method
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #hash the password for more security
        self.db.execute(
            "INSERT INTO user (id, firstname, lastname, username, password_hash, age, user_role) VALUES (%s, %s, %s, %s, %s, %s)",
            (id, firstname, lastname, username, password_hash, age, role)
        )
        self.db.execute("UPDATE user SET logged_in = FALSE")
        self.db.execute("UPDATE user SET logged_in = TRUE WHERE id = %s", (id,))
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

    def load_last_logged_in_user(self): #This method manages save and load operations
        cursor = self.db.execute("SELECT username FROM user WHERE logged_in = TRUE")
        user = cursor.fetchone()
        return user[0] if user else None


# The main 
if __name__ == "__main__":

    db = Database(host="localhost", user="root", password="password123", database="hospital")
    user_manager = UserManager(db)

    try:
        
        while True:
            print("\n1. Sign Up\n2. Log In\n3. Load Last Logged In User\n4. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                firstname = input("Enter first name: ")
                lastname = input("Enter last name: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                age = int(input("Enter age: "))
                role = input("Enter role: ")
                user_manager.sign_up(firstname, lastname, username, password, age, role)
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user_manager.login(username, password)
            elif choice == "3":
                last_user = user_manager.load_last_logged_in_user()
                if last_user:
                    print(f"Last logged in user: {last_user}")
                else:
                    print("No user is currently logged in.")
            elif choice == "4":
                break
            else:
                print("Invalid option. Try again!")
    finally:
        db.close()