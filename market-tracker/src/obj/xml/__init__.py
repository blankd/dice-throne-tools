from datetime import datetime
from enum import Enum
from obj import MarketPlayer, is_plural, is_str_valid, MarketConfig, if_none_then_default, MarketGameParticipant, \
    MarketGame, DATE_FORMAT, parse_datetime, MarketAspect
from xml.etree.ElementTree import parse, Element, SubElement, fromstring, tostring

from obj.xml.errors import NotXML, WrongXMLElement, MissingAttribute


class XmlElements(Enum):
    ACTIONS = "actions"
    ACTION = "action"
    BANISH = "banish"
    BANISHED = "banished"
    BUY = "buy"
    CHARACTER = "character"
    CHARACTERS = "characters"
    CONFIG = "config"
    DOUBLE_KO = "doubleKo"
    FIRST_LOSER = "firstLoser"
    GAME = 'game'
    GAMES = 'games'
    GAME_ANTE = "ante"
    INITIAL_DRAFT = "draft"
    LOSER = "loser"
    LOSERS = "losers"
    MARKET = 'market'
    NAME = 'name'
    PARTICIPANTS = 'participants'
    PAYOUT = "payout"
    PLAYER = "player"
    PLAYERS = "players"
    PURSE = "purse"
    RESULTS = "results"
    SECOND_LOSER = "secondLoser"
    SELL = "sell"
    SINGLE_KO = "singleKo"
    START_COINS = "start"
    SURVIVOR = "survivor"
    TRIPLE_KO = "tripleKo"
    WINNER = "winner"


class XmlAttributes(Enum):
    BANISH = "banish"
    BANISH_LOSER = "loserBanish"
    BANISH_WINNER = "winnerBanish"
    DATE = "date"
    PLAYER = "player"


def add_aspect_sub_elements(parent: Element, kids: MarketAspect | set[MarketAspect] | list[MarketAspect] | tuple[
    MarketAspect]) -> Element | None:
    if parent is not None and kids is not None:
        if is_iterable(kids):
            for kid in kids:
                parent.append(kid.write_to())
        else:
            parent.append(kids.write_to())
    return parent


def get_enum_value(what) -> str:
    try:
        return what.value
    except AttributeError:
        return what


def is_iterable(what) -> bool:
    return what is not None and isinstance(what, (set, tuple, list))


def add_sub_elements(parent: Element, sub_elems, sub_attrs=None):
    for sub_elem, value in sub_elems.items():
        try:
            if isinstance(value, dict):
                add_sub_elements(SubElement(parent, sub_elem.value), value, sub_attrs)
            elif is_iterable(value):
                for val in value:
                    if isinstance(val, dict):
                        add_sub_elements(SubElement(parent, sub_elem.value), val, sub_attrs)
                    else:
                        SubElement(parent, sub_elem.value).text = str(val)
            else:
                SubElement(parent, sub_elem.value).text = str(value)
        except AttributeError:
            if isinstance(value, dict):
                add_sub_elements(SubElement(parent, sub_elem), value, sub_attrs)
            elif is_iterable(value):
                for val in value:
                    if isinstance(val, dict):
                        add_sub_elements(SubElement(parent, sub_elem), val, sub_attrs)
                    else:
                        SubElement(parent, sub_elem).text = str(val)
            else:
                SubElement(parent, sub_elem).text = str(value)


def follow_xpath(xml, *the_path):
    ret = None
    for i in range(0, len(the_path)):
        try:
            ret = xml.find('./{}'.format('/'.join(map(lambda p: p.value, the_path[i:]))))
        except AttributeError:
            ret = xml.find('./{}'.format('/'.join(the_path[i:])))
        if ret is not None:
            return ret
    return ret


def get_attribute_else_raise(xml: Element, attrib) -> str:
    try:
        return xml.attrib[attrib]
    except KeyError:
        raise MissingAttribute(missing_attrib=attrib, tag=xml.tag)


def get_element_text_else_raise(xml: Element, expected_tag, no_xml_msg=None) -> str:
    try:
        if xml is not None and xml.tag == expected_tag:
            return xml.text
        else:
            raise WrongXMLElement(got_tag=xml.tag if xml is not None else "Unknown", expected_tag=expected_tag)
    except AttributeError:
        if is_str_valid(no_xml_msg):
            raise NotXML(no_xml_msg)
        else:
            raise NotXML(f"Was expecting an Element, got {type(xml)}")


def make_list_from(found, **kwargs):
    if 'the_path' in kwargs:
        the_path = kwargs['the_path']
        found = found.findall('./{}'.format('/'.join(the_path)) if isinstance(the_path, list) else the_path)
    attrib = kwargs['attrib'] if 'attrib' in kwargs else None
    return [item.attrib[attrib] if attrib is not None else item.text for item in found]


def map_to_subelement_text(xml, sub_map):
    for key, value in sub_map.items():
        SubElement(xml, key).text = str(value)
    return xml


def parse_xml_if_str(what) -> Element:
    if isinstance(what, str):
        return fromstring(what)
    return what


