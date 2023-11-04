## @author alyssa   # noqa: E266

"""
Select from a list of factors
https://github.com/VERSO-UVM/interactive-management-app/issues/21
"""

from typing import List as _List


def select_factors(factors: _List[str]) -> _List[str]:

    option: str = '0'
    keepers: _List[str] = []
    for i in factors:
        print(i)
        while not (option == 'y' or option == 'n'):
            option = input("Keep? y/n: ").lower()
        if option == 'y':
            keepers.append(i)
    
    return keepers
