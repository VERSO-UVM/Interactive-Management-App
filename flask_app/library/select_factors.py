from typing import List as _List


## @author alyssa   # noqa: E266
## @see https://github.com/VERSO-UVM/interactive-management-app/issues/21
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
