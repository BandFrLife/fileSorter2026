'''
Tag class
'''

__author__ = "Parker Stacy"


class Tag:
    '''
    Tag class
    '''
    def __init__(self) -> None:
        self._name: str = ""
        self._desc: str = ""

    def set_name(self, name: str) -> None:
        '''
        Setter method for name
        '''
        self._name = name

    def set_description(self, desc: str) -> None:
        '''
        Setter method for description
        '''
        self._desc = desc

    @property
    def name(self) -> str:
        '''
        Getter method for name
        '''
        return self._name

    @property
    def desc(self) -> str:
        '''
        Getter method for description
        '''
        return self._desc

    def __str__(self) -> str:
        return f"{self.name}"
