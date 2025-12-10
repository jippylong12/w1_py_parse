import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaCheckRegisterRecord

def test_parse_segment_13_from_sample(tmp_path):
    # Construct a sample file with '13' records
    # Rec ID: 13 (1-2)
    # Date: 20251210 (Century 20, Year 25, Month 12, Day 10) (3-10)
    # Register Number: 12345678 (11-18)
    
    line_1 = (
        "13"
        "20251210"
        "12345678"
    )
    # Pad to cover filler
    line_1 = line_1.ljust(100, ' ') + "\n"
    
    line_2 = (
        "13"
        "20251211"
        "87654321"
    )
    line_2 = line_2.ljust(100, ' ') + "\n"

    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        + line_1
        + line_2
    )
    
    d = tmp_path / "test_13.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "13" in group
    
    seg13_list = group["13"]
    assert isinstance(seg13_list, list)
    assert len(seg13_list) == 2
    
    rec1 = seg13_list[0]
    assert isinstance(rec1, DaCheckRegisterRecord)
    assert rec1.register_date_year == 25
    assert rec1.register_number == 12345678
    
    rec2 = seg13_list[1]
    assert rec2.register_number == 87654321

