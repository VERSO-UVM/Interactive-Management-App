## @author gracekinney
## Idea Voting Class

'''
The IdeaVoting class encapsulates information about an idea, allowing retrieval and modification of its title, category, number of votes, and percentage of votes. 
The __repr__ method provides a formatted string representation.
"'''
class IdeaVoting:

    # TODO waiting for category function from another card

    # custom constructor for IdeaVoting class
    def __init__(self, title, category, numVotes=0, percentVotes=0):
        # setting private fields
        self.__title = title
        self.__category = category
        self.__numVotes = numVotes
        self.__percentVotes = percentVotes

    # getters
    def getTitle(self):
        return self.__title

    def getCategory(self):
        return self.__category

    def getNumVotes(self):
        return self.__numVotes

    def getPercentVotes(self):
        return self.__percentVotes

    # setters
    def setTitle(self, newTitle):
        self.__title = newTitle

    def setCategory(self, newCatategory):
        self.__category = newCatategory

    def setNumVotes(self, newNumVotes):
        self.__numVotes = newNumVotes

    def setPercentVotes(self, newPercentVotes):
        self.__percentVotes = newPercentVotes

    def __repr__(self) -> str:
        return self.__title + ': ' + self.__percentVotes + '%'
