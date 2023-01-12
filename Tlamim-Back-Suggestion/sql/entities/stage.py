class Stage(object):

    def __init__(self, stage_index: int, stage_name: str):
        self.index = stage_index
        self.name = stage_name

    def __str__(self):
        res = "({0}, {1})".format(self.index, f"\'{self.name}\'")
        return res
