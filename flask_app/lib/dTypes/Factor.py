import uuid
from flask_app.lib.dTypes.Idea import Idea as _Idea


# @author tasthana
class Factor:
    def __init__(self,
                 idea: _Idea,
                 description: str = None,
                 label: str = None):

        self.id = str(uuid.uuid4())
        self.idea = idea
        self.description = description
        self.label = label
