from obj import is_str_valid


class NotXML(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class WrongXMLElement(Exception):
    def __init__(self, msg=None, got_tag=None, expected_tag=None):
        self.msg = msg
        self.got_tag = got_tag
        self.expected_tag = expected_tag

    def __str__(self):
        return self.msg if is_str_valid(self.msg) else "Wanted tag {expected_tag} but got tag {got_tag}".format(
            expected_tag=self.expected_tag, got_tag=self.got_tag)
