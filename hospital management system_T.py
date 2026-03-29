
#                     HOSPITAL MANAGEMENT 
# Global data store (nested dictionaries)
patients = {}

# =============================================================================
#  UTILITY / HELPER FUNCTIONS
# =============================================================================

def display_separator(char="=", length=65):
    """Print a visual separator line."""
    print(char * length)

def display_header(title):
    """Print a formatted section header."""
    display_separator()
    print(f"  {title.upper()}")
    display_separator()

def get_positive_float(prompt):
    """
    Prompt the user until a valid positive number is entered.
    Returns a float.
    """
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if number <= 0:
                print("  [!] Cost must be a positive number. Please try again.")
            else:
                return number
        except ValueError:
            print("  [!] Invalid input. Please enter a numeric value.")

def get_non_empty_string(prompt):
    """Prompt the user until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] This field cannot be empty. Please try again.")

def get_positive_integer(prompt):
    """Prompt the user until a valid positive integer is entered."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number <= 0:
                print("  [!] Please enter a positive whole number.")
            else:
                return number
        except ValueError:
            print("  [!] Invalid input. Please enter a whole number.")

def get_valid_gender():
    """Prompt until the user enters Male, Female, or Other."""
    while True:
        gender = input("  Gender (Male / Female / Other): ").strip().title()
        if gender in ("Male", "Female", "Other"):
            return gender
        print("  [!] Please enter Male, Female, or Other.")

def patient_exists(patient_id):
    """Return True if the patient_id is already in the records."""
    return patient_id.upper() in patients

def format_currency(amount):
    """Return a nicely formatted currency string."""
    return f"K {amount:,.2f}"

def calculate_total_bill(patient_id):
    """Return the sum of all treatment costs for a given patient."""
    pid = patient_id.upper()
    return sum(patients[pid]["treatments"].values())

# =============================================================================
#  1. ADD PATIENT  
# =============================================================================

def add_patient():
    """Capture and store a new patient record with at least two treatments."""
    display_header("Add New Patient")

    # Patient ID
    while True:
        patient_id = get_non_empty_string("  Patient ID (e.g. P001): ").upper()
        if patient_exists(patient_id):
            print(f"  [!] Patient ID '{patient_id}' already exists. Use a unique ID.")
        else:
            break

    # Personal Details
    full_name  = get_non_empty_string("  Full Name           : ")
    age        = get_positive_integer("  Age                 : ")
    gender     = get_valid_gender()
    diagnosis  = get_non_empty_string("  Diagnosis           : ")

    # Treatments (minimum 2)
    treatments = {}
    print("\n  --- Enter Treatments (minimum 2 required) ---")

    treatment_count = 1
    while True:
        print(f"\n  Treatment #{treatment_count}")
        t_name = get_non_empty_string("    Treatment Name  : ").title()

        # Prevent duplicate treatment names for the same patient
        if t_name in treatments:
            print(f"  [!] '{t_name}' already added. Use a different name.")
            continue

        t_cost = get_positive_float("    Cost (K)        : ")
        treatments[t_name] = t_cost
        treatment_count += 1

        # Enforce minimum of 2 treatments
        if treatment_count <= 2:
            print("  [i] At least one more treatment is required.")
            continue

        # After 2 treatments, let the user decide whether to add more
        more = input("\n  Add another treatment? (yes / no): ").strip().lower()
        if more not in ("yes", "y"):
            break

    # Save the Record
    patients[patient_id] = {
        "name"       : full_name,
        "age"        : age,
        "gender"     : gender,
        "diagnosis"  : diagnosis,
        "treatments" : treatments
    }

    print(f"\n  [✓] Patient '{full_name}' (ID: {patient_id}) added successfully.")
    display_separator("-")

# =============================================================================
#  2. VIEW ALL PATIENTS 
# =============================================================================

