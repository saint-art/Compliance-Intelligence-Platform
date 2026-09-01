from collectors.presidency_collector import PresidencyCollector
from parsers.presidency_parser import PresidencyParser


SOURCES = [

    {
        "name": "Presidency",

        "collector": PresidencyCollector,

        "parser": PresidencyParser
    },

]