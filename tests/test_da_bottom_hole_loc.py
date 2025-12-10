import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaBottomHoleLocationRecord

def test_parse_segment_15_from_sample(tmp_path):
    # Construct a sample file with '15' records
    # Rec ID: 15 (1-2)
    # Longitude: 00123456789 (3-14)
    # Latitude:  00987654321 (15-26)
    
    line_1 = (
        "15"
        "001234567890"  # Longitude
        "009876543210"  # Latitude
    )
    # Pad
    line_1 = line_1.ljust(100, ' ') + "\n"
    
    line_2 = (
        "15"
        "002234567890"
        "008876543210"
    )
    line_2 = line_2.ljust(100, ' ') + "\n"

    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        + line_1
        + line_2
    )
    
    d = tmp_path / "test_15.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "15" in group
    
    seg15_list = group["15"]
    assert isinstance(seg15_list, list)
    assert len(seg15_list) == 2
    
    rec1 = seg15_list[0]
    assert isinstance(rec1, DaBottomHoleLocationRecord)
    assert rec1.longitude == "001234567890"
    assert rec1.latitude == "009876543210"
    
    rec2 = seg15_list[1]
    assert rec2.longitude == "002234567890"
    assert rec2.latitude == "008876543210"
