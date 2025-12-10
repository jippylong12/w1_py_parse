import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaRemarkRecord

def test_parse_segment_12_from_sample(tmp_path):
    # Construct a sample file with '12' records
    # Rec ID: 12 (1-2)
    # Seq Num: 001 (3-5)
    # Date: 20251210 (6-13) (Century 20, Year 25, Month 12, Day 10)
    # Remark: "This is a test remark line 1.                                     "
    
    line_1 = (
        "12"
        "001"
        "20251210"
        "This is a test remark line 1.                                         "
    )
    # Pad to correct length (manual says 417 bytes filler at 94, total 511?)
    # Just padding enough to cover fields + some filler
    line_1 = line_1.ljust(150, ' ') + "\n"
    
    line_2 = (
        "12"
        "002"
        "20251211"
        "This is a test remark line 2.                                         "
    )
    line_2 = line_2.ljust(150, ' ') + "\n"

    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        + line_1
        + line_2
    )
    
    d = tmp_path / "test_12.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "12" in group
    
    seg12_list = group["12"]
    assert isinstance(seg12_list, list)
    assert len(seg12_list) == 2
    
    rec1 = seg12_list[0]
    assert isinstance(rec1, DaRemarkRecord)
    assert rec1.remark_sequence_number == 1
    assert rec1.remark_date_year == 25
    assert rec1.remark_line.strip() == "This is a test remark line 1."
    
    rec2 = seg12_list[1]
    assert rec2.remark_sequence_number == 2
    assert rec2.remark_line.strip() == "This is a test remark line 2."

