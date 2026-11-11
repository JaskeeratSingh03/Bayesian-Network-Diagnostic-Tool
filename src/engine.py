from typing import Dict, List, Set, Tuple
import math

class BayesianNode:
    """Represents a node in the Bayesian Network."""
    def __init__(self, name: str, prior: float = None):
        self.name = name
        self.prior = prior  # P(Node=True)
        self.parents: List['BayesianNode'] = []
        # CPT: Mapping from tuple of parent states to P(Node=True | parents)
        # Example: {(True, False): 0.8} means if parent1 is True and parent2 is False, prob is 0.8
        self.cpt: Dict[Tuple[bool, ...], float] = {}

    def set_cpt(self, probabilities: Dict[Tuple[bool, ...], float]):
        self.cpt = probabilities

    def get_probability(self, parent_states: Tuple[bool, ...]) -> float:
        if not self.parents:
            return self.prior
        return self.cpt.get(parent_states, 0.01)  # Small epsilon for unseen states

class DiagnosticNetwork:
    """Manages the Bayesian Network and performs inference."""
    def __init__(self):
        self.nodes: Dict[str, BayesianNode] = {}
        self.evidence: Dict[str, bool] = {}

    def add_node(self, node: BayesianNode):
        self.nodes[node.name] = node

    def add_edge(self, parent_name: str, child_name: str):
        parent = self.nodes[parent_name]
        child = self.nodes[child_name]
        child.parents.append(parent)

    def set_evidence(self, node_name: str, state: bool):
        self.evidence[node_name] = state

    def get_posterior(self, fault_name: str) -> float:
        """
        Simplified exact inference for small networks.
        Calculates P(Fault | Evidence) = P(Evidence | Fault) * P(Fault) / P(Evidence)
        """
        fault = self.nodes[fault_name]
        
        # P(Fault = True | Evidence)
        p_fault_true = fault.prior
        p_evidence_given_true = 1.0
        
        # P(Fault = False | Evidence)
        p_fault_false = 1.0 - fault.prior
        p_evidence_given_false = 1.0
        
        # Calculate likelihood of evidence given fault state
        # For this prototype, we assume symptoms are conditionally independent given the fault
        for node_name, state in self.evidence.items():
            node = self.nodes[node_name]
            if fault in node.parents:
                # P(Symptom | Fault)
                prob_true = node.get_probability((True,)) if len(node.parents) == 1 else 0.5
                # P(Symptom | ~Fault)
                prob_false = node.get_probability((False,)) if len(node.parents) == 1 else 0.05
                
                if state:
                    p_evidence_given_true *= prob_true
                    p_evidence_given_false *= prob_false
                else:
                    p_evidence_given_true *= (1 - prob_true)
                    p_evidence_given_false *= (1 - prob_false)

        numerator = p_evidence_given_true * p_fault_true
        denominator = (p_evidence_given_true * p_fault_true) + (p_evidence_given_false * p_fault_false)
        
        return numerator / denominator if denominator > 0 else fault.prior

    def calculate_entropy(self, fault_probs: List[float]) -> float:
        """Calculates the Shannon entropy of the current fault distribution."""
        entropy = 0
        for p in fault_probs:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def recommend_next_test(self, test_nodes: List[str], fault_nodes: List[str]) -> str:
        """
        Recommends the test that minimizes the expected entropy of the fault distribution.
        This is the 'Next-Best-Test' feature based on Information Gain.
        """
        current_probs = [self.get_posterior(f) for f in fault_nodes]
        current_entropy = self.calculate_entropy(current_probs)

        best_test = None
        max_info_gain = -1.0

        for test_name in test_nodes:
            if test_name in self.evidence:
                continue

            # We simulate the outcome of the test (True or False)
            # P(Test=True | Evidence)
            # For simplicity, we use the law of total probability over faults
            p_test_true = 0
            for f in fault_nodes:
                f_prob = self.get_posterior(f)
                test_node = self.nodes[test_name]
                p_test_given_f = test_node.get_probability((True,)) if self.nodes[f] in test_node.parents else 0.5
                p_test_true += p_test_given_f * f_prob

            # Calculate expected entropy after observing Test=True
            probs_if_true = []
            for f in fault_nodes:
                f_prob = self.get_posterior(f)
                test_node = self.nodes[test_name]
                p_test_given_f = test_node.get_probability((True,)) if self.nodes[f] in test_node.parents else 0.5

                # Update prob using Bayes: P(F|T) = P(T|F)P(F) / P(T)
                p_f_given_true = (p_test_given_f * f_prob) / p_test_true if p_test_true > 0 else f_prob
                probs_if_true.append(p_f_given_true)

            # Calculate expected entropy after observing Test=False
            probs_if_false = []
            p_test_false = 1.0 - p_test_true
            for f in fault_nodes:
                f_prob = self.get_posterior(f)
                test_node = self.nodes[test_name]
                p_test_given_f = test_node.get_probability((True,)) if self.nodes[f] in test_node.parents else 0.5

                # P(F|~T) = P(~T|F)P(F) / P(~T)
                p_f_given_false = ((1 - p_test_given_f) * f_prob) / p_test_false if p_test_false > 0 else f_prob
                probs_if_false.append(p_f_given_false)

            expected_entropy = (p_test_true * self.calculate_entropy(probs_if_true)) + \
                               (p_test_false * self.calculate_entropy(probs_if_false))

            info_gain = current_entropy - expected_entropy
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                best_test = test_name

        return best_test

