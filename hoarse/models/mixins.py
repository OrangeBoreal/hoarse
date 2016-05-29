# Standard Library
from itertools import count


class IDMixin(object):

    def __init__(self, *args, **kwargs):
        self.id = self.get_next_id()
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return self.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __gt__(self, other):
        return self.id > other.id

    @classmethod
    def get_next_id(cls):
        if not getattr(cls, "idCounter", None):
            cls.idCounter = count(1)

        return next(cls.idCounter)