def view_all_patients():
    """Display a summary table of all patients."""
    display_header("All Patients")

    if not patients:
        print("  [i] No patient records found.")
        display_separator("-")
        return

    # Table header
    print(f"  {'Patient ID':<12} {'Full Name':<25} {'Diagnosis':<20} {'Total Bill':>12}")
    display_separator("-")

    for pid, info in patients.items():
        total = calculate_total_bill(pid)
        print(
            f"  {pid:<12} "
            f"{info['name']:<25} "
            f"{info['diagnosis']:<20} "
            f"{format_currency(total):>12}"
        )

    display_separator("-")
    print(f"  Total patients on record: {len(patients)}")
    display_separator("-")

# =============================================================================
#  3. VIEW PATIENT REPORT 
# =============================================================================

def view_patient_report():
    """Display a detailed billing report for a chosen patient."""
    display_header("Patient Report")

    if not patients:
        print("  [i] No patient records found.")
        display_separator("-")
        return

    patient_id = get_non_empty_string("  Enter Patient ID: ").upper()

    if not patient_exists(patient_id):
        print(f"  [!] Patient ID '{patient_id}' not found.")
        display_separator("-")
        return

    info = patients[patient_id]

    # Patient Details
    display_separator("-")
    print("  PATIENT DETAILS")
    display_separator("-")
    print(f"  Patient ID   : {patient_id}")
    print(f"  Full Name    : {info['name']}")
    print(f"  Age          : {info['age']} years")
    print(f"  Gender       : {info['gender']}")
    print(f"  Diagnosis    : {info['diagnosis']}")

    # Treatments & Costs
    display_separator("-")
    print("  TREATMENTS & COSTS")
    display_separator("-")
    print(f"  {'Treatment':<30} {'Cost':>12}")
    display_separator("-", 45)

    for treatment, cost in info["treatments"].items():
        print(f"  {treatment:<30} {format_currency(cost):>12}")

    display_separator("-", 45)

    total_bill = calculate_total_bill(patient_id)
    print(f"  {'TOTAL BILL':<30} {format_currency(total_bill):>12}")
    display_separator("-")

# =============================================================================
#  4. UPDATE PATIENT 
# =============================================================================

def update_patient():
    """Allow updates to diagnosis, treatments, or treatment costs."""
    display_header("Update Patient Record")

    if not patients:
        print("  [i] No patient records found.")
        display_separator("-")
        return

    patient_id = get_non_empty_string("  Enter Patient ID to update: ").upper()

    if not patient_exists(patient_id):
        print(f"  [!] Patient ID '{patient_id}' not found.")
        display_separator("-")
        return

    info = patients[patient_id]
    print(f"\n  Updating record for: {info['name']} (ID: {patient_id})")

    while True:
        print("\n  ── Update Options ──────────────────────────────")
        print("  1. Update Diagnosis")
        print("  2. Add New Treatment")
        print("  3. Update Treatment Cost")
        print("  4. Remove Treatment")
        print("  5. Back to Main Menu")
        display_separator("-")

        choice = input("  Select option (1-5): ").strip()

        # 4a. Update Diagnosis
        if choice == "1":
            print(f"\n  Current Diagnosis: {info['diagnosis']}")
            new_diag = get_non_empty_string("  New Diagnosis     : ")
            info["diagnosis"] = new_diag
            print(f"  [✓] Diagnosis updated to '{new_diag}'.")

        # 4b. Add New Treatment
        elif choice == "2":
            t_name = get_non_empty_string("\n  New Treatment Name : ").title()
            if t_name in info["treatments"]:
                print(f"  [!] Treatment '{t_name}' already exists for this patient.")
            else:
                t_cost = get_positive_float("  Cost (K)           : ")
                info["treatments"][t_name] = t_cost
                print(f"  [✓] Treatment '{t_name}' added at {format_currency(t_cost)}.")

        # 4c. Update Treatment Cost
        elif choice == "3":
            if not info["treatments"]:
                print("  [!] No treatments recorded for this patient.")
            else:
                print("\n  Current Treatments:")
                for idx, (t, c) in enumerate(info["treatments"].items(), start=1):
                    print(f"    {idx}. {t} — {format_currency(c)}")
                t_name = get_non_empty_string("\n  Treatment to update (exact name): ").title()
                if t_name not in info["treatments"]:
                    print(f"  [!] Treatment '{t_name}' not found.")
                else:
                    new_cost = get_positive_float(f"  New cost for '{t_name}' (K): ")
                    info["treatments"][t_name] = new_cost
                    print(f"  [✓] Cost updated to {format_currency(new_cost)}.")

        # 4d. Remove Treatment
        elif choice == "4":
            if not info["treatments"]:
                print("  [!] No treatments recorded for this patient.")
            else:
                print("\n  Current Treatments:")
                for t, c in info["treatments"].items():
                    print(f"    • {t} — {format_currency(c)}")

                t_name = get_non_empty_string("\n  Treatment to remove (exact name): ").title()
                if t_name not in info["treatments"]:
                    print(f"  [!] Treatment '{t_name}' not found.")
                else:
                    confirm = input(
                        f"  Are you sure you want to remove '{t_name}'? (yes / no): "
                    ).strip().lower()
                    if confirm in ("yes", "y"):
                        del info["treatments"][t_name]
                        print(f"  [✓] Treatment '{t_name}' removed.")
                    else:
                        print("  [i] Removal cancelled.")

        # Back
        elif choice == "5":
            break

        else:
            print("  [!] Invalid option. Please choose 1 – 5.")

    display_separator("-")

