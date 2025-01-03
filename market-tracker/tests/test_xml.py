from datetime import datetime
import unittest
from types import FunctionType, LambdaType
from xml.etree.ElementTree import parse, Element, tostring

from obj import is_str_valid, DATE_FORMAT, if_none_then_default, are_all_in_collection, in_map
from obj.xml import MarketPlayerXML, XmlElements, NotXML, WrongXMLElement, is_iterable, make_list_from, MarketConfigXML, \
    MarketGameParticipantXML, XmlAttributes, MarketGameXML


def try_enum_val(what) -> str:
    try:
        return what.value
    except AttributeError:
        return what


def make_xml(tag, text, parent=None, attrib=None):
    def gen_attrs(attr):
        return ' {}'.format(' '.join([f'{try_enum_val(key)}="{val}"' for key, val in attrib[attr].items()])) if in_map(
            attr, attrib) else ''

    tag_fmt = "<{tag}{attr}>{cdata}</{tag}>"
    ret = ''.join([tag_fmt.format(tag=try_enum_val(tag), attr=gen_attrs(t), cdata=t) for t in text]) if is_iterable(
        text) else tag_fmt.format(tag=try_enum_val(tag), attr=gen_attrs(text), cdata=text)
    return "<{p}{attr}>{cdata}</{p}>".format(p=try_enum_val(parent), attr=gen_attrs(parent), cdata=ret) if is_str_valid(
        try_enum_val(parent)) else ret


ARTIFICER = "Artificer"
BARBARIAN = "Barbarian"
BLACK_PANTHER = "Black Panther"
BLACK_WIDOW = "Black Widow"
CURSED_PIRATE = "Cursed Pirate"
DR_STRANGE = "Dr. Strange"
GUNSLINGER = "Gunslinger"
HUNTRESS = "Huntress"
KRAMPUS = "Krampus"
LOKI = "Loki"
MONK = "Monk"
MOON_ELF = "Moon Elf"
NINJA = "Ninja"
PALADIN = "Paladin"
PYROMANCER = "Pyromancer"
SAMURAI = "Samurai"
SANTA = "Santa"
SCARLET_WITCH = "Scarlet Witch"
SERAPH = "Seraph"
SHADOW_THIEF = "Shadow Thief"
SPIDER_MAN = "Spider-man"
TACTICIAN = "Tactician"
THOR = "Thor"
TREANT = "Treant"
VAMPIRE_LORD = "Vampire Lord"

BRIAN_NAME = "Brian"
BRIAN_PURSE = 10

DAREK_NAME = 'Darek'
DAREK_PURSE = 5

SHERRI_BANISHED = [BLACK_WIDOW, TREANT, BARBARIAN]
SHERRI_CHARACTERS = [DR_STRANGE, MONK, HUNTRESS, KRAMPUS, PYROMANCER, SCARLET_WITCH]
SHERRI_NAME = "Sherri"
SHERRI_PURSE = 6

CONFIG_CONSTRUCTOR_DRAFT = 5
CONFIG_CONSTRUCTOR_INITIAL_PURSE = 3
CONFIG_CONSTRUCTOR_ANTE = 2
CONFIG_CONSTRUCTOR_BUY_CHAR = 2
CONFIG_CONSTRUCTOR_SELL_CHAR = 1
CONFIG_CONSTRUCTOR_BANISH_CHAR = 8

CONFIG_STRING_DRAFT = 2
CONFIG_STRING_INITIAL_PURSE = 3
CONFIG_STRING_ANTE = 1
CONFIG_STRING_BUY_CHAR = 4
CONFIG_STRING_SELL_CHAR = 1
CONFIG_STRING_BANISH_CHAR = 4
CONFIG_STRING_ALWAYS_PRESET = (make_xml(XmlElements.INITIAL_DRAFT.value, CONFIG_STRING_DRAFT),
                               make_xml(XmlElements.START_COINS.value, CONFIG_STRING_INITIAL_PURSE),
                               make_xml(XmlElements.GAME_ANTE.value, CONFIG_STRING_ANTE),
                               make_xml(XmlElements.BUY.value, CONFIG_STRING_BUY_CHAR),
                               make_xml(XmlElements.BANISH.value, CONFIG_STRING_BANISH_CHAR))
