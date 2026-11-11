import sys

def rule_based_diagnostic():
    print("\n--- Rule-Based (If-Then) Diagnostic System ---")
    print("This system uses strict logic. If a condition is not met, it may fail.")
    
    # Simple Rule-based logic
    boot = input("Device won't boot? (y/n): ").lower() == 'y'
    
    if boot:
        voltage = input("Voltage low? (y/n): ").lower() == 'y'
        if voltage:
            return "Dead Battery"
        
        beeping = input("Continuous beeping? (y/n): ").lower() == 'y'
        if beeping:
            return "Corrupted RAM"
        
        return "Fried Motherboard (by elimination)"
    else:
        return "Device is functioning normally"

def run_comparison():
    print("====================================================")
    print("BAYESIAN vs RULE-BASED SYSTEM COMPARISON")
    print("====================================================")
    
    print("\nScenario: Device won't boot, but voltage is NORMAL and there is NO beeping.")
    print("Rule-Based result: ", rule_based_diagnostic())
    
    print("\nObservation: The Rule-Based system simply 'guesses' Motherboard by elimination.")
    print("The Bayesian system would maintain a probability distribution (e.g., Motherboard 70%, RAM 20%, Battery 10%)")
    print("allowing the technician to see the uncertainty.")
    
    print("\nKey Advantages of Bayesian Approach:")
    print("1. Handling Uncertainty: Outputs probabilities, not just binary labels.")
    print("2. Graceful Degradation: Works with missing data using Prior probabilities.")
    print("3. Efficient Search: 'Next-Best-Test' reduces the number of steps needed to reach a conclusion.")
    print("====================================================")

if __name__ == "__main__":
    run_comparison()
