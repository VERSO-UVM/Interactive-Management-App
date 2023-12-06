from typing import List as _List


# @author alyssa   # noqa: E266
# @see https://github.com/VERSO-UVM/interactive-management-app/issues/21
'''
The Python script defines a function select_factors designed for use in a command-line interface (CLI).
The function takes a list of factors as input and iterates through each element, prompting the user to decide whether to keep each factor.
The user is presented with a list of factors in uppercase and asked to input 'y' (yes) or 'n' (no) for each factor.
The function then returns a list containing only the factors that the user chose to keep.
Additionally, there is a test function __test() that demonstrates the usage of select_factors with a sample list of factors

'''


def select_factors(factors: _List[str]) -> _List[str]:
    """
    Select from a list of factors
    Use with CLI only
    """

    option: str = '0'
    keepers: _List[str] = []
    for i in factors:
        print(i.upper(), end=" | ")
        option = input("Keep? y/n: ").lower()
        while option != 'y' and option != 'n':
            option = input("Keep? y/n: ").lower()
        if option == 'y':
            keepers.append(i)

    return keepers


def __test():
    test_data = ['Community', 'Consistency', 'Speediness']
    print(select_factors(test_data))


if __name__ == '__main__':
    __test()
