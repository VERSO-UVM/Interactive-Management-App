import uuid

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

    def __init__(self,
                 u_name: str,
                 f_name: str,
                 l_name: str,
                 email: str,
                 ):

        self.id = str(uuid.uuid4())
        self.u_name = u_name
        self.f_name = f_name
        self.l_name = l_name
        self.email = email

        self.haveVoted = []
        self.willVote = []

# Methods to get the person's name or the list of factors that have or will vote
    def addHaveVoted(self, newItem):
        self.haveVoted.append(newItem)

    def addWillVoted(self, newItem):
        self.willVote.append(newItem)

    def getName(self):
        return self.u_name

    def getVoted(self):
        return self.haveVoted

    def __repr__(self):
        return self.u_name + self.willVote + self.haveVoted + ""