def setup_laptop_network() -> DiagnosticNetwork:
    """
    Designs the Bayesian Network for a Laptop.
    Faults: Dead Battery, Fried Motherboard, Corrupted RAM
    Symptoms: Won't Boot, Screen Flickers, Beeping
    Tests: Voltage Check, RAM Swap
    """
    net = DiagnosticNetwork()
    
    # --- Fault Nodes (Priors) ---
    dead_battery = BayesianNode("Dead Battery", prior=0.15)
    fried_mobo = BayesianNode("Fried Motherboard", prior=0.05)
    corrupt_ram = BayesianNode("Corrupted RAM", prior=0.10)
    
    for n in [dead_battery, fried_mobo, corrupt_ram]:
        net.add_node(n)
        
    # --- Symptom Nodes ---
    wont_boot = BayesianNode("Won't Boot")
    screen_flicker = BayesianNode("Screen Flickers")
    beeping = BayesianNode("Beeping")
    
    # CPTs for 'Won't Boot'
    # P(Won't Boot | Battery, Mobo, RAM) - simplified to most likely cause for the prototype
    wont_boot.set_cpt({
        (True,): 0.95, # Battery
        (False,): 0.10
    })
    
    # P(Screen Flicker | Mobo)
    screen_flicker.set_cpt({
        (True,): 0.80,
        (False,): 0.05
    })
    
    # P(Beeping | RAM)
    beeping.set_cpt({
        (True,): 0.90,
        (False,): 0.02
    })
    
    for n in [wont_boot, screen_flicker, beeping]:
        net.add_node(n)
        
    # Edges
    net.add_edge("Dead Battery", "Won't Boot")
    net.add_edge("Fried Motherboard", "Won't Boot")
    net.add_edge("Fried Motherboard", "Screen Flickers")
    net.add_edge("Corrupted RAM", "Beeping")
    
    # --- Test Nodes ---
    voltage_test = BayesianNode("Voltage Check")
    voltage_test.set_cpt({(True,): 0.99, (False,): 0.01}) # Very reliable for battery
    
    ram_swap_test = BayesianNode("RAM Swap Test")
    ram_swap_test.set_cpt({(True,): 0.95, (False,): 0.05}) # Very reliable for RAM
    
    for n in [voltage_test, ram_swap_test]:
        net.add_node(n)
        
    net.add_edge("Dead Battery", "Voltage Check")
    net.add_edge("Corrupted RAM", "RAM Swap Test")
    
    return net
