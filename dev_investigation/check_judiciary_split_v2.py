from parsers.judiciary_parser import JudiciaryParser

parser = JudiciaryParser()

test_cases = [
    "Judge, Court of Appeal",
    "Chief Justice and President of the Supreme Court of Kenya",
    "Deputy Chief Justice and Vice President of the Supreme Court of Kenya",
    "Judge of the Supreme Court of Kenya",
    "judge of the ELRC",
    "Principal Judge, ELRC",
    "Judge of the ELRC",
]

for designation in test_cases:
    title, court = parser._split_designation(designation)
    print(f"{designation!r:65} -> title={title!r:35} court={court!r}")