CONFIG_XML = "{}".format(make_xml(XmlElements.CONFIG.value,
                                  f"{''.join(CONFIG_STRING_ALWAYS_PRESET)}{make_xml(XmlElements.SELL.value, CONFIG_STRING_SELL_CHAR)}",
                                  XmlElements.MARKET.value))
CONFIG_XML_NO_SELL = "<{}>{}</{}>".format(XmlElements.CONFIG.value, ''.join(CONFIG_STRING_ALWAYS_PRESET),
                                          XmlElements.CONFIG.value)

CONFIG_FILE_DRAFT = 4
CONFIG_FILE_INITIAL_PURSE = 5
CONFIG_FILE_ANTE = -1
CONFIG_FILE_BUY_CHAR = -3
CONFIG_FILE_SELL_CHAR = 2
CONFIG_FILE_BANISH_CHAR = 7

PLAYER_CONSTRUCTOR_NAME = "Talos"
PLAYER_CONSTRUCTOR_PURSE = 12
PLAYER_CONSTRUCTOR_CHARACTERS = ["Jenga", "Jenkins", "Java"]

PLAYER_FILE_CHARS = [SHADOW_THIEF, CURSED_PIRATE, THOR, PYROMANCER, SAMURAI, LOKI, NINJA]
PLAYER_FILE_BANISH = [SCARLET_WITCH, SANTA, SERAPH, GUNSLINGER, SPIDER_MAN]

PLAYER_STRING_NAME = "Yager"
PLAYER_STRING_PURSE = 4
PLAYER_STRING_CHARACTERS = ["Tyrant", "Portal", "Kano"]
PLAYER_STRING_BANISHED = ["Porter"]
PLAYER_XML_STRING = f"<{XmlElements.PLAYER.value}>{make_xml(XmlElements.NAME.value, PLAYER_STRING_NAME)}{make_xml(XmlElements.PURSE, PLAYER_STRING_PURSE)}{make_xml(XmlElements.CHARACTER.value, PLAYER_STRING_CHARACTERS, XmlElements.CHARACTERS.value)}{make_xml(XmlElements.CHARACTER.value, PLAYER_STRING_BANISHED, XmlElements.BANISHED.value)}</{XmlElements.PLAYER.value}>"
XPATH_TO_PLAYERS = f"./{XmlElements.PLAYERS.value}/{XmlElements.PLAYER.value}"

PARTICIPANT_CONSTRUCTOR_PLAYER = "Miku"
PARTICIPANT_CONSTRUCTOR_CHARACTER = "Iceman"

PARTICIPANT_STRING_PLAYER = "Regalia"
PARTICIPANT_STRING_CHARACTER = "Ultraman"
PARTICIPANT_XML = f"<{XmlElements.CHARACTER.value} {XmlAttributes.PLAYER.value}='{PARTICIPANT_STRING_PLAYER}'>{PARTICIPANT_STRING_CHARACTER}</{XmlElements.CHARACTER.value}>"

PARTICIPANT_FILE_PLAYER = DAREK_NAME
PARTICIPANT_FILE_CHARACTER = SHADOW_THIEF

GAME_CONSTRUCTOR_DATE = datetime(year=2024, month=12, day=25, hour=0, minute=34, second=3, microsecond=123456)
GAME_CONSTRUCTOR_PARTICIPANTS = [
    MarketGameParticipantXML(player=DAREK_NAME, character=BARBARIAN),
    MarketGameParticipantXML(player=SHERRI_NAME, character=SERAPH),
]

GAME_STRING_DATE = datetime(year=2024, month=12, day=24, hour=12, minute=4, second=33, microsecond=123456)
GAME_STRING_PARTICIPANTS = [
    MarketGameParticipantXML(player=DAREK_NAME, character=SANTA),
    MarketGameParticipantXML(player=SHERRI_NAME, character=BLACK_PANTHER),
    MarketGameParticipantXML(player=BRIAN_NAME, character=PALADIN)
]
GAME_XML_STRING_PARTICIPANTS = make_xml(tag=XmlElements.CHARACTER, text=[SANTA, BLACK_PANTHER, PALADIN],
                                        parent=XmlElements.PARTICIPANTS,
                                        attrib={SANTA: {XmlAttributes.PLAYER: DAREK_NAME},
                                                BLACK_PANTHER: {XmlAttributes.PLAYER: SHERRI_NAME},
                                                PALADIN: {XmlAttributes.PLAYER: BRIAN_NAME}})