# =============================================================================
#  5. DELETE PATIENT 
# =============================================================================

def delete_patient():
    """Remove a patient record after confirmation."""
    display_header("Delete Patient")

    if not patients:
        print("  [i] No patient records found.")
        display_separator("-")
        return

    patient_id = get_non_empty_string("  Enter Patient ID to delete: ").upper()

    if not patient_exists(patient_id):
        print(f"  [!] Patient ID '{patient_id}' not found.")
        display_separator("-")
        return

    name = patients[patient_id]["name"]
    confirm = input(
        f"  Are you sure you want to permanently delete '{name}' (ID: {patient_id})? "
        "(yes / no): "
    ).strip().lower()

    if confirm in ("yes", "y"):
        del patients[patient_id]
        print(f"  [✓] Patient '{name}' (ID: {patient_id}) has been deleted.")
    else:
        print("  [i] Deletion cancelled. Record retained.")

    display_separator("-")

# =============================================================================
#  6. SEARCH PATIENT
# =============================================================================

def search_patient():
    """Search for patients by Patient ID or by name (partial match)."""
    display_header("Search Patient")

    if not patients:
        print("  [i] No patient records found.")
        display_separator("-")
        return

    print("  Search by:")
    print("  1. Patient ID")
    print("  2. Name")
    display_separator("-")
    choice = input("  Select option (1 or 2): ").strip()

    results = {}

    if choice == "1":
        # Search by exact Patient ID
        pid = get_non_empty_string("  Enter Patient ID: ").upper()
        if patient_exists(pid):
            results[pid] = patients[pid]
        else:
            print(f"  [!] No patient found with ID '{pid}'.")
            display_separator("-")
            return

    elif choice == "2":
        # Search by partial name (case-insensitive)
        keyword = get_non_empty_string("  Enter name (or part of name): ").lower()
        for pid, info in patients.items():
            if keyword in info["name"].lower():
                results[pid] = info

        if not results:
            print(f"  [!] No patients found matching '{keyword}'.")
            display_separator("-")
            return

    else:
        print("  [!] Invalid option.")
        display_separator("-")
        return

    # Display Results
    print(f"\n  {len(results)} result(s) found:\n")
    print(f"  {'Patient ID':<12} {'Full Name':<25} {'Age':<6} {'Gender':<10} {'Diagnosis':<20} {'Total Bill':>12}")
    display_separator("-")

    for pid, info in results.items():
        total = calculate_total_bill(pid)
        print(
            f"  {pid:<12} "
            f"{info['name']:<25} "
            f"{str(info['age']):<6} "
            f"{info['gender']:<10} "
            f"{info['diagnosis']:<20} "
            f"{format_currency(total):>12}"
        )

    display_separator("-")

