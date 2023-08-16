"""
Contain singleton design pattern code super class.
"""


class SingletonPattern:
    """
    Contain singleton design pattern code super class.
    """
    # Singleton instance flag:
    __singleton_instance: object or None = None
    # Singleton __init__ blocker callable function:
    __devnull_init: None = lambda self, *args, **kwargs: None

    def __new__(cls, *args, **kwargs) -> object:
        """
        Singleton design pattern class constructor part.
        Return Singleton instance.
        Blocking __init__ new instance dander method by callable function returning None.

        :result: Singleton instance.
        """
        if cls.__singleton_instance is None:
            try:
                cls.__singleton_instance: object = super(SingletonPattern, cls).__new__(cls)
            except TypeError:
                cls.__singleton_instance: object = super(SingletonPattern, cls).__new__(cls, *args, **kwargs)

        # Check default '__init__' value... is callable result None:
        elif cls.__dict__.get('__init__', None) is not cls.__devnull_init:
            cls.__init__: None = cls.__devnull_init

        return cls.__singleton_instance
