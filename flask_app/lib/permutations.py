# @author tasthana

# List of Factor Permutations
factor_permutations = [
    ('Factor1', 'Factor2'),
    ('Factor1', 'Factor3'),
    ('Factor2', 'Factor3'),
    # Add more factor permutations as needed
]

# Dictionary to store Factor Permutations with Weights
factor_weights = {
    ('Factor1', 'Factor2'): 0.75,
    ('Factor1', 'Factor3'): 0.60,
    ('Factor2', 'Factor3'): 0.90,
    # Add more factor permutations with weights as needed
}

# Calculate Average Factor Permutation and Weights
average_factor_weights = {}
for permutation, weight in factor_weights.items():
    factors = permutation
    # Assuming equal weightage for each permutation
    average_weight = weight / len(factor_permutations)
    average_factor_weights[factors] = average_weight

# Print the data structures
print("List of Factor Permutations:", factor_permutations)
print("List of Factor Permutations with Weights:", factor_weights)
print("List of Average Factor Permutation and Weights:", average_factor_weights)