# =============================================================================
#  7. HOSPITAL STATISTICS 
# =============================================================================

def hospital_statistics():
    """Display aggregate statistics for the hospital."""
    display_header("Hospital Statistics")

    if not patients:
        print("  [i] No patient records found. Statistics unavailable.")
        display_separator("-")
        return

    # Compute per-patient totals
    bills = {pid: calculate_total_bill(pid) for pid in patients}

    total_patients = len(patients)
    total_revenue   = sum(bills.values())

    # Highest and lowest bill
    highest_pid = max(bills, key=bills.get)
    lowest_pid  = min(bills, key=bills.get)

    # Diagnosis frequency
    diagnosis_count = {}
    for info in patients.values():
        diag = info["diagnosis"].title()
        diagnosis_count[diag] = diagnosis_count.get(diag, 0) + 1

    most_common_diag = max(diagnosis_count, key=diagnosis_count.get)

    # Gender distribution
    gender_count = {}
    for info in patients.values():
        g = info["gender"]
        gender_count[g] = gender_count.get(g, 0) + 1

    # Average bill
    average_bill = total_revenue / total_patients

    # Display
    display_separator("-")
    print("  GENERAL STATISTICS")
    display_separator("-")
    print(f"  Total Number of Patients   : {total_patients}")
    print(f"  Total Hospital Revenue     : {format_currency(total_revenue)}")
    print(f"  Average Patient Bill       : {format_currency(average_bill)}")

    display_separator("-")
    print("  BILLING EXTREMES")
    display_separator("-")
    print(
        f"  Highest Bill  : {patients[highest_pid]['name']:<25} "
        f"(ID: {highest_pid})  —  {format_currency(bills[highest_pid])}"
    )
    print(
        f"  Lowest  Bill  : {patients[lowest_pid]['name']:<25} "
        f"(ID: {lowest_pid})  —  {format_currency(bills[lowest_pid])}"
    )

    display_separator("-")
    print("  DIAGNOSIS FREQUENCY")
    display_separator("-")
    for diag, count in sorted(diagnosis_count.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {diag:<25} {bar}  ({count} patient{'s' if count > 1 else ''})")

    print(f"\n  Most Common Diagnosis      : {most_common_diag} ({diagnosis_count[most_common_diag]} case(s))")

    display_separator("-")
    print("  GENDER DISTRIBUTION")
    display_separator("-")
    for gender, count in gender_count.items():
        percentage = (count / total_patients) * 100
        print(f"  {gender:<10} : {count} patient{'s' if count > 1 else ''} ({percentage:.1f}%)")

    display_separator("-")

# =============================================================================
#  MAIN MENU
# =============================================================================

def display_menu():
    """Print the main navigation menu."""
    display_separator()
    print("           HOSPITAL MANAGEMENT SYSTEM")
    print("              TIM General Hospital")
    display_separator()
    print("  1. Add Patient")
    print("  2. View All Patients")
    print("  3. View Patient Report")
    print("  4. Update Patient")
    print("  5. Delete Patient")
    print("  6. Search Patient")
    print("  7. Hospital Statistics")
    print("  8. Exit")
    display_separator()

def main():
    """Entry point — continuous menu loop."""
    print("\n" + "=" * 65)
    print("   Welcome to the Hospital Management System")
    print("   TIM General Hospital — Patient Records")
    print("=" * 65)

    # Menu dispatch table
    menu_actions = {
        "1": add_patient,
        "2": view_all_patients,
        "3": view_patient_report,
        "4": update_patient,
        "5": delete_patient,
        "6": search_patient,
        "7": hospital_statistics,
    }

    while True:
        display_menu()
        choice = input("  Enter your choice (1-8): ").strip()

        if choice in menu_actions:
            print()
            menu_actions[choice]()
        elif choice == "8":
            display_separator()
            print("  Thank you for using the Hospital Management System.")
            print("  Goodbye!")
            display_separator()
            break
        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 8.\n")

# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()