class MarketPlayerXML(MarketPlayer):
    def __init__(self, player_name=None, purse=0, characters=None, banished=None, xml=None):
        super().__init__(player_name, purse, characters, banished)
        if xml is not None:
            self.read_from(parse_xml_if_str(xml))

    def read_from(self, xml):
        try:
            if xml is not None and xml.tag == XmlElements.PLAYER.value:
                self.player_name = xml.find(XmlElements.NAME.value).text
                self.purse = int(xml.find(XmlElements.PURSE.value).text)
                self.characters = make_list_from(found=xml,
                                                 the_path=[XmlElements.CHARACTERS.value, XmlElements.CHARACTER.value])
                self.banished = make_list_from(found=xml,
                                               the_path=f"./{XmlElements.BANISHED.value}/{XmlElements.CHARACTER.value}")
            else:
                raise WrongXMLElement(got_tag=xml.tag if xml is not None else "Unknown",
                                      expected_tag=XmlElements.PLAYER.value)
        except AttributeError:
            raise NotXML(f"Was expecting an Element, got {type(xml)}")

    def write_to(self) -> Element:
        subs = {
            XmlElements.NAME: self.player_name,
            XmlElements.PURSE: self.purse,
            XmlElements.CHARACTERS: {XmlElements.CHARACTER.value: self.characters},
            XmlElements.BANISHED: {XmlElements.CHARACTER.value: self.banished}
        }
        player = Element(XmlElements.PLAYER.value)
        add_sub_elements(player, subs)
        return player


class MarketConfigXML(MarketConfig):
    def __init__(self, draft=0, initial_purse=0, ante=0, buy_char=0, sell_char=None, banish_char=0, xml=None):
        super().__init__(draft=draft, initial_purse=initial_purse, ante=ante, buy_char=buy_char, sell_char=sell_char,
                         banish_char=banish_char)
        if xml is not None:
            self.read_from(parse_xml_if_str(xml))

    def read_from(self, xml):
        try:
            self.draft = int(
                get_element_text_else_raise(follow_xpath(xml, XmlElements.CONFIG, XmlElements.INITIAL_DRAFT),
                                            XmlElements.INITIAL_DRAFT.value,
                                            f"Got {type(xml)} when looking for {XmlElements.INITIAL_DRAFT.value} element"))
            self.initial_purse = int(
                get_element_text_else_raise(follow_xpath(xml, XmlElements.CONFIG.value, XmlElements.START_COINS.value),
                                            XmlElements.START_COINS.value,
                                            f"Got {type(xml)} when looking for {XmlElements.START_COINS.value} element"))
            self.ante = int(
                get_element_text_else_raise(follow_xpath(xml, XmlElements.CONFIG.value, XmlElements.GAME_ANTE.value),
                                            XmlElements.GAME_ANTE.value,
                                            f"Got {type(xml)} when looking for {XmlElements.GAME_ANTE.value} element"))
            self.buy_char = int(
                get_element_text_else_raise(follow_xpath(xml, XmlElements.CONFIG.value, XmlElements.BUY.value),
                                            XmlElements.BUY.value,
                                            f"Got {type(xml)} when looking for {XmlElements.BUY.value} element"))
            self.banish_char = int(
                get_element_text_else_raise(follow_xpath(xml, XmlElements.CONFIG.value, XmlElements.BANISH.value),
                                            XmlElements.BANISH.value,
                                            f"Got {type(xml)} when looking for {XmlElements.BANISH.value} element"))
            has_sell = follow_xpath(xml, XmlElements.CONFIG.value, XmlElements.SELL.value)
            if has_sell is not None:
                self.sell_char = int(get_element_text_else_raise(has_sell, XmlElements.SELL.value,
                                                                 f"Got {type(xml)} when looking for {XmlElements.SELL.value} element"))

        except AttributeError:
            raise NotXML(f"Was expecting an Element, got {type(xml)}")

    def write_to(self) -> Element:
        subs = {
            XmlElements.INITIAL_DRAFT.value: self.draft,
            XmlElements.START_COINS.value: self.initial_purse,
            XmlElements.BUY.value: self.buy_char,
            XmlElements.GAME_ANTE.value: self.ante,
            XmlElements.BANISH.value: self.banish_char
        }
        if self.sell_char is not None:
            subs[XmlElements.SELL.value] = self.sell_char

        config = Element(XmlElements.CONFIG.value)
        add_sub_elements(config, subs)
        return config


class MarketGameParticipantXML(MarketGameParticipant):
    def __init__(self, player=None, character=None, xml=None):
        super().__init__(player, character)
        if xml is not None:
            self.read_from(parse_xml_if_str(xml))

    def write_to(self) -> Element:
        part = Element(XmlElements.CHARACTER.value, {XmlAttributes.PLAYER.value: self.player})
        part.text = self.character
        return part

    def read_from(self, xml):
        self.character = get_element_text_else_raise(xml, XmlElements.CHARACTER.value,
                                                     f"Got {type(xml)} when looking for {XmlElements.CHARACTER.value} element")
        self.player = get_attribute_else_raise(xml, XmlAttributes.PLAYER.value)


class MarketGameXML(MarketGame):
    def __init__(self, date: datetime | str = None,
                 participants: list[MarketGameParticipant] | tuple[MarketGameParticipant] = None, xml=None):
        super().__init__(date=date, participants=participants)
        if xml is not None:
            self.read_from(parse_xml_if_str(xml))

    def read_from(self, xml):
        self.date = parse_datetime(get_attribute_else_raise(xml, XmlAttributes.DATE.value))
        parts = follow_xpath(xml, XmlElements.GAME, XmlElements.PARTICIPANTS)
        self.participants = [MarketGameParticipantXML(xml=c) for c in parts.findall(XmlElements.CHARACTER.value)]

    def write_to(self) -> Element | None:
        game = Element(XmlElements.GAME.value, {XmlAttributes.DATE.value: self.date.strftime(DATE_FORMAT)})
        # No idea why but it only works this way.
        game.append(add_aspect_sub_elements(Element(XmlElements.PARTICIPANTS.value), self.participants))
        return game
