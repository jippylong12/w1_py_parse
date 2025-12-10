import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaCanRestrFieldRecord

def test_parse_segment_07_from_sample(tmp_path):
    # Construct a sample file with recurring 06 and 07 segments
    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        "060201                                   P0000000000\n"
        "076999620000000\n"
        "071234567800000\n"
        "060306                                   F0000000000\n"
    )
    
    d = tmp_path / "test_07.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "07" in group
    
    # Check that 07 is a list
    seg07_list = group["07"]
    assert isinstance(seg07_list, list)
    assert len(seg07_list) == 2
    
    # Verify individual records
    # 07 (2) FieldNo (8)
    
    # Rec 1: 07 69996200
    rec1 = seg07_list[0]
    assert isinstance(rec1, DaCanRestrFieldRecord)
    assert rec1.field_number == "69996200"
    
    # Rec 2: 07 12345678
    rec2 = seg07_list[1]
    assert rec2.field_number == "12345678"

