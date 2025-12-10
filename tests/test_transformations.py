import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import DaRootRecord, DaPermitRecord, DaCanRestrRecord

# Sample data snippets for testing
# We need valid lines that parse into these records.

# Schema 01 (Root)
# 01... county at 12 (3 chars). 001 = Anderson.
# 01000000000001                                00900000    00000000                                000N0NNNNNNNNNN00000000000000000000N                    000000000000000NE                                  
# Let's construct a minimal valid line for 01.
# 1-2: 01
# 3-9: 0000000
# 10-11: 00
# 12-14: 001 (Anderson)
# ... pad the rest
LINE_01_ANDERSON = "01000000000001" + " " * 32 + "00000000    00000000" + " " * 32 + "000N0NNNNNNNNNN00000002025010100000000N                    0000000000000000NE" + " " * 500

# Schema 02 (Permit)
# 02... county at 12 (3 chars). 201 = HARRIS.
# Well status at 170 (1 char). 'W' = Final Completion.
# Type App at 66 (2 chars). 'G ' = Gas.
LINE_02_HARRIS = "02" + "0" * 7 + "00" + "201" + " " * 32 + "00" + "00000000000" + "000000G " + " " * 400 
# Note: Type App is at 66.
# 02 (2)
# PermitNum (7) -> 9
# Seq (2) -> 11
# County (3) -> 14. "201"
# Lease (32) -> 46
# Dist (2) -> 48
# Well (6) -> 54
# Depth (5) -> 59
# Op (6) -> 65
# Type App (2) -> 67. "G "
# ...
# Well Status (1) at 170.
# We need to pad correctly to reach 170.
# Let's use a helper or make a long string.
# 68 (Other Expl) + 30 = 97.
# 98 (Addr Unique) + 6 = 103.
# 104 (Zip Prefix) + 5 = 108.
# 109 (Zip Suffix) + 4 = 112.
# 113 (Fiche) + 6 = 118.
# 119 (Onshore County) + 3 = 121. Let's make this 003 (ANDREWS).
# 122 (Rec Date) + 8 = 129
# ...
# 170 (Well Status) + 1. Let's put 'W'.

def create_line_02():
    # Helper to build a line by fields would be better but for now padding:
    # 01-65: ...
    # 66-67: "G "
    # ...
    # 119-121: "003"
    # ...
    # 170: "W"
    
    # We can use ljust.
    line = "02" + "0"*7 + "00" + "201" + " " * 32 + "00" + "000000" + "00000" + "000000" # Ends at 65
    line += "G " # 66-67: Type App
    line += " " * 30 # 68-97
    line += "000000" # 98-103
    line += "78701" # 104-108
    line += "0000" # 109-112
    line += "000000" # 113-118
    line += "003" # 119-121: Onshore County (ANDREWS)
    line += " " * 48 # 122-169?
    # 122 (Received) 8
    # 130 (Issued) 8
    # 138 (Amended) 8
    # 146 (Extended) 8
    # 154 (Spud) 8
    # 162 (Surf Casing) 8
    # Total 48. Correct.
    line += "W" # 170: Well Status
    line = line.ljust(524, ' ')
    return line

LINE_02_FULL = create_line_02()

# Schema 06 (Canned Restriction)
# 06... Restriction Type at 5 (2 chars). "A ".
def create_line_06():
    # 01-02: 06
    # 03-04: Key (int) "01"
    # 05-06: Type "A "
    # 07-41: Remark
    line = "0601A " + " " * 35 + "N"
    return line.ljust(500, ' ')

LINE_06_FULL = create_line_06()

def test_transformations_disabled(tmp_path):
    # Create a file
    f = tmp_path / "test.dat"
    f.write_text(LINE_01_ANDERSON + "\n" + LINE_02_FULL + "\n" + LINE_06_FULL, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(f), transform_codes=False)
    
    assert len(records) == 1
    group = records[0]
    
    # Check 01
    root = group['01']
    assert isinstance(root, DaRootRecord)
    assert root.county_code == 1 # Int, not "ANDERSON"
    
    # Check 02
    permit = group['02']
    assert isinstance(permit, DaPermitRecord)
    assert permit.county_code == 201 # Int, not "HARRIS"
    assert permit.onshore_county == 3 # Int
    assert permit.well_status == "W"
    assert permit.type_application == "G" # Stripped "G "
    
    # Check 06
    restrs = group['06']
    assert len(restrs) == 1
    restr = restrs[0]
    assert restr.restriction_type == "A"

def test_transformations_enabled(tmp_path):
    f = tmp_path / "test.dat"
    f.write_text(LINE_01_ANDERSON + "\n" + LINE_02_FULL + "\n" + LINE_06_FULL, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(f), transform_codes=True)
    
    assert len(records) == 1
    group = records[0]
    
    # Check 01
    root = group['01']
    assert root.county_code == "ANDERSON"
    
    # Check 02
    permit = group['02']
    assert permit.county_code == "HARRIS"
    assert permit.onshore_county == "ANDREWS"
    assert permit.well_status == "Final Completion"
    assert permit.type_application == "Gas"
    
    # Check 06
    restr = group['06'][0]
    assert "THIS WELL IS NEVER COMPLETED IN THE SAME RESERVOIR" in restr.restriction_type

def test_transformations_unknown_codes(tmp_path):
    # Line with unknown county code 999
    line_01_unknown = LINE_01_ANDERSON.replace("001", "999", 1)
    
    f = tmp_path / "test_unknown.dat"
    f.write_text(line_01_unknown, encoding='utf-8')
    
    parser = W1Parser()
    records = parser.parse_file(str(f), transform_codes=True)
    
    root = records[0]['01']
    assert root.county_code == 999 # Unchanged