GAME_XML_STRING = "<{game} date='{game_date}'>{the_game}</{game}>".format(game=XmlElements.GAME.value,
                                                                          game_date=GAME_STRING_DATE.strftime(
                                                                              DATE_FORMAT), the_game=''.join(
        [GAME_XML_STRING_PARTICIPANTS]))

GAME_FILE_PARTICIPANTS = [
    MarketGameParticipantXML(player=DAREK_NAME, character=DR_STRANGE),
    MarketGameParticipantXML(player=BRIAN_NAME, character=SAMURAI),
    MarketGameParticipantXML(player=SHERRI_NAME, character=VAMPIRE_LORD),
]

GAME_ONE_DATE = datetime(year=2024, month=3, day=4, hour=19, minute=12, second=23, microsecond=123000)
GAME_TWO_DATE = datetime(year=2024, month=4, day=4, hour=12, minute=19, second=23, microsecond=123000)


class MarketXmlTest(unittest.TestCase):
    def setUp(self):
        self.market = parse('test_configs/market.xml')

    def assertAllIn(self, testing, expected):
        for test in expected:
            self.assertIn(test, testing)

    def _if_func_run_else_equal(self, what, expected):
        if isinstance(expected, (FunctionType, LambdaType)):
            self.assertTrue(expected(what))
        elif is_iterable(what):
            self.assertAllIn(what, expected)
        else:
            self.assertEqual(what, expected)

    def _get_an_element(self, xpath, get_first=None, xml=None):
        xml = if_none_then_default(xml, self.market)
        if is_iterable(xpath):
            xpath = './{}'.format('/'.join(xpath))
        if get_first is not None:
            for elem in xml.findall(xpath):
                if get_first(elem):
                    return elem
            return None
        else:
            return xml.find(xpath)

    def _get_a_game(self, date=None, participants=None):
        game_path = [XmlElements.GAMES.value, XmlElements.GAME.value]
        if date is not None:
            return self._get_an_element(xpath=game_path,
                                        get_first=lambda g: datetime.strptime(g.attrib[XmlAttributes.DATE.value],
                                                                              DATE_FORMAT) == date)
        elif participants is not None and participants:
            return self._get_an_element(xpath=game_path, get_first=lambda g: are_all_in_collection(
                make_list_from(g, the_path=f"./{XmlElements.PARTICIPANTS.value}/{XmlElements.CHARACTER.value}"),
                participants))

        return None


class TestMarketPlayerXml(MarketXmlTest):
    def test_constructor(self):
        self.player = MarketPlayerXML(PLAYER_CONSTRUCTOR_NAME, PLAYER_CONSTRUCTOR_PURSE, PLAYER_CONSTRUCTOR_CHARACTERS)
        self.__assert_player(PLAYER_CONSTRUCTOR_NAME, lambda p: p == PLAYER_CONSTRUCTOR_PURSE,
                             PLAYER_CONSTRUCTOR_CHARACTERS, lambda b: len(b) == 0)

    def test_string(self):
        self.player = MarketPlayerXML(xml=PLAYER_XML_STRING)
        self.__assert_player(PLAYER_STRING_NAME, PLAYER_STRING_PURSE, PLAYER_STRING_CHARACTERS, PLAYER_STRING_BANISHED)

    def test_from_file(self):
        self.player = MarketPlayerXML(
            xml=self._get_an_element(f"./{XmlElements.PLAYERS.value}/{XmlElements.PLAYER.value}",
                                     lambda e: e.find(XmlElements.NAME.value).text == DAREK_NAME))
        self.__assert_player(DAREK_NAME, DAREK_PURSE, PLAYER_FILE_CHARS, PLAYER_FILE_BANISH)

    def test_not_xml(self):
        with self.assertRaises(NotXML):
            self.player = MarketPlayerXML(xml=2)

    def test_wrong_element(self):
        with self.assertRaises(WrongXMLElement):
            self.player = MarketPlayerXML(xml=self.market.find(XmlElements.PLAYERS.value))

    def test_write_xml(self):
        self.player = MarketPlayerXML(xml=self._get_an_element([XmlElements.PLAYERS.value, XmlElements.PLAYER.value],
                                                               lambda e: e.find(
                                                                   XmlElements.NAME.value).text == SHERRI_NAME))
        xml = self.player.write_to()
        self.assertEqual(xml.find(XmlElements.NAME.value).text, SHERRI_NAME)
        self.assertEqual(int(xml.find(XmlElements.PURSE.value).text), SHERRI_PURSE)
        self.assertAllIn(
            make_list_from(found=xml, the_path=[XmlElements.CHARACTERS.value, XmlElements.CHARACTER.value]),
            SHERRI_CHARACTERS)
        self.assertAllIn(make_list_from(found=xml, the_path=[XmlElements.BANISHED.value, XmlElements.CHARACTER.value]),
                         SHERRI_BANISHED)

    def __assert_player(self, name, purse, chars, banished):
        self._if_func_run_else_equal(self.player.player_name, name)
        self._if_func_run_else_equal(self.player.purse, purse)
        self._if_func_run_else_equal(self.player.characters, chars)
        self._if_func_run_else_equal(self.player.banished, banished)


