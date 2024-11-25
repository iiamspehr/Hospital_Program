import mysql.connector
import bcrypt

# Connection setup
try:
    connection = mysql.connector.connect(
        host='localhost',        
        user='root',             
        password='password123',  
        database='hospital'   
    )
    
    cursor=connection.cursor()
    
    if connection.is_connected():
        print("Successfully connected to the database")
        
        # Perform operations here
        
except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")


class main:

    # sign up function
    def sign_up(firstname, lastname, username, password, id, age, role):

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())    #hash the password

        cursor.execute("INSERT INTO user (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        connection.commit()
        print(f"successfully signed up as {username}")

    # login function
    def login(username, password):
        
        cursor.execute("SELECT id, password_hash from user where username=%s", (username, ))
        user=cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        
            cursor.execute("UPDATE user SET last_login = FALSE")
            cursor.execute("UPDATE user SET last_login = TRUE WHERE id = %s", (user[0],))
            connection.commit()
            print(f"successful logged in as {username}")
        else:
            print("Invalid username or password!")
        

        
    # def __init__(self, first_name, last_name, age, id,role):               
    #     self.first_name=first_name
    #     self.last_name=last_name
    #     self.age=age
    #     self.id=id
    #     self.role=role