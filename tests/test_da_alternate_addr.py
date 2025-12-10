import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import W1RecordGroup, DaAlternateAddressRecord

def test_parse_segment_11_from_sample(tmp_path):
    # Construct a sample file with '11' records
    # Based on user example: "114936 COLLINWOOD AVE"
    # Rec ID: 11 (1-2)
    # Key: 49 (3-4)? or 4 ?
    # Address: 36 COLLINWOOD AVE...
    
    # If the user line is exactly: "114936 COLLINWOOD AVE"
    # Then:
    # 1-2: 11
    # 3-4: 49
    # 5-39: 36 COLLINWOOD AVE...
    
    # Let's try to construct a line that fits the schema perfectly first.
    # 11 (ID)
    # AB (Key)
    # 1234 MAIN STREET                  (Address Line 1)
    
    line_1 = "11AB1234 MAIN STREET                  " # Key AB, Address starts with 1
    # Pad to correct length
    line_1 = line_1.ljust(100, ' ') + "\n"
    
    # Line 2 example
    line_2 = "11ACPO BOX 567                        " # Key AC
    line_2 = line_2.ljust(100, ' ') + "\n"

    content = (
        "01091198799103MCKNIGHT SAND HILLS UNIT        10073056    20251125BLACKBEARD OPERATING, LLC       00ANNNNNNNNNNN09119872025120400000000N                    7305H N000000000000000000 X00000000000000000000000000000\n"
        + line_1
        + line_2
    )
    
    d = tmp_path / "test_11.txt"
    d.write_text(content, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(d))
    
    assert len(records) == 1
    group = records[0]
    
    assert "11" in group
    
    seg11_list = group["11"]
    assert isinstance(seg11_list, list)
    assert len(seg11_list) == 2
    
    rec1 = seg11_list[0]
    assert isinstance(rec1, DaAlternateAddressRecord)
    assert rec1.address_key == "AB"
    assert rec1.address_line.strip() == "1234 MAIN STREET"
    
    rec2 = seg11_list[1]
    assert rec2.address_key == "AC"
    assert rec2.address_line.strip() == "PO BOX 567"

