import uuid


# @author tasthana
class Factor:
    def __init__(self,
                 title: str = None,
                 description: str = None,
                 label: str = None):

        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.label = label
        self.votes = 0
