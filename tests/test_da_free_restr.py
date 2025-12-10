import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaFreeRestrRecord

def test_parse_segment_08_from_sample(tmp_path):
    # Construct a sample file with '08' records
    # Sample lines from user provided content:
    # 080129THIS WELL MUST COMPLY TO THE NEW SWR 3.13 REQUIREMENTS CONCERNING THE P0000000000
    # 080229ISOLATION OF ANY POTENTIAL FLOW ZONES AND ZONES WITH CORROSIVE FORMATIP0000000000
    # ...
    
    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        "080129THIS WELL MUST COMPLY TO THE NEW SWR 3.13 REQUIREMENTS CONCERNING THE P0000000000\n"
        "080229ISOLATION OF ANY POTENTIAL FLOW ZONES AND ZONES WITH CORROSIVE FORMATIP0000000000\n"
    )
    
    d = tmp_path / "test_08.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "08" in group
    
    # Check that 08 is a list
    seg08_list = group["08"]
    assert isinstance(seg08_list, list)
    assert len(seg08_list) == 2
    
    # Rec 1
    # Key: 01, Type: 29, Remark: 'THIS WELL MUST COMPLY ...', Flag: P
    rec1 = seg08_list[0]
    assert isinstance(rec1, DaFreeRestrRecord)
    assert rec1.restriction_key == 1
    assert rec1.restriction_type == "29"
    assert rec1.restriction_remark.strip() == "THIS WELL MUST COMPLY TO THE NEW SWR 3.13 REQUIREMENTS CONCERNING THE"
    assert rec1.restriction_flag == "P"
    
    # Rec 2
    rec2 = seg08_list[1]
    assert rec2.restriction_key == 2
    assert rec2.restriction_type == "29"
    assert rec2.restriction_remark.strip() == "ISOLATION OF ANY POTENTIAL FLOW ZONES AND ZONES WITH CORROSIVE FORMATI"
    assert rec2.restriction_flag == "P"

