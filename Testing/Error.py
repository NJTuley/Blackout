

class Error(object):
    name = ""
    description = ""

    def __init__(self, name, desc):
        self.name = name
        self.description = desc

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description