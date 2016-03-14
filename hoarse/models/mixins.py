from itertools import count


class IDMixin(object):

    def __init__(self, *args, **kwargs):
        self.id = self.get_next_id()
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return self.id

    @classmethod
    def get_next_id(cls):
        if not getattr(cls, "idCounter", None):
            cls.idCounter = count()

        return next(cls.idCounter)
