'''Function for factor voting-FDEOLIVE'''
import pandas as pd


# @author Fernanda
def votingFactor(factorList):
    "Column Name"
    "Lists to insert into the dataframe"
    listFrom = []
    listTo = []
    listRating = []

    "Essentially cross joins the factor list with itself, which allows for the bidirectional factor voting, and asks users for rating"
    for i in factorList:
        for j in factorList:
            if (i != j):
                keepGoing = True
                userRating = input(
                    f'Enter rating for factor:{i}\'s influence on factor:{j} :')
                '''Input validation'''
                while (keepGoing):
                    try:
                        value = int(userRating)
                        if (0 <= value <= 10):
                            listFrom.append(i)
                            listTo.append(j)
                            listRating.append(userRating)
                            keepGoing = False
                        else:
                            userRating = input(
                                f'Enter rating for factor:{i}\'s influence on factor:{j} :')
                    except:  # noqa: E722
                        userRating = input(
                            f'Enter rating for factor:{i}\'s influence on factor:{j} :')

    """Adds to the dataframe"""
    votingDataFrame = pd.DataFrame(
        {'From': listFrom, 'To': listTo, 'Rating': listRating})
    "For testing:"
    print(votingDataFrame)


def main():
    list = ['1', '2', '3']
    votingFactor(list)


main()
