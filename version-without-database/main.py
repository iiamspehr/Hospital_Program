from DataStructures import LinkedList, Queue, Stack, Graph, DrugTree, Trie, HashMap
import heapq
import math

# Updated Role Management Classes
class Patient:
    def __init__(self, patient_id: str, name: str):
        self.patient_id = patient_id
        self.name = name

class Doctor:
    def __init__(self, doctor_id: str, name: str):
        self.doctor_id = doctor_id
        self.name = name
        self.patient_queue = Queue()
        self.completed_visits = Stack()

    def add_patient(self, patient: Patient):
        self.patient_queue.enqueue(patient)

    def start_visit(self):
        if self.patient_queue.is_empty():
            print("No patients in the queue.")
        else:
            patient = self.patient_queue.dequeue()
            print(f"Visiting patient {patient.name}...")
            self.completed_visits.push(patient)

class Ambulance:
    def __init__(self, ambulance_id: str, location: str):
        self.ambulance_id = ambulance_id
        self.location = location
        self.priority = 0  # Lower values indicate higher priority

class Hospital:
    def __init__(self, hospital_id: str, name: str, location: str):
        self.hospital_id = hospital_id
        self.name = name
        self.location = location
        self.ambulances = []  # List of ambulances assigned to this hospital

    def assign_ambulance(self, ambulance: Ambulance):
        self.ambulances.append(ambulance)

    def remove_ambulance(self, ambulance_id: str):
        self.ambulances = [amb for amb in self.ambulances if amb.ambulance_id != ambulance_id]

class EmergencyManagement:
    def __init__(self):
        self.graph = Graph()
        self.hospitals = {}
        self.ambulances = {}
        self.route_history = HashMap()

    def add_hospital(self, hospital_id, name, location):
        self.hospitals[hospital_id] = Hospital(hospital_id, name, location)
        self.graph.add_node(location)

    def add_ambulance(self, ambulance_id, hospital_id, location):
        if hospital_id in self.hospitals:
            ambulance = Ambulance(ambulance_id, location)
            self.hospitals[hospital_id].assign_ambulance(ambulance)
            self.ambulances[ambulance_id] = ambulance
            self.graph.add_node(location)

    def remove_hospital(self, hospital_id):
        if hospital_id in self.hospitals:
            hospital = self.hospitals.pop(hospital_id)
            for ambulance in hospital.ambulances:
                del self.ambulances[ambulance.ambulance_id]
            self.graph.remove_node(hospital.location)

    def allocate_ambulance(self, patient_location):
        closest_ambulance = None
        min_distance = float("inf")
        for ambulance in self.ambulances.values():
            distance = self.graph.a_star(ambulance.location, patient_location, lambda x, y: 0) #A*
            if distance < min_distance:
                min_distance = distance
                closest_ambulance = ambulance
        if closest_ambulance:
            print(f"Allocated Ambulance {closest_ambulance.ambulance_id} from {closest_ambulance.location} to {patient_location}")
            self.route_history.insert(f"{closest_ambulance.location} -> {patient_location}", min_distance)
            closest_ambulance.location = patient_location
        else:
            print("No available ambulance.")

    def update_ambulance_location(self, ambulance_id, new_location):
        """Updates the location of an ambulance in real-time."""
        if ambulance_id in self.ambulances:
            self.ambulances[ambulance_id].location = new_location


    def display_route_history(self):
        self.route_history.display()
    
    def display_city_graph(self):
        """Displays the city graph with live ambulance locations."""
        print("Displaying City Graph...")

        # Get the latest locations of all ambulances
        ambulance_locations = {amb_id: amb.location for amb_id, amb in self.ambulances.items()}

        # Call visualize() with updated ambulance positions
        self.graph.visualize(ambulance_locations)


