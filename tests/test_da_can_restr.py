import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaCanRestrRecord

def test_parse_segment_06_from_sample(tmp_path):
    # Construct a sample file with recurring 06 segments
    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        "0510      B21       1114  PSL/ MC KNIGHT, M B                                    001150000.0                         00000500S            00312300W            00000500S            00214200E            CRANE        00049400S            00200600E            000000\n"
        "060201                                   P0000000000\n"
        "060306                                   F0000000000\n"
        "078047331000000\n"
        "060402                                   F0000000000\n"
    )
    
    d = tmp_path / "test_06.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "01" in group
    assert "06" in group
    
    # Check that 06 is a list
    seg06_list = group["06"]
    assert isinstance(seg06_list, list)
    assert len(seg06_list) == 3
    
    # Verify individual records
    # 06 (2) Key (2) Type (2) Remark (35) Flag (1)
    
    # Rec 1: 06 02 01 "                                   " P
    rec1 = seg06_list[0]
    assert isinstance(rec1, DaCanRestrRecord)
    assert rec1.restriction_key == 2
    assert rec1.restriction_type == "01"
    assert rec1.restriction_flag == "P"
    
    # Rec 2: 06 03 06 "                                   " F
    rec2 = seg06_list[1]
    assert rec2.restriction_key == 3
    assert rec2.restriction_type == "06"
    assert rec2.restriction_flag == "F"
    
    # Rec 3: 06 04 02 "                                   " F
    rec3 = seg06_list[2]
    assert rec3.restriction_key == 4
    assert rec3.restriction_type == "02"
    assert rec3.restriction_flag == "F"

