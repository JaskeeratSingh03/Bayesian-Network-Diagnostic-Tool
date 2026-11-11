# AI Probabilistic Diagnostic Tool

This tool implements a Bayesian Network to diagnose equipment failure based on observed symptoms. Unlike traditional rule-based systems, it uses probability and information theory to identify root causes and recommend the most efficient diagnostic tests.

## Core Components

1. **Bayesian Network**: A Directed Acyclic Graph (DAG) representing the causal relationship:
   `Faults (Root Causes) -> Symptoms (Observable Effects) -> Diagnostic Tests (Evidence Gathering)`
2. **Probabilistic Inference**: Uses Bayes' Theorem to update the probability of faults (posterior) given observed evidence.
3. **Next-Best-Test**: Recommends tests that maximize Information Gain (Entropy Reduction).

## Comparison: Bayesian vs Rule-Based

| Feature | Bayesian Network | Rule-Based System |
|---|---|---|
| Uncertainty | Probabilistic (e.g., 80% chance) | Binary (True/False) |
| Missing Data | Uses priors to make best guesses | Often halts or fails |
| Scaling | Local updates to CPTs | Exponential rule growth |
| Cost | High data gathering (CPTs) | Faster initial logic translation |
