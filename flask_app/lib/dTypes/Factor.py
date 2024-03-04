import uuid


# @author tasthana
class Factor:
    def __init__(self,
                 title: str = None,
                ):

        self.id = str(uuid.uuid4())
        self.title = title
        