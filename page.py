class Page:
    idx = 0

    def __init__(self, *modules):
        self.modules = modules

    def lines(self, num):
        start = self.idx
        end = start+num

        ret = []
        for mod in self.modules:
            ret.extend(mod.lines())

        if len(ret) > end:
            self.idx += 1
        else:
            self.idx = 0

        return ret[start:end]
