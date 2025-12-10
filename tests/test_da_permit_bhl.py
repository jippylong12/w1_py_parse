import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaPermitBhlRecord

def test_parse_segment_10_from_sample(tmp_path):
    # Construct a sample file with '10' record
    # Sample based on manual structure
    # 10 (2)
    # Section (8) ex: "      12"
    # Block (10) ex: "       A  "
    # Abstract (6) ex: "   123"
    # Survey (55) ex: "Test Survey Name                                       "
    # Acres (8) ex: "  100.00"
    # Nearest Well (28)
    # ...
    
    line_10 = (
        "10"
        "SECTION1"  # 3-10 (8)
        "BLOCK12345" # 11-20 (10)
        "ABSTR1"    # 21-26 (6)
        "SURVEY NAME IS HERE                                    " # 27-81 (55)
        "06400000"  # 82-89 (8) Acres
        "NEAREST WELL INFO           " # 90-117 (28)
        "00100000"  # 118-125 (8) Lease Ft 1
        "NORTH        " # 126-138 (13) Lease Dir 1
        "00200000"  # 139-146 (8) Lease Ft 2
        "EAST         " # 147-159 (13) Lease Dir 2
        "00300000"  # 160-167 (8) Survey Ft 1
        "SOUTH        " # 168-180 (13) Survey Dir 1
        "00400000"  # 181-188 (8) Survey Ft 2
        "WEST         " # 189-201 (13) Survey Dir 2
        "LOVING       " # 202-214 (13) County
        "00050000"  # 215-222 (8) Pntrt Dist 1
        "NW           " # 223-235 (13) Pntrt Dir 1
        "00060000"  # 236-243 (8) Pntrt Dist 2
        "SE           " # 244-256 (13) Pntrt Dir 2
        "000000"    # Filler
    )
    # Pad to full length just in case, though parser only cares about fields
    line_10 = line_10.ljust(553, ' ') + "\n"

    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        + line_10
    )
    
    d = tmp_path / "test_10.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "10" in group
    
    rec = group["10"]
    assert isinstance(rec, DaPermitBhlRecord)
    
    # Verify fields
    assert rec.bhl_section == "SECTION1"
    assert rec.bhl_block == "BLOCK12345"
    assert rec.bhl_abstract == "ABSTR1"
    assert rec.bhl_survey.strip() == "SURVEY NAME IS HERE"
    assert rec.bhl_acres == "06400000"
    assert rec.bhl_nearest_well.strip() == "NEAREST WELL INFO"
    assert rec.bhl_lease_feet_1 == "00100000"
    assert rec.bhl_lease_direction_1.strip() == "NORTH"
    assert rec.bhl_county.strip() == "LOVING"

