"""
Central registry of every collector/parser pair in the platform.

Used by tools/run_all_pipelines.py to refresh the full dataset
with a single command, and serves as living documentation of
every source currently integrated.
"""

from collectors.cabinet_collector import CabinetCollector
from parsers.cabinet_parser import CabinetParser

from collectors.presidency_collector import PresidencyCollector
from parsers.presidency_parser import PresidencyParser

from collectors.national_assembly_collector import NationalAssemblyCollector
from parsers.national_assembly_parser import NationalAssemblyParser

from collectors.senate_collector import SenateCollector
from parsers.senate_parser import SenateParser

from collectors.governors_collector import GovernorsCollector
from parsers.governors_parser import GovernorsParser

from collectors.supreme_court_collector import SupremeCourtCollector
from collectors.court_of_appeal_collector import CourtOfAppealCollector
from collectors.high_court_collector import HighCourtCollector
from collectors.elrc_collector import ELRCCollector
from collectors.elc_collector import ELCCollector
from parsers.judiciary_parser import JudiciaryParser

from collectors.kra_collector import KRACollector
from parsers.kra_parser import KRAParser

from collectors.kplc_collector import KPLCCollector
from parsers.kplc_parser import KPLCParser

from collectors.nssf_collector import NSSFCollector
from parsers.nssf_parser import NSSFParser


SOURCES = [
    {"name": "Cabinet", "collector": CabinetCollector, "parser": CabinetParser},
    {"name": "Presidency", "collector": PresidencyCollector, "parser": PresidencyParser},
    {"name": "National Assembly", "collector": NationalAssemblyCollector, "parser": NationalAssemblyParser},
    {"name": "Senate", "collector": SenateCollector, "parser": SenateParser},
    {"name": "Governors", "collector": GovernorsCollector, "parser": GovernorsParser},
    {"name": "Supreme Court", "collector": SupremeCourtCollector, "parser": JudiciaryParser},
    {"name": "Court of Appeal", "collector": CourtOfAppealCollector, "parser": JudiciaryParser},
    {"name": "High Court", "collector": HighCourtCollector, "parser": JudiciaryParser},
    {"name": "Employment and Labour Relations Court", "collector": ELRCCollector, "parser": JudiciaryParser},
    {"name": "Environment and Land Court", "collector": ELCCollector, "parser": JudiciaryParser},
    {"name": "Kenya Revenue Authority", "collector": KRACollector, "parser": KRAParser},
    {"name": "Kenya Power and Lighting Company", "collector": KPLCCollector, "parser": KPLCParser},
    {"name": "National Social Security Fund", "collector": NSSFCollector, "parser": NSSFParser},
]
