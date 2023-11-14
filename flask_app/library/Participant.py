
# Participant class
'''
The Python script defines two classes: Participant and Idea.
The Participant class represents individuals involved in a voting process, initializing with a name and two lists, haveVoted and willVote,
to track their voting history and intended votes.
The class includes methods to add items to these lists and retrieve the participant's name or voting records.
The __repr__ method outputs a string representation of the participant, including their name and voting information.
 The Idea class models ideas, initializing with a name and purpose.
 It offers methods to change the idea's name or purpose and retrieve these attributes.
 '''
# @author Fernanda


class Participant:

    def __init__(self, name):
        self.name = name
        self.haveVoted = []
        self.willVote = []

# Methods to get the person's name or the list of factors that have or will vote
    def addHaveVoted(self, newItem):
        self.haveVoted.append(newItem)

    def addWillVoted(self, newItem):
        self.willVote.append(newItem)

    def getName(self):
        return self.name

    def getVoted(self):
        return self.haveVoted

    def __repr__(self):
        return self.name + self.willVote + self.haveVoted + ""


# Class for an idea
class Idea:
    name = "None"
    purpose = "Main Purpose"

    def __init__(self, name, purpose):
        self.name = name
        self.purpose = purpose

    def chnageName(self, name):
        self.name = name

    def chnagePurpose(self, purpose):
        self.purpose = purpose

    def getPurpose(self):
        return self.purpose

    def getName(self):
        return self.name
