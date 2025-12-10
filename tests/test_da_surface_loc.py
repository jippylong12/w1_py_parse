import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaSurfaceLocationRecord

def test_parse_segment_14_from_sample(tmp_path):
    # Construct a sample file with '14' records
    # Rec ID: 14 (1-2)
    # Longitude: 00123456789 (3-14)
    # Latitude:  00987654321 (15-26)
    
    line_1 = (
        "14"
        "001234567890"  # Longitude
        "009876543210"  # Latitude
    )
    # Pad to cover potential filler (schema doesn't specify large filler but let's be safe)
    line_1 = line_1.ljust(100, ' ') + "\n"
    
    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        + line_1
    )
    
    d = tmp_path / "test_14.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "14" in group
    
    seg14 = group["14"]
    assert isinstance(seg14, DaSurfaceLocationRecord)
    
    assert seg14.longitude == "001234567890"
    assert seg14.latitude == "009876543210"