def preload_data(doctors, patients, emergency_management, pharmacist_drug_tree, drug_trie):
    print("Preloading default data...")
    
    # Adding default doctors
    doctors["D001"] = Doctor("D001", "Dr. Smith")
    doctors["D002"] = Doctor("D002", "Dr. Johnson")
    
    # Adding default patients
    patients["P001"] = Patient("P001", "Alice")
    patients["P002"] = Patient("P002", "Bob")
    
    # Adding default drugs
    pharmacist_drug_tree.add_drug(101, "Aspirin", "Painkiller", 5.99, 50)
    pharmacist_drug_tree.add_drug(102, "Ibuprofen", "Anti-inflammatory", 7.49, 30)
    pharmacist_drug_tree.add_drug(103, "Amoxicillin", "Antibiotic", 12.99, 25)
    
    # Adding drugs to Trie for autocomplete
    drug_trie.insert("Aspirin")
    drug_trie.insert("Ibuprofen")
    drug_trie.insert("Amoxicillin")
    
    # Adding default locations to Emergency Management
    emergency_management.add_hospital("H001", "Hospital A", "Hospital_A")
    emergency_management.add_hospital("H002", "Hospital B", "Hospital_B")

    # Adding default homes and access points
    emergency_management.graph.add_node("Home_1")
    emergency_management.graph.add_node("Home_2")
    emergency_management.graph.add_node("Access_Point_1")
    
    # Adding ambulances
    emergency_management.add_ambulance("A001", "H001", "Hospital_A")
    emergency_management.add_ambulance("A002", "H002", "Hospital_B")

    # Properly connecting locations (edges must exist)
    emergency_management.graph.add_edge("Hospital_A", "Home_1", 10)
    emergency_management.graph.add_edge("Hospital_A", "Home_2", 15)
    emergency_management.graph.add_edge("Hospital_A", "Access_Point_1", 8)

    emergency_management.graph.add_edge("Hospital_B", "Home_1", 12)
    emergency_management.graph.add_edge("Hospital_B", "Home_2", 8)
    emergency_management.graph.add_edge("Hospital_B", "Access_Point_1", 6)

    emergency_management.graph.add_edge("Home_1", "Access_Point_1", 4)
    emergency_management.graph.add_edge("Home_2", "Access_Point_1", 5)

    print("Default data loaded successfully!")

def main_menu():
    print("Welcome to the Hospital Management System!")
    
    doctors = {}
    patients = {}
    emergency_management = EmergencyManagement()
    pharmacist_drug_tree = DrugTree()
    drug_trie = Trie()
    
    # Preload Data
    preload_data(doctors, patients, emergency_management, pharmacist_drug_tree, drug_trie)

    while True:
        print("\nMain Menu")
        print("1. Doctor Role")
        print("2. Patient Role")
        print("3. Pharmacist Role")
        print("4. Emergency Management (City Graph, Ambulances, Hospitals)")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            doctor_menu(doctors)
        elif choice == "2":
            patient_menu(patients, doctors)
        elif choice == "3":
            pharmacist_menu(pharmacist_drug_tree, drug_trie)
        elif choice == "4":
            emergency_management_menu(emergency_management)
        elif choice == "5":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


def doctor_menu(doctors):
    doctor_id = input("Enter Doctor ID: ")
    if doctor_id not in doctors:
        name = input("Enter Doctor Name: ")
        doctors[doctor_id] = Doctor(doctor_id, name)

    doctor = doctors[doctor_id]
    while True:
        print("\nDoctor Menu")
        print("1. View Patient Queue")
        print("2. Start Visit")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            doctor.patient_queue.display()
        elif choice == "2":
            doctor.start_visit()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")


def patient_menu(patients, doctors):
    patient_id = input("Enter Patient ID: ")
    if patient_id not in patients:
        name = input("Enter Patient Name: ")
        patients[patient_id] = Patient(patient_id, name)

    patient = patients[patient_id]
    while True:
        print("\nPatient Menu")
        print("1. Book Appointment")
        print("2. Cancel Appointment")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            doctor_id = input("Enter Doctor ID to book with: ")
            if doctor_id in doctors:
                doctors[doctor_id].add_patient(patient)
                print(f"Appointment booked with Doctor {doctors[doctor_id].name}.")
            else:
                print("Doctor not found.")
        elif choice == "2":
            doctor_id = input("Enter Doctor ID to cancel appointment with: ")
            if doctor_id in doctors:
                doctor = doctors[doctor_id]
                temp_queue = Queue()
                removed = False
                while not doctor.patient_queue.is_empty():
                    p = doctor.patient_queue.dequeue()
                    if p.patient_id == patient_id:
                        removed = True
                        continue
                    temp_queue.enqueue(p)
                while not temp_queue.is_empty():
                    doctor.patient_queue.enqueue(temp_queue.dequeue())
                print("Appointment canceled." if removed else "No appointment found to cancel.")
            else:
                print("Doctor not found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")


