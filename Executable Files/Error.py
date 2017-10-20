
class Error(Exception):
    name = ""
    description = ""

    def __init__(self, name, description):
        super(Error, self).__init__(description)
        self.name = name
        self.description = description

    def __str__(self):
        return str("Error: " + self.name + " - ", self.description + "\n")