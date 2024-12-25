from abc import ABC, abstractmethod
from datetime import datetime
from xml.etree.ElementTree import Element

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

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


class MarketConfig(MarketAspect, ABC):
    def __init__(self, draft=0, initial_purse=0, ante=0, buy_char=0, sell_char=None, banish_char=0):
        self.draft = if_none_then_default(draft, 3)
        self.initial_purse = if_none_then_default(initial_purse, 3)
        self.ante = if_none_then_default(ante, 1)
        self.buy_char = if_none_then_default(buy_char, 3)
        self.sell_char = sell_char
        self.banish_char = if_none_then_default(banish_char, 5)

    def __eq__(self, other):
        return self.draft == other.draft and self.initial_purse == other.initial_purse and self.ante == other.ante and \
            self.banish_char == other.banish_char and self.sell_char == other.sell_char and \
            self.buy_char == other.buy_char

    def __str__(self):
        sell_part = " Sell characters for {} coin{},".format(self.sell_char, is_plural(
            self.sell_char)) if self.sell_char is not None else ""
        return ("Game configuration: Draft {} character{}, Start with {} coin{}, Game ante is {}, Buy characters "
                "for {} coin{},{} Banish characters for {} coin{}").format(self.draft, is_plural(self.draft),
                                                                           self.initial_purse,
                                                                           is_plural(self.initial_purse), self.ante,
                                                                           is_plural(self.ante), self.buy_char,
                                                                           is_plural(self.buy_char), sell_part,
                                                                           self.banish_char,
                                                                           is_plural(self.banish_char))

class MarketGameParticipant(MarketAspect, ABC):
    def __init__(self, player=None, character=None):
        self.player = player
        self.character = character

    def __eq__(self, other):
        return self.player == other.player and self.character == other.character

    def __str__(self):
        return "Participant {} used {}".format(self.player, self.character)

class MarketGame(MarketAspect, ABC):
    def __init__(self, date=datetime.now(), participants=None):
        self.participants = if_none_then_default(participants, list())
        self.date = date
