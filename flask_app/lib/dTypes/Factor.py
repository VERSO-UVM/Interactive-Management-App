from datetime import datetime
import uuid


# @author tasthana
class Factor:
    def __init__(self,
                 idea,
                 clarification,
                 label,
                 category):
        self.id = str(uuid.uuid4())
        self.idea = idea
        self.clarification = clarification
        self.label = label
        self.category = category
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