class TestMarketConfigGameXML(MarketXmlTest):
    def test_constructor(self):
        self.config = MarketConfigXML(draft=CONFIG_CONSTRUCTOR_DRAFT, initial_purse=CONFIG_CONSTRUCTOR_INITIAL_PURSE,
                                      ante=CONFIG_CONSTRUCTOR_ANTE, buy_char=CONFIG_CONSTRUCTOR_BUY_CHAR,
                                      sell_char=CONFIG_CONSTRUCTOR_SELL_CHAR,
                                      banish_char=CONFIG_CONSTRUCTOR_BANISH_CHAR)
        self.__match_values(CONFIG_CONSTRUCTOR_DRAFT, CONFIG_CONSTRUCTOR_INITIAL_PURSE, CONFIG_CONSTRUCTOR_ANTE,
                            CONFIG_CONSTRUCTOR_BUY_CHAR, CONFIG_CONSTRUCTOR_BANISH_CHAR, CONFIG_CONSTRUCTOR_SELL_CHAR)

    def test_string_market(self):
        self.config = MarketConfigXML(xml=CONFIG_XML)
        self.__match_values(CONFIG_STRING_DRAFT, CONFIG_STRING_INITIAL_PURSE, CONFIG_STRING_ANTE,
                            CONFIG_STRING_BUY_CHAR, CONFIG_STRING_BANISH_CHAR, CONFIG_STRING_SELL_CHAR)

    def test_string_config(self):
        self.config = MarketConfigXML(xml=CONFIG_XML_NO_SELL)
        self.__match_values(CONFIG_STRING_DRAFT, CONFIG_STRING_INITIAL_PURSE, CONFIG_STRING_ANTE,
                            CONFIG_STRING_BUY_CHAR, CONFIG_STRING_BANISH_CHAR)

    def test_file(self):
        self.config = MarketConfigXML(xml=self.market)
        self.__match_values(CONFIG_FILE_DRAFT, CONFIG_FILE_INITIAL_PURSE, CONFIG_FILE_ANTE,
                            CONFIG_FILE_BUY_CHAR, CONFIG_FILE_BANISH_CHAR, CONFIG_FILE_SELL_CHAR)

    def test_write_xml(self):
        self.config = MarketConfigXML(xml=self.market)
        wrote = self.config.write_to()
        self._if_func_run_else_equal(wrote, lambda d: int(
            wrote.find(XmlElements.INITIAL_DRAFT.value).text) == CONFIG_FILE_DRAFT)
        self._if_func_run_else_equal(wrote, lambda d: int(
            wrote.find(XmlElements.START_COINS.value).text) == CONFIG_FILE_INITIAL_PURSE)
        self._if_func_run_else_equal(wrote,
                                     lambda d: int(wrote.find(XmlElements.GAME_ANTE.value).text) == CONFIG_FILE_ANTE)
        self._if_func_run_else_equal(wrote,
                                     lambda d: int(wrote.find(XmlElements.BUY.value).text) == CONFIG_FILE_BUY_CHAR)
        self._if_func_run_else_equal(wrote,
                                     lambda d: int(wrote.find(XmlElements.SELL.value).text) == CONFIG_FILE_SELL_CHAR)
        self._if_func_run_else_equal(wrote, lambda d: int(
            wrote.find(XmlElements.BANISH.value).text) == CONFIG_FILE_BANISH_CHAR)

    def __match_values(self, draft, initial_purse, ante, buy_char, banish_char, sell_char=None):
        self._if_func_run_else_equal(self.config.draft, draft)
        self._if_func_run_else_equal(self.config.initial_purse, initial_purse)
        self._if_func_run_else_equal(self.config.ante, ante)
        self._if_func_run_else_equal(self.config.buy_char, buy_char)
        self._if_func_run_else_equal(self.config.banish_char, banish_char)
        if sell_char is not None:
            self._if_func_run_else_equal(self.config.sell_char, sell_char)


