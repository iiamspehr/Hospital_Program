import bcrypt
from DataStructures import LinkedList, Queue, Stack, MinHeap 

# User Management
class User:
    def __init__(self, user_id, name, role, password):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.password = password

class UserManagement:
    def __init__(self):
        self.users = LinkedList()

    def signup(self, user_id, name, role, password):
        user = User(user_id, name, role, password)
        self.users.insert(user)
        print(f"User {name} signed up successfully.")

    def login(self, user_id, password):
        current = self.users.head
        while current:
            if current.data.user_id == user_id and current.data.password == password:
                print(f"Welcome {current.data.name}!")
                return current.data
            current = current.next
        print("Invalid credentials.")
        return None

# Patient Management
class Patient:
    def __init__(self, national_id, name, age):
        self.national_id = national_id
        self.name = name
        self.age = age

class PatientManagement:
    def __init__(self):
        self.patient_queue = Queue()  # Patient queue

    def add_patient(self, national_id, name, age):
        patient = {"national_id": national_id, "name": name, "age": age}
        self.patient_queue.enqueue(patient)
        print(f"Patient {name} added to the queue.")

    def cancel_appointment(self, national_id):
        temp_queue = Queue()
        found = False
        while not self.patient_queue.is_empty():
            patient = self.patient_queue.dequeue()
            if patient["national_id"] != national_id:
                temp_queue.enqueue(patient)
            else:
                print(f"Appointment for patient {patient['name']} canceled.")
                found = True
        self.patient_queue = temp_queue  # Replace the old queue
        if not found:
            print("Patient not found in the queue.")

    def next_patient(self):
        if self.patient_queue.is_empty():
            print("No patients in the queue.")
        else:
            patient = self.patient_queue.dequeue()
            print(f"Next patient: {patient['name']} (ID: {patient['national_id']}).")
            return patient

# Role Doctor
class Doctor:
    def __init__(self, doctor_id, name):
        self.doctor_id = doctor_id
        self.name = name

# Doctor Management
class DoctorManagement:
    def __init__(self):
        self.patient_queue = Queue()  # Queue for patients
        self.completed_visits = Stack()  # Stack for completed visits (optional)

    def add_patient_to_queue(self, patient):
        self.patient_queue.enqueue(patient)
        print(f"Patient {patient['name']} added to the doctor's queue.")

    def view_patients(self):
        print("Patients in the queue:")
        self.patient_queue.display()

    def start_visit(self):
        if self.patient_queue.is_empty():
            print("No patients in the queue.")
        else:
            patient = self.patient_queue.dequeue()
            print(f"Doctor is now seeing {patient['name']}.")
            self.completed_visits.push(patient)  # Record completed visit
            return patient

    def review_completed_visits(self):
        print("Reviewing completed visits:")
        self.completed_visits.display()

# Pharmacy
class Pharmacy:
    def __init__(self):
        self.medicine_stack = Stack()  # Medicine stack

    def add_prescription(self, medicine):
        self.medicine_stack.push(medicine)
        print(f"Medicine '{medicine}' added to the stack.")

    def dispense_medicine(self):
        if self.medicine_stack.is_empty():
            print("No medicines to dispense.")
        else:
            medicine = self.medicine_stack.pop()
            print(f"Dispensed Medicine: {medicine}")

# Emergency Triage
class Triage:
    def __init__(self):
        self.priority_queue = MinHeap() #Using MinHeap

    def add_emergency_case(self, patient, priority):
        self.priority_queue.insert((priority, patient))
        print(f"Patient {patient.name} added to emergency queue with priority {priority}.")

    def attend_patient(self):
        if self.priority_queue.heap:
            priority, patient = self.priority_queue.extract_min()
            print(f"Attending to {patient.name} with priority {priority}.")
        else:
            print("No emergency cases.")

    def view_patients(self):
        self.priority_queue.display()
        print("Cases in the queue:")

# Admin Management
class AdminManagement:
    def __init__(self, user_management):
        self.user_management = user_management

    def add_user(self, user_id, name, role, password):
        self.user_management.signup(user_id, name, role, password)

    def delete_user(self, user_id):
        current = self.user_management.users.head
        prev = None
        while current:
            if current.data.user_id == user_id:
                if prev:
                    prev.next = current.next
                else:
                    self.user_management.users.head = current.next
                print(f"User {user_id} deleted.")
                return
            prev = current
            current = current.next
        print("User not found.")

    def search_user(self, user_id):
        current = self.user_management.users.head
        while current:
            if current.data.user_id == user_id:
                user = current.data
                print(f"Found User: {user.name}, Role: {user.role}")
                return user
            current = current.next
        print("User not found.")
        return None



