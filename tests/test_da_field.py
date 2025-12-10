
import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import DaFieldRecord

def test_parse_da_field_segment():
    # Sample line from the spec
    # 01...
    # 03 DA-FIELD-NUMBER (8) ...
    
    # Construct a sample line
    # Field 03: 1-2
    # Field Number: 3-10
    # App Well Code: 11
    # Comp Well Code: 12
    # Comp Code: 13
    # Transfer Code: 14
    # Val Date: 15-22
    # Comp Date: 23-30
    # Rule 37: 31
    # Rule 38: 32
    
    # 03 12345678 O G S N 19950101 19950202 Y N
    # 0312345678OGSN1995010119950202YN
    
    line = "0312345678OGSN1995010119950202YN                                                                                                    "
    
    parser = W1Parser()
    record = parser._parse_da_field(line)
    
    assert isinstance(record, DaFieldRecord)
    assert record.record_id == "03"
    assert record.field_number == 12345678
    assert record.field_application_well_code == "O"
    assert record.field_completion_well_code == "G"
    assert record.field_completion_code == "S"
    assert record.field_transfer_code == "N"
    assert record.field_validation_century == 19
    assert record.field_validation_year == 95
    assert record.field_validation_month == 1
    assert record.field_validation_day == 1
    assert record.field_completion_century == 19
    assert record.field_completion_year == 95
    assert record.field_completion_month == 2
    assert record.field_completion_day == 2
    assert record.field_rule37_flag == "Y"
    assert record.field_rule38_flag == "N"

def test_integration_parse_file_with_segment_03(tmp_path):
    # create a dummy file with 01, 02, and 03
    p = tmp_path / "sample.dat"
    # 01 line (min length)
    line01 = "01" + " " * 100 + "\n"
    # 02 line
    line02 = "02" + " " * 501 + "\n"
    # 03 line
    line03 = "0312345678OGSN1995010119950202YN" + " " * 50 + "\n"
    
    p.write_text(line01 + line02 + line03)
    
    parser = W1Parser()
    records = parser.parse_file(str(p))
    
    assert len(records) == 1
    group = records[0]
    
    assert "01" in group
    assert "02" in group
    assert "03" in group
    
    field_rec = group["03"]
    assert field_rec.field_number == 12345678
