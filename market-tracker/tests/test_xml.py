import unittest
from types import FunctionType, LambdaType
from xml.dom.pulldom import CHARACTERS
from xml.etree.ElementTree import parse

from obj import is_str_valid
from obj.xml import MarketPlayerXML, XmlElements, NotXML, WrongXMLElement, is_iterable, make_list_from


def make_xml(tag, text, parent=None):
    if isinstance(text, (list, set, tuple)):
        ret = "".join([f"<{tag}>{t}</{tag}>" for t in text])
        return f"<{parent}>{ret}</{parent}>" if is_str_valid(parent) else ret
    ret = f"<{tag}>{text}</{tag}>"
    return f"<{parent}>{ret}</{parent}>" if is_str_valid(parent) else ret


DAREK_NAME = 'Darek'
DAREK_PURSE = 5

SHERRI_BANISHED = ["Black Widow", "Treant", "Barbarian"]
SHERRI_CHARACTERS = ["Dr. Strange", "Monk", "Huntress", "Krampus", "Pyromancer", "Scarlet Witch"]
SHERRI_NAME = "Sherri"
SHERRI_PURSE = 6

PLAYER_CONSTRUCTOR_NAME = "Talos"
PLAYER_CONSTRUCTOR_PURSE = 12
PLAYER_CONSTRUCTOR_CHARACTERS = ["Jenga", "Jenkins", "Java"]

PLAYER_FILE_CHARS = ["Shadow Thief", "Cursed Pirate", "Thor", "Ninja", "Pyromancer", "Ninja", "Samurai", "Loki"]
PLAYER_FILE_BANISH = ["Scarlet Witch", "Santa", "Seraph", "Gunslinger", "Spider-nan"]

PLAYER_STRING_NAME = "Yager"
PLAYER_STRING_PURSE = 4
PLAYER_STRING_CHARACTERS = ["Tyrant", "Portal", "Kano"]
PLAYER_STRING_BANISHED = ["Porter"]
PLAYER_XML_STRING = f"<{XmlElements.PLAYER.value}>{make_xml(XmlElements.NAME.value, PLAYER_STRING_NAME)}{make_xml(XmlElements.PURSE.value, PLAYER_STRING_PURSE)}{make_xml(XmlElements.CHARACTER.value, PLAYER_STRING_CHARACTERS, XmlElements.CHARACTERS.value)}{make_xml(XmlElements.CHARACTER.value, PLAYER_STRING_BANISHED, XmlElements.BANISHED.value)}</{XmlElements.PLAYER.value}>"
XPATH_TO_PLAYERS = f"./{XmlElements.PLAYERS.value}/{XmlElements.PLAYER.value}"


class MarketXmlTest(unittest.TestCase):
    def setUp(self):
        self.market = parse('test_configs/market.xml')

    def assertAllIn(self, testing, expected):
        for test in testing:
            self.assertIn(test, expected)

    def _if_func_run_else_equal(self, what, expected):
        if isinstance(expected, (FunctionType, LambdaType)):
            self.assertTrue(expected(what))
        elif is_iterable(what):
            self.assertAllIn(what, expected)
        else:
            self.assertEqual(what, expected)

    def _get_an_element(self, xpath, get_first=None):
        if is_iterable(xpath):
            xpath = './{}'.format('/'.join(xpath))
        if get_first is not None:
            for elem in self.market.findall(xpath):
                if get_first(elem):
                    return elem
            return None
        else:
            return self.market.find(xpath)


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
        self.assertEqual(xml.find(XmlElements.PURSE.value).text, SHERRI_PURSE)
        self.assertAllIn(make_list_from(found=xml, the_path=[XmlElements.CHARACTERS.value, XmlElements.CHARACTER.value]), SHERRI_CHARACTERS)
        self.assertAllIn(make_list_from(found=xml, the_path=[XmlElements.BANISHED.value, XmlElements.CHARACTER.value]), SHERRI_BANISHED)

    def __assert_player(self, name, purse, chars, banished):
        self._if_func_run_else_equal(self.player.player_name, name)
        self._if_func_run_else_equal(self.player.purse, purse)
        self._if_func_run_else_equal(self.player.characters, chars)
        self._if_func_run_else_equal(self.player.banished, banished)


if __name__ == '__main__':
    unittest.main()
