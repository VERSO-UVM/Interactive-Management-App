"""
Created on Thu Nov  2 14:19:56 2023
​
@author: jmeluso
"""
​
import numpy as np
import pandas as pd
​
​
def structure_matrix(A):
    """
    This function that takes a square boolean numpy array as input and returns
    a dictionary of the levels and lists of indices for those levels.
​
    Parameters:
    A (numpy.ndarray): A 2-dimensional numpy array
​
    Returns:
    dict: a dictionary with keys as levels and values as indices (indexed from
    0) returned in lists
​
    Example :
    >>> import numpy as np
    >>> A = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]], dtype=bool)
    >>> structure_matrix(A)
    {1: [0], 2: [1], 3: [2, 5], 4: [3], 5: [4]}
    """
​
    # Check if A is a square matrix
    if len(A) != len(A[0]):
        raise "Error: The input matrix is not square."
​
    # Construct reachability matrix
    M = create_reachability_matrix(A)
​
    # Structure reachability matrix
    level2indices = find_levels(M)
​
    # Return the levels and indices
    return level2indices
​
​
def create_reachability_matrix(A):
    """
    This function takes a 2-dimensional numpy array A as input and returns a
    reachability matrix M. Matrix A consists of elements a_ij where the rows i
    correspond to the source nodes and the columns j correspond to the
    destination nodes. All entries indexed from 0.
​
    Parameters:
    A (numpy.ndarray): A 2-dimensional numpy array
​
    Returns:
    numpy.ndarray: A reachability matrix M
​
    Raises:
    RuntimeError: If the matrix does not converge within 1000 iterations
​
    Example:
    >>> import numpy as np
    >>> A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    >>> create_reachability_matrix(A)
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]])
    """
​
    # Sum A with identity matrix I
    n = len(A)
    I = np.eye(n, dtype=bool)
    M = A + I
​
    # Take M to successive powers until (A+I)^n = (A+I)^(n+1)
    MAX_ITERATIONS = 100
    ii = 0
    while ii < MAX_ITERATIONS:
        ii += 1
        M2 = np.matmul(M, M)
        if np.array_equal(M2, M):
            break
        M = M2
​
    # Return an error message if the matrix does not converge w/i 100 iters
    if not np.array_equal(M, M2):
        raise RuntimeError("The matrix did not converge within "
                           + "{MAX_ITERATIONS} iterations.")
​
    # Otherwise, return reachability matrix M
    return M
​
​
def find_levels(M):
    """
    This function takes a 2-dimensional numpy array M as input and returns a
    dictionary level2indices with keys as levels and values as lists of
    indices corresponding to that level. Entries are indexed from 0, except
    levels which are indexed from 1.
​
    Parameters:
    M (numpy.ndarray): A 2-dimensional numpy array
​
    Returns:
    dict: A dictionary level2indices
​
    Example:
    >>> import numpy as np
    >>> M = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1]])
    >>> find_levels(M)
    {1: [0], 2: [1], 3: [2]}
    """
​
    # Convert the matrix to a pandas dataframe
    df = pd.DataFrame(M)
​
    # Create dictionaries index2reachable, index2antecedents, and intersection
    index2reachable, index2antecedents, intersection = get_matrix_sets(df)
​
    # Create dictionary level2indices
    level2indices = {}
​
    # Iteratively find level2indices levels
    kk = 1
    while intersection:
​
        # Add an empty entry to level2indices
        level2indices[kk] = []
​
        # Check entries that repeat (antecedents = intersections)
        for ii in intersection:
            if index2antecedents[ii] == intersection[ii]:
                for ss in index2antecedents[ii]:
                    if ss not in level2indices[kk]:
                        level2indices[kk].append(ss)
​
        # Remove row and column from M
        df = df.drop(level2indices[kk], axis=0)
        df = df.drop(level2indices[kk], axis=1)
​
        # Increment index
        kk += 1
​
        # Recreate dicts index2reachable, index2antecedents, and intersection
        index2reachable, index2antecedents, intersection = get_matrix_sets(df)
​
    return level2indices
​
​
def get_matrix_sets(df):
    """
    This function takes a pandas dataframe df as input and returns three
    dictionaries: ind2reach, ind2antec, and intx.
​
    Parameters:
    df (pandas.DataFrame): A pandas dataframe
​
    Returns:
    tuple: A tuple of three dictionaries: ind2reach, ind2antec, and intx
​
    Example:
    >>> import pandas as pd
    >>> df = pd.DataFrame({0: [1, 0, 0], 1: [0, 1, 1], 2: [1, 0, 1]})
    >>> get_matrix_sets(df)
    ({0: [0, 2], 1: [1], 2: [1, 2]},
     {0: [0], 1: [1, 2], 2: [0, 2]},
     {0: [0], 1: [1], 2: [2]})
    """
​
    # Create dictionaries index2reachable, index2antecedents, and intersection
    ind2reach = {ii: list(df.columns[(df.iloc[ii, :] == 1).values])
                 for ii in range(len(df))}
    ind2antec = {jj: list(df.index[(df.iloc[:, jj] == 1).values])
                 for jj in range(len(df.columns))}
    intx = {ii: list(set(ind2reach[ii]) & set(ind2antec[ii]))
            for ii in range(len(df))}
​
    # Return dictionaries
    return ind2reach, ind2antec, intx
​
​
if __name__ == '__main__':
​
    # Test the function with different matrices
    A1 = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]], dtype=bool)
    A2 = np.array([
        [1, 0, 0],
        [0, 1, 1],
        [0, 1, 1]], dtype=bool)
    A3 = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]], dtype=bool)
    A4 = np.array([
        [1, 0, 1, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0]], dtype=bool)
    A5 = np.array([
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0]], dtype=bool)
    A6 = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0]], dtype=bool)
    A7 = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]], dtype=bool)
    A8 = np.array([
        [1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1]], dtype=bool)
​
    # Print the level2indices test results
    print(structure_matrix(A1))
    print(structure_matrix(A2))
    print(structure_matrix(A3))
    print(f"{structure_matrix(A4)} (Malone, 1975 example)")
    print(structure_matrix(A5))
    print(structure_matrix(A6))
    print(structure_matrix(A7))
    print(f"{structure_matrix(A8)} (Warfield, 1974 example)")
