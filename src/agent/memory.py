from collections import deque


class ActivityMemory:

    def __init__(self):

        self.history = deque(maxlen=50)

    def add(self, state):

        self.history.append(state)

    def get_recent(self):

        return list(self.history)