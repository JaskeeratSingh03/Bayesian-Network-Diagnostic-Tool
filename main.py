from src.engine import setup_laptop_network

def main():
    net = setup_laptop_network()
    faults = ["Dead Battery", "Fried Motherboard", "Corrupted RAM"]
    symptoms = ["Won't Boot", "Screen Flickers", "Beeping"]
    tests = ["Voltage Check", "RAM Swap Test"]

    print("--- AI Diagnostic Tool: Laptop Edition ---")
    print("Welcome, technician. I will help you identify the root cause using probability.")
    
    while True:
        print("\n--- Current Probabilities ---")
        for f in faults:
            print(f"{f}: {net.get_posterior(f):.2%}")

        print("\nWhat would you like to do?")
        print("1. Add Symptom Observation")
        print("2. Perform Diagnostic Test")
        print("3. Exit")
        
        choice = input("\nChoice: ")
        
        if choice == "1":
            print("\nAvailable Symptoms:")
            for i, s in enumerate(symptoms):
                print(f"{i+1}. {s}")
            s_idx = int(input("Select symptom number: ")) - 1
            s_name = symptoms[s_idx]
            obs = input(f"Is '{s_name}' present? (y/n): ").lower() == 'y'
            net.set_evidence(s_name, obs)
            
        elif choice == "2":
            best_test = net.recommend_next_test(tests, faults)
            if not best_test:
                print("\nNo further tests recommended. Root cause should be evident.")
                continue
            
            print(f"\nRecommended Next-Best-Test: {best_test}")
            obs = input(f"Result of {best_test} - Positive? (y/n): ").lower() == 'y'
            net.set_evidence(best_test, obs)
            
        elif choice == "3":
            print("Exiting diagnostic tool. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
