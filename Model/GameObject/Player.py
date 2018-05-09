class player(object):
    def __init__(self, name, index, is_AI):
        self.name = name
        self.is_AI = is_AI
        self.index = index
        self.ai = None
