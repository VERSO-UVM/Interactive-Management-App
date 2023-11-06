# @author James Catanzaro
# TODO: add proposer variable when completed
class idea ():
    def __init__(self, title: str, votes: int):
        self.title = title
        self.votes = votes

    def __repr__(self):
        return self.title + str(self.votes) + ""
