##Idea Voting Class
class IdeaVoting:
    # default values
    title = "None"
    category = "None"
    numVotes = 0
    percentVotes = 0

    # OR DO WE WANT A DEFAULT CONSTRUCTOR

    # custom constructor for IdeaVoting class
    def __init__(self, title, category, numVotes, percentVotes):
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

    def setCategory(self, newCat):
        self.__category = newCat

    def setNumVotes(self, newNumVotes):
        self.__numVotes = newNumVotes

    def setPercentVotes(self, newPercentVotes):
        self.__percentVotes = newPercentVotes