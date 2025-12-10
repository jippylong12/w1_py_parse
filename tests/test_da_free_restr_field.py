import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaFreeRestrFieldRecord

def test_parse_segment_09_from_sample(tmp_path):
    # Construct a sample file with '09' records
    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        "091234567800000\n"
        "098765432100000\n"
    )
    
    d = tmp_path / "test_09.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "09" in group
    
    # Check that 09 is a list
    seg09_list = group["09"]
    assert isinstance(seg09_list, list)
    assert len(seg09_list) == 2
    
    # Rec 1
    rec1 = seg09_list[0]
    assert isinstance(rec1, DaFreeRestrFieldRecord)
    assert rec1.field_number == "12345678"
    
    # Rec 2
    rec2 = seg09_list[1]
    assert rec2.field_number == "87654321"