def pharmacist_menu(drug_tree, drug_trie):
    while True:
        print("\nPharmacist Menu")
        print("1. Add a Drug")
        print("2. Delete a Drug")
        print("3. Search for a Drug")
        print("4. Display All Drugs (Sorted)")
        print("5. Auto-Complete Drug Names")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            drug_id = int(input("Enter Drug ID (unique integer): "))
            name = input("Enter Drug Name: ")
            category = input("Enter Drug Category: ")
            price = float(input("Enter Drug Price: "))
            doses = int(input("Enter Number of Doses: "))

            drug_tree.add_drug(drug_id, name, category, price, doses)
            drug_trie.insert(name)

        elif choice == "2":
            drug_id = int(input("Enter Drug ID to delete: "))
            drug_tree.delete_drug(drug_id, drug_trie)

        elif choice == "3":
            search_by = input("Search by (id/name): ").strip().lower()
            if search_by == "id":
                drug_id = int(input("Enter Drug ID: "))
                drug = drug_tree.search_drug(drug_id)
                if drug:
                    print(f"Found: ID={drug.drug_id}, Name={drug.name}, Category={drug.category}, Price={drug.price}, Doses={drug.doses}")
                else:
                    print("Drug not found.")
            elif search_by == "name":
                name = input("Enter Drug Name: ")
                results = drug_trie.search(name)
                print(f"Drugs matching '{name}': {results}")
            else:
                print("Invalid search type.")

        elif choice == "4":
            print("\nDrugs (Sorted by ID):")
            drug_tree.display_in_order()

        elif choice == "5":
            prefix = input("Enter prefix for auto-completion: ")
            suggestions = drug_trie.search(prefix)
            print(f"Suggestions: {suggestions}")

        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")


def emergency_management_menu(emergency_management):
    while True:
        print("\nEmergency Management")
        print("1. Add Hospital")
        print("2. Add Ambulance")
        print("3. Remove Hospital")
        print("4. Allocate Ambulance")
        print("5. Display City Graph")
        print("6. Display Route History")
        print("7. Add Edge ( path / line)")
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            hospital_id = input("Enter Hospital ID: ")
            name = input("Enter Hospital Name: ")
            location = input("Enter Hospital Location: ")
            emergency_management.add_hospital(hospital_id, name, location)
            print(f"Hospital {name} added at {location}.")

        elif choice == "2":
            ambulance_id = input("Enter Ambulance ID: ")
            hospital_id = input("Enter Hospital ID where ambulance is assigned: ")
            location = input("Enter Ambulance Initial Location: ")
            emergency_management.add_ambulance(ambulance_id, hospital_id, location)
            print(f"Ambulance {ambulance_id} added at {location}.")

        elif choice == "3":
            hospital_id = input("Enter Hospital ID to remove: ")
            emergency_management.remove_hospital(hospital_id)
            print(f"Hospital {hospital_id} and its ambulances removed.")

        elif choice == "4":
            patient_location = input("Enter Patient Location: ")
            emergency_management.allocate_ambulance(patient_location)

        elif choice == "5":  # NEW: Display City Graph
            emergency_management.display_city_graph()

        elif choice == "6":  # Display Route History
            emergency_management.display_route_history()

        elif choice=="7":
            start = input("Enter starting point")
            end = input("Enter the ending point")
            weight=int(input("ENter the edge weigh"))
            emergency_management.graph.add_edge(start, end, weight)
        elif choice == "8":
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()