# ============================================================
# HOSPITAL MANAGEMENT SYSTEM
# Promotion Exam (Practical Only) - Due: 29/03/2026
# Total: 100 Marks
# ============================================================

# Global dictionary to store all patient records
patients = {}


def display_menu():
    """Display the main menu of the Hospital Management System."""
    print("\n" + "=" * 50)
    print("       HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 50)
    print("  1. Add Patient")
    print("  2. View All Patients")
    print("  3. View Patient Report")
    print("  4. Update Patient")
    print("  5. Delete Patient")
    print("  6. Search Patient")
    print("  7. Hospital Statistics")
    print("  8. Exit")
    print("=" * 50)


def get_valid_positive_number(prompt):
    """
    Repeatedly ask the user for input until a valid positive number is entered.
    Returns the number as a float.
    """
    while True:
        value = input(prompt)
        try:
            num = float(value)
            if num > 0:
                return num
            else:
                print("  ERROR: Value must be greater than zero. Please try again.")
        except ValueError:
            print("  ERROR: Invalid input. Please enter a valid number.")


def get_valid_age(prompt):
    """Get and validate patient age (must be a positive integer)."""
    while True:
        value = input(prompt)
        try:
            age = int(value)
            if age > 0 and age <= 150:
                return age
            else:
                print("  ERROR: Age must be between 1 and 150. Please try again.")
        except ValueError:
            print("  ERROR: Invalid input. Please enter a whole number.")


def get_valid_gender(prompt):
    """Get and validate patient gender."""
    while True:
        gender = input(prompt).strip().capitalize()
        if gender in ("Male", "Female", "Other"):
            return gender
        print("  ERROR: Gender must be Male, Female, or Other. Please try again.")


def add_patient():
    """
    Add a new patient record.
    Captures: Patient ID, Name, Age, Gender, Diagnosis, and at least 2 treatments with costs.
    (20 Marks)
    """
    print("\n--- ADD NEW PATIENT ---")

    # --- Patient ID (must be unique) ---
    while True:
        patient_id = input("Enter Patient ID (e.g., P001): ").strip()
        if patient_id == "":
            print("  ERROR: Patient ID cannot be empty.")
        elif patient_id in patients:
            print("  ERROR: A patient with this ID already exists. Please use a different ID.")
        else:
            break

    # --- Full Name ---
    while True:
        name = input("Enter Full Name: ").strip()
        if name == "":
            print("  ERROR: Name cannot be empty.")
        else:
            break

    # --- Age (validated) ---
    age = get_valid_age("Enter Age: ")

    # --- Gender (validated) ---
    gender = get_valid_gender("Enter Gender (Male/Female/Other): ")

    # --- Diagnosis ---
    while True:
        diagnosis = input("Enter Diagnosis (e.g., Malaria, Flu): ").strip()
        if diagnosis == "":
            print("  ERROR: Diagnosis cannot be empty.")
        else:
            break

    # --- Treatments (at least 2 with positive costs) ---
    treatments = {}
    print("\n  --- Enter Treatments (at least 2) ---")
    treatment_count = 0

    while treatment_count < 2:
        treatment_name = input(f"  Treatment {treatment_count + 1} Name: ").strip()
        if treatment_name == "":
            print("  ERROR: Treatment name cannot be empty.")
            continue
        if treatment_name in treatments:
            print("  ERROR: This treatment has already been added. Please enter a different one.")
            continue
        cost = get_valid_positive_number(f"  Cost for '{treatment_name}': ")
        treatments[treatment_name] = cost
        treatment_count += 1

    # Allow adding more treatments optionally
    while True:
        add_more = input("\n  Add another treatment? (yes/no): ").strip().lower()
        if add_more in ("no", "n"):
            break
        elif add_more in ("yes", "y"):
            treatment_name = input("  Treatment Name: ").strip()
            if treatment_name == "":
                print("  ERROR: Treatment name cannot be empty.")
                continue
            if treatment_name in treatments:
                print("  ERROR: This treatment already exists. Use Update to change its cost.")
                continue
            cost = get_valid_positive_number(f"  Cost for '{treatment_name}': ")
            treatments[treatment_name] = cost
        else:
            print("  Please enter 'yes' or 'no'.")

    # --- Store patient in dictionary ---
    patients[patient_id] = {
        "name": name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis,
        "treatments": treatments
    }

    print(f"\n  SUCCESS: Patient '{name}' (ID: {patient_id}) added successfully!")


def view_all_patients():
    """
    Display all patients showing Patient ID, Name, and Diagnosis.
    (10 Marks)
    """
    print("\n--- ALL PATIENTS ---")

    if not patients:
        print("  No patients found in the system.")
        return

    print(f"  {'Patient ID':<12} {'Name':<25} {'Diagnosis':<20}")
    print("  " + "-" * 57)

    for pid, details in patients.items():
        name = details["name"]
        diagnosis = details["diagnosis"]
        print(f"  {pid:<12} {name:<25} {diagnosis:<20}")

    print(f"\n  Total Patients: {len(patients)}")


def calculate_bill(treatments):
    """Calculate and return the total bill from a treatments dictionary."""
    return sum(treatments.values())


def view_patient_report():
    """
    Display a full report for a selected patient including all treatments,
    individual costs, and the total bill.
    (20 Marks)
    """
    print("\n--- VIEW PATIENT REPORT ---")

    if not patients:
        print("  No patients found in the system.")
        return

    patient_id = input("Enter Patient ID: ").strip()

    if patient_id not in patients:
        print("  ERROR: Patient not found.")
        return

    p = patients[patient_id]

    print("\n  " + "=" * 45)
    print(f"       PATIENT REPORT - {patient_id}")
    print("  " + "=" * 45)
    print(f"  Name      : {p['name']}")
    print(f"  Age       : {p['age']}")
    print(f"  Gender    : {p['gender']}")
    print(f"  Diagnosis : {p['diagnosis']}")
    print("  " + "-" * 45)
    print(f"  {'Treatment':<25} {'Cost':>10}")
    print("  " + "-" * 45)

    for treatment_name, cost in p["treatments"].items():
        print(f"  {treatment_name:<25} {cost:>10.2f}")

    print("  " + "-" * 45)
    total_bill = calculate_bill(p["treatments"])
    print(f"  {'TOTAL BILL':<25} {total_bill:>10.2f}")
    print("  " + "=" * 45)


def update_patient():
    """
    Allow updating a patient's diagnosis, adding new treatments,
    updating existing treatment costs, and removing treatments.
    (15 Marks)
    """
    print("\n--- UPDATE PATIENT ---")

    if not patients:
        print("  No patients found in the system.")
        return

    patient_id = input("Enter Patient ID: ").strip()

    if patient_id not in patients:
        print("  ERROR: Patient not found.")
        return

    p = patients[patient_id]
    print(f"\n  Patient: {p['name']} (ID: {patient_id})")
    print(f"  Current Diagnosis: {p['diagnosis']}")
    print(f"  Current Treatments: {p['treatments']}")

    while True:
        print("\n  --- Update Options ---")
        print("  1. Update Diagnosis")
        print("  2. Add New Treatment")
        print("  3. Update Treatment Cost")
        print("  4. Remove Treatment")
        print("  5. Done (Back to Main Menu)")
        choice = input("  Select option (1-5): ").strip()

        if choice == "1":
            # --- Update Diagnosis ---
            new_diagnosis = input("  Enter new Diagnosis: ").strip()
            if new_diagnosis == "":
                print("  ERROR: Diagnosis cannot be empty.")
            else:
                p["diagnosis"] = new_diagnosis
                print(f"  SUCCESS: Diagnosis updated to '{new_diagnosis}'.")

        elif choice == "2":
            # --- Add New Treatment ---
            treatment_name = input("  Enter new Treatment Name: ").strip()
            if treatment_name == "":
                print("  ERROR: Treatment name cannot be empty.")
            elif treatment_name in p["treatments"]:
                print("  ERROR: This treatment already exists. Use option 3 to update its cost.")
            else:
                cost = get_valid_positive_number(f"  Enter cost for '{treatment_name}': ")
                p["treatments"][treatment_name] = cost
                print(f"  SUCCESS: Treatment '{treatment_name}' with cost {cost:.2f} added.")

        elif choice == "3":
            # --- Update Treatment Cost ---
            if not p["treatments"]:
                print("  ERROR: No treatments available to update.")
            else:
                print("  Current treatments:")
                for t_name, t_cost in p["treatments"].items():
                    print(f"    - {t_name}: {t_cost:.2f}")
                treatment_name = input("  Enter treatment name to update: ").strip()
                if treatment_name not in p["treatments"]:
                    print("  ERROR: Treatment not found.")
                else:
                    new_cost = get_valid_positive_number(f"  Enter new cost for '{treatment_name}': ")
                    p["treatments"][treatment_name] = new_cost
                    print(f"  SUCCESS: Cost for '{treatment_name}' updated to {new_cost:.2f}.")

        elif choice == "4":
            # --- Remove Treatment ---
            if not p["treatments"]:
                print("  ERROR: No treatments available to remove.")
            else:
                print("  Current treatments:")
                for t_name, t_cost in p["treatments"].items():
                    print(f"    - {t_name}: {t_cost:.2f}")
                treatment_name = input("  Enter treatment name to remove: ").strip()
                if treatment_name not in p["treatments"]:
                    print("  ERROR: Treatment not found.")
                else:
                    del p["treatments"][treatment_name]
                    print(f"  SUCCESS: Treatment '{treatment_name}' removed.")

        elif choice == "5":
            print("  Returning to main menu...")
            break

        else:
            print("  ERROR: Invalid option. Please select 1-5.")


def delete_patient():
    """
    Remove a patient record using Patient ID.
    (10 Marks)
    """
    print("\n--- DELETE PATIENT ---")

    if not patients:
        print("  No patients found in the system.")
        return

    patient_id = input("Enter Patient ID to delete: ").strip()

    if patient_id not in patients:
        print("  ERROR: Patient not found.")
        return

    patient_name = patients[patient_id]["name"]
    confirm = input(f"  Are you sure you want to delete '{patient_name}' (ID: {patient_id})? (yes/no): ").strip().lower()

    if confirm in ("yes", "y"):
        del patients[patient_id]
        print(f"  SUCCESS: Patient '{patient_name}' (ID: {patient_id}) has been deleted.")
    else:
        print("  Deletion cancelled.")


def search_patient():
    """
    Search for a patient by Patient ID or by Name.
    (10 Marks)
    """
    print("\n--- SEARCH PATIENT ---")

    if not patients:
        print("  No patients found in the system.")
        return

    print("  Search by:")
    print("  1. Patient ID")
    print("  2. Patient Name")
    choice = input("  Select option (1-2): ").strip()

    if choice == "1":
        # --- Search by Patient ID ---
        patient_id = input("  Enter Patient ID: ").strip()
        if patient_id in patients:
            p = patients[patient_id]
            print(f"\n  --- Patient Found ---")
            print(f"  Patient ID : {patient_id}")
            print(f"  Name       : {p['name']}")
            print(f"  Age        : {p['age']}")
            print(f"  Gender     : {p['gender']}")
            print(f"  Diagnosis  : {p['diagnosis']}")
        else:
            print("  No patient found with that ID.")

    elif choice == "2":
        # --- Search by Name (partial match, case-insensitive) ---
        search_name = input("  Enter Patient Name (or part of name): ").strip().lower()
        results = []

        for pid, details in patients.items():
            if search_name in details["name"].lower():
                results.append((pid, details))

        if results:
            print(f"\n  --- {len(results)} Patient(s) Found ---")
            print(f"  {'Patient ID':<12} {'Name':<25} {'Age':<6} {'Gender':<8} {'Diagnosis':<20}")
            print("  " + "-" * 71)
            for pid, details in results:
                print(f"  {pid:<12} {details['name']:<25} {details['age']:<6} {details['gender']:<8} {details['diagnosis']:<20}")
        else:
            print("  No patients found with that name.")

    else:
        print("  ERROR: Invalid option. Please select 1 or 2.")


def hospital_statistics():
    """
    Display hospital-wide statistics:
    - Total number of patients
    - Total revenue (sum of all bills)
    - Patient with the highest bill
    - Patient with the lowest bill
    (15 Marks)
    """
    print("\n--- HOSPITAL STATISTICS ---")

    if not patients:
        print("  No patients in the system. No statistics to display.")
        return

    total_patients = len(patients)
    total_revenue = 0.0
    patient_bills = {}

    # Calculate bill for each patient and accumulate total revenue
    for pid, details in patients.items():
        bill = calculate_bill(details["treatments"])
        patient_bills[pid] = bill
        total_revenue += bill

    # Find patient with highest bill
    highest_bill = max(patient_bills.values())
    highest_pid = [pid for pid, bill in patient_bills.items() if bill == highest_bill]

    # Find patient with lowest bill
    lowest_bill = min(patient_bills.values())
    lowest_pid = [pid for pid, bill in patient_bills.items() if bill == lowest_bill]

    # Display statistics
    print("  " + "=" * 45)
    print(f"  Total Patients    : {total_patients}")
    print(f"  Total Revenue     : {total_revenue:.2f}")
    print("  " + "-" * 45)

    # Handle case where multiple patients share highest/lowest bill
    if len(highest_pid) == 1:
        print(f"  Highest Bill      : {highest_bill:.2f}")
        print(f"    Patient        : {patients[highest_pid[0]]['name']} ({highest_pid[0]})")
    else:
        print(f"  Highest Bill      : {highest_bill:.2f}")
        names = ", ".join([f"{patients[pid]['name']} ({pid})" for pid in highest_pid])
        print(f"    Patient(s)     : {names}")

    print("  " + "-" * 45)

    if len(lowest_pid) == 1:
        print(f"  Lowest Bill       : {lowest_bill:.2f}")
        print(f"    Patient        : {patients[lowest_pid[0]]['name']} ({lowest_pid[0]})")
    else:
        print(f"  Lowest Bill       : {lowest_bill:.2f}")
        names = ", ".join([f"{patients[pid]['name']} ({pid})" for pid in lowest_pid])
        print(f"    Patient(s)     : {names}")

    print("  " + "=" * 45)


def main():
    """
    Main function: Displays the menu in a continuous loop until the user chooses to exit.
    """
    while True:
        display_menu()
        choice = input("Select option (1-8): ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_all_patients()
        elif choice == "3":
            view_patient_report()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            delete_patient()
        elif choice == "6":
            search_patient()
        elif choice == "7":
            hospital_statistics()
        elif choice == "8":
            print("\n  Thank you for using the Hospital Management System. Goodbye!")
            break
        else:
            print("  ERROR: Invalid option. Please enter a number between 1 and 8.")


# Entry point of the program

if __name__ == "__main__":
    main()