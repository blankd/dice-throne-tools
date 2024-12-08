from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element


def are_all_in_collection(checking, expected):
    if not isinstance(checking, (set, list, tuple) or not isinstance(expected, (set, list, tuple))):
        return False

    for e in expected:
        if e not in checking:
            return False
    return True


def if_none_then_default(what, default=None):
    return default if what is None else what


def is_plural(maybe_num):
    if isinstance(maybe_num, (set, list, tuple)):
        return '' if len(maybe_num) == 1 else 's'
    return '' if maybe_num == 1 else 's'


def is_str_valid(the_str) -> bool:
    return the_str is not None and isinstance(the_str, str) and len(the_str.strip()) > 0


class MarketAspect(ABC):
    @abstractmethod
    def read_from(self, **kwargs):
        pass

    @abstractmethod
    def write_to(self, **kwargs) -> Element:
        pass


class MarketPlayer(MarketAspect, ABC):
    def __init__(self, player_name=None, purse=0, characters=None, banished=None):
        self.player_name = player_name
        self.purse = purse
        self.characters = if_none_then_default(characters, list())
        self.banished = if_none_then_default(banished, list())

    def __eq__(self, other):
        return self.player_name == other.player_name and self.purse == other.purse and are_all_in_collection(
            self.characters, other.characters) and are_all_in_collection(self.banished, other.banished)

    def __str__(self):
        return "Player {} has {} coin{} has character{}: {} and banished: {}".format(self.player_name, self.purse,
                                                                                     is_plural(self.purse),
                                                                                     is_plural(self.characters),
                                                                                     ", ".join(self.characters),
                                                                                     ", ".join(self.banished))