# Main Program
def main():
    # Initialize management systems
    user_management = UserManagement()
    patient_management = PatientManagement()
    doctor_management = DoctorManagement()
    pharmacy = Pharmacy()
    triage=Triage()

    # Add an admin user for demonstration
    user_management.signup("admin", "Admin", "admin", "admin123")

    print("Welcome to the Hospital Management System!")

    while True:
        print("\nMain Menu")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Sign-Up
            print("\n--- Sign-Up ---")
            user_id = input("Enter User ID: ")
            name = input("Enter Name: ")
            role = input("Enter Role (admin/patient/doctor/pharmacist/triage): ").lower()
            password = input("Enter Password: ")
            user_management.signup(user_id, name, role, password)

        elif choice == "2":
            # Log-In
            print("\n--- Log In ---")
            user_id = input("Enter User ID: ")
            password = input("Enter Password: ")
            user = user_management.login(user_id, password)

            if user:
                if user.role == "admin":
                    # Admin Menu
                    admin = AdminManagement(user_management)
                    while True:
                        print("\nAdmin Menu")
                        print("1. Add User")
                        print("2. Delete User")
                        print("3. Search User")
                        print("4. Logout")
                        admin_choice = input("Enter your choice: ")

                        if admin_choice == "1":
                            user_id = input("Enter User ID: ")
                            name = input("Enter Name: ")
                            role = input("Enter Role (admin/patient/doctor/pharmacist/triage): ").lower()
                            password = input("Enter Password: ")
                            admin.add_user(user_id, name, role, password)

                        elif admin_choice == "2":
                            user_id = input("Enter User ID to delete: ")
                            admin.delete_user(user_id)

                        elif admin_choice == "3":
                            user_id = input("Enter User ID to search: ")
                            admin.search_user(user_id)

                        elif admin_choice == "4":
                            print("Logging out from Admin Menu.")
                            break

                        else:
                            print("Invalid choice. Try again.")

                elif user.role == "triage":
                    # Triage Menu
                    while True:
                        print("\nTriage Menu")
                        print("1. Add Emergency Case")
                        print("2. View Next Emergency Patient")
                        print("3. Logout")
                        triage_choice = input("Enter your choice: ")

                        if triage_choice == "1":
                            national_id = input("Enter Patient National ID: ")
                            name = input("Enter Patient Name: ")
                            severity = int(input("Enter Severity (1 = Critical, higher = Less Critical): "))
                            patient = {"national_id": national_id, "name": name}
                            triage.add_emergency_case(patient, severity)

                        elif triage_choice == "2":
                            triage.attend_patient()

                        elif triage_choice == "3":
                            print("Logging out from Triage Menu.")
                            break

                        else:
                            print("Invalid choice. Try again.")
                            
                elif user.role == "patient":
                    # Patient Menu
                    while True:
                        print("\nPatient Menu")
                        print("1. Book Appointment")
                        print("2. Cancel Appointment")
                        print('3.Emergancy Needs')
                        print("4. Logout")
                        patient_choice = input("Enter your choice: ")

                        if patient_choice == "1":
                            national_id = input("Enter National ID: ")
                            name = input("Enter Name: ")
                            age = int(input("Enter Age: "))
                            patient_management.add_patient(national_id, name, age)

                        elif patient_choice == "2":
                            national_id = input("Enter National ID to cancel: ")
                            patient_management.cancel_appointment(national_id)

                        elif patient_choice == '3':
                            national_id = input("Enter National ID: ")
                            name = input("Enter Name: ")
                            age = int(input("Enter Age:"))
                            patient=Patient(national_id, name, age)
                            priority=int(input("Declare your priority degree from 1 to 5"))
                            triage.add_emergency_case(patient, priority)
                        elif patient_choice == "4":
                            print("Logging out from Patient Menu.")
                            break

                        else:
                            print("Invalid choice. Try again.")

                elif user.role == "doctor":
                    # Doctor Menu
                    while True:
                        print("\nDoctor Menu")
                        print("1. View Patients")
                        print("2. Start Visit")
                        print("3. Review Completed Visits")
                        print("4. Logout")
                        doctor_choice = input("Enter your choice: ")

                        if doctor_choice == "1":
                            doctor_management.view_patients()

                        elif doctor_choice == "2":
                            patient = doctor_management.start_visit()
                            if patient:
                                print(f"Completed visit with {patient['name']}.")

                        elif doctor_choice == "3":
                            doctor_management.review_completed_visits()

                        elif doctor_choice == "4":
                            print("Logging out from Doctor Menu.")
                            break

                        else:
                            print("Invalid choice. Try again.")

                elif user.role == "pharmacist":
                    # Pharmacist Menu
                    while True:
                        print("\nPharmacy Menu")
                        print("1. Add Prescription")
                        print("2. Dispense Medicine")
                        print("3. Logout")
                        pharmacy_choice = input("Enter your choice: ")

                        if pharmacy_choice == "1":
                            medicine = input("Enter Medicine Name: ")
                            pharmacy.add_prescription(medicine)

                        elif pharmacy_choice == "2":
                            pharmacy.dispense_medicine()

                        elif pharmacy_choice == "3":
                            print("Logging out from Pharmacy Menu.")
                            break

                        else:
                            print("Invalid choice. Try again.")

                else:
                    print("Unknown role. Returning to main menu.")

        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()