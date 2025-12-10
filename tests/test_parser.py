import pytest
from w1_py_parse.parser import W1Parser
import json

def test_parser_workflow(tmp_path):
    # Create a dummy file with Schema 01 and 02
    d = tmp_path / "test_data.txt"
    # Line 1: 01 (Root)
    # Line 2: 02 (Permit) - Using the real sample line
    content = (
        "01091197899003SPDTX SWD                       10900327    20251125WATERBRIDGE STATELINE LLC       00ANNNNNNNNNNN09119782025120300000000N                      17  N000000000000000000 E00000000000000000000000000000\n"
        "02091197899003SPDTX SWD                       10  17  0597590032701                              000000000000000000000000202511252025120300000000000000000000000000000000 000000002027120300000000                              NNNN00000000000000N9       A40       PSL / MILES, T J                                       782   00000000275002720W     ANDREWS      00015000FWL          00020000FSL          00035900FWL          00034700FSL          0.0                         O00000000 NNNN09748797 NN       00349279"
    )
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    # Verify return type
    assert isinstance(records, list)
    assert len(records) == 1
    
    # Verify grouping
    item = records[0]
    assert isinstance(item, dict)
    assert "01" in item
    assert "02" in item
    
    # Verify data content
    assert item["01"]["status_number"] == 911978
    assert item["02"]["permit_number"] == 911978
    assert item["02"]["api_number"] == "00349279"
    
    # Verify JSON structure
    json_out = parser.to_json()
    data = json.loads(json_out)
    assert len(data) == 1
    assert data[0]["01"]["lease_name"].strip() == "SPDTX SWD"
