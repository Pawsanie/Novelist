"""
Contain state machine design pattern code super class.
"""


class StateMachinePattern:
    """
    Contain StateMachine design pattern code.
    StateMachine state objects must have "status" attribute.
    Use self.state() for execute state.
    """
    def __init__(self, collection: list[object]):
        """
        :param collection: List with StateMachine state objects.
        """
        self._collection: list = collection
        self.state = collection[0]
        self._index: int = 0

    def __next__(self) -> object:
        """
        Get next StateMachine state.
        """
        if self._index + 1 <= len(self._collection) - 1:
            self._index += 1
        else:
            self._index: int = 0
        return self._collection[self._index]

    def append(self, element: object):
        """
        Add new object to StateMachine collections end.
        :param element: State class object.
        """
        self._collection.append(element)

    def next_state(self):
        """
        Switch StateMachine state.
        """
        self.state: object = self.__next__()
