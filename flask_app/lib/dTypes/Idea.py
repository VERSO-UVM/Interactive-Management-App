# @author James Catanzaro

"""
idea.py

This Python script defines a simple class 'Idea' representing an idea with a title and a vote count.
The class includes an initializer (__init__) and a representation method (__repr__) for easy display and debugging.

@author: James Catanzaro

Classes:
    Idea:
        Represents an idea with a title and a vote count.

        Methods:
            __init__(self, title: str, votes: int):
                Initializes an Idea object with the specified title and vote count.

                Parameters:
                    title (str): The title of the idea.
                    votes (int): The initial vote count for the idea.

            __repr__(self):
                Returns a string representation of the Idea object for easy display and debugging.

Attributes:
    title (str): The title of the idea.
    votes (int): The vote count associated with the idea.

Usage:
    To use this script, import the 'Idea' class into your Python code and create instances of the 'Idea' class as needed.

"""


class Idea():
    def __init__(self,
                 title: str,
                 votes: int):

        self.title = title
        self.votes = votes

    def __repr__(self):
        return self.title + str(self.votes) + ""
