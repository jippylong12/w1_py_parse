import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaFieldBhlRecord

def test_parse_segment_05_from_sample(tmp_path):
    # Sample from user:
    # 0510      B21       1114  PSL/ MC KNIGHT, M B                                    001150000.0                         00000500S            00345100W            00000500S            00181400E            CRANE        00041000S            00175800E            000000
    # 05 (2)
    # 10      (8) -> Section
    # B21       (10) -> Block
    # 1114  (6) -> Abstract
    # PSL/ MC KNIGHT, M B                                    (55) -> Survey
    # ...
    
    sample_content = (
        "0510      B21       1114  PSL/ MC KNIGHT, M B                                    001150000.0                         00000500S            00345100W            00000500S            00181400E            CRANE        00041000S            00175800E            000000\n"
    )
    # The parser needs a root record to attach 05 to. 
    # Or strict parser might skip it? Logic:
    # if record_id == '01': ...
    # else: if current_record is not None: ...
    # So we need a 01 record first.
    
    full_content = (
        "01091198299103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119822025120400000000N                    7105H N000000000000000000 X00000000000000000000000000000\n"
        "0510      B21       1114  PSL/ MC KNIGHT, M B                                    001150000.0                         00000500S            00345100W            00000500S            00181400E            CRANE        00041000S            00175800E            000000\n"
    )
    
    d = tmp_path / "test_05.txt"
    d.write_text(full_content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "01" in group
    assert "05" in group
    
    seg05 = group["05"]
    assert isinstance(seg05, DaFieldBhlRecord)
    
    # Check specific fields
    assert seg05.bhl_section.strip() == "10"
    assert seg05.bhl_block.strip() == "B21"
    assert seg05.bhl_abstract.strip() == "1114"
    assert seg05.bhl_survey.strip() == "PSL/ MC KNIGHT, M B"
    # bhl_acres at 82 (len 8). Sample: `00115000`?
    # Let's count from survey end (pos 27+55-1 = 81).
    # Next is 82.
    # In sample string:
    # Survey ends at '...B                                    ' (55 chars)
    # Then `00115000` (8 chars).
    assert seg05.bhl_acres == "00115000"
    
    # bhl_nearest_well at 90 (len 28). `0.0                         `?
    # Looks like `0.0` then spaces.
    assert seg05.bhl_nearest_well.strip() == "0.0"
    
    # bhl_county at 202 (len 13). `CRANE        `
    assert seg05.bhl_county.strip() == "CRANE"

