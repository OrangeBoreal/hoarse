# Hoarse
from hoarse.models.mixins import IDMixin


class Competitor(IDMixin):
    """
    Define the attributes of a competitor
    """
    def __init__(self, riderName, group, horseName=''):
        super().__init__()
        self.riderName = riderName
        self.horseName = horseName
        self.group = group

    @property
    def orderInGroup(self):
        #I think it is bugged.... since self.group is an int
        return self.group.competitors.index(self)


#define a class for groups of competitors ?
