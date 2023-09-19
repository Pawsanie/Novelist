"""
Contain state machine design pattern code super class.
"""


class StateMachinePattern:
    """
    Contain StateMachine design pattern code.
    StateMachine state objects must have "status" parameter.
    """
    def __init__(self, collection: list[object]):
        """
        :param collection: List with StateMachine state objects.
        :type collection: list[object]
        """
        self.collection: list = collection
        self.state = collection[0]
        self.index: int = 0

    def __next__(self) -> object:
        """
        Get next StateMachine state.
        """
        if self.index + 1 <= len(self.collection) - 1:
            self.index += 1
        else:
            self.index: int = 0
        return self.collection[self.index]

    def append(self, element: object):
        """
        Add new object to StateMachine collections end.
        :param element: State class object.
        :type element: object
        """
        self.collection.append(element)

    def next_state(self):
        """
        Switch StateMachine state.
        """
        self.state: object = self.__next__()