class TestMarketGameParticipantXML(MarketXmlTest):
    def test_constructor(self):
        self.participant = MarketGameParticipantXML(player=PARTICIPANT_CONSTRUCTOR_PLAYER,
                                                    character=PARTICIPANT_CONSTRUCTOR_CHARACTER)
        self._if_func_run_else_equal(self.participant, MarketGameParticipantXML(player=PARTICIPANT_CONSTRUCTOR_PLAYER,
                                                                                character=PARTICIPANT_CONSTRUCTOR_CHARACTER))

    def test_string(self):
        self.participant = MarketGameParticipantXML(xml=PARTICIPANT_XML)
        self._if_func_run_else_equal(self.participant, MarketGameParticipantXML(player=PARTICIPANT_STRING_PLAYER,
                                                                                character=PARTICIPANT_STRING_CHARACTER))

    def test_file(self):
        self.participant = MarketGameParticipantXML(
            xml=self._get_an_element((XmlElements.PARTICIPANTS.value, XmlElements.CHARACTER.value),
                                     lambda x: x.attrib[XmlAttributes.PLAYER.value] == DAREK_NAME,
                                     self._get_a_game(GAME_ONE_DATE)))
        self._if_func_run_else_equal(self.participant, MarketGameParticipantXML(player=PARTICIPANT_FILE_PLAYER,
                                                                                character=PARTICIPANT_FILE_CHARACTER))


class TestMarketGameXML(MarketXmlTest):
    def test_constructor(self):
        self.__assert_game(
            check_game=MarketGameXML(date=GAME_CONSTRUCTOR_DATE, participants=GAME_CONSTRUCTOR_PARTICIPANTS),
            expected_game=MarketGameXML(date=GAME_CONSTRUCTOR_DATE, participants=GAME_CONSTRUCTOR_PARTICIPANTS))

    def test_string(self):
        self.__assert_game(expected_participants=GAME_STRING_PARTICIPANTS,
                           check_game=MarketGameXML(xml=GAME_XML_STRING))

    def test_file(self):
        self.__assert_game(expected_date=GAME_TWO_DATE, expected_participants=GAME_FILE_PARTICIPANTS,
                           check_game=MarketGameXML(xml=self._get_a_game(GAME_TWO_DATE)))

    def test_write_xml(self):
        xml = MarketGameXML(date=GAME_CONSTRUCTOR_DATE, participants=GAME_CONSTRUCTOR_PARTICIPANTS).write_to()
        check_game = MarketGameXML(xml=xml)
        self.__assert_game(
            expected_game=MarketGameXML(date=GAME_CONSTRUCTOR_DATE, participants=GAME_CONSTRUCTOR_PARTICIPANTS),
            check_game=check_game)

    def __assert_game(self, expected_game: MarketGameXML = None, expected_date: datetime = None,
                      expected_participants: list[MarketGameParticipantXML] = None, check_game: MarketGameXML = None):
        if expected_game is not None:
            self.assertEqual(expected_game, check_game)
        else:
            if expected_date is not None:
                self.assertEqual(expected_date, check_game.date)
            if expected_participants is not None:
                self.assertAllIn(expected_participants, check_game.participants)


if __name__ == '__main__':
    unittest.main()
