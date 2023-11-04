## @author alyssa   # noqa: E266

"""
Select from a list of factors
https://github.com/VERSO-UVM/interactive-management-app/issues/21
"""

from typing import List as _List


def select_factors(factors: _List[str]) -> _List[str]:
    """
    User manually prunes a large list of factors to a list of factors they want
    For use with CLI
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
