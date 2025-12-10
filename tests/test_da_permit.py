import pytest
from w1_py_parse.parser import W1Parser
from w1_py_parse.models import DaPermitRecord
from w1_py_parse.schemas.da_permit import DA_PERMIT_FIELDS

def test_parse_da_permit_record():
    # Real line from sample data
    line = "02091197899003SPDTX SWD                       10  17  0597590032701                              000000000000000000000000202511252025120300000000000000000000000000000000 000000002027120300000000                              NNNN00000000000000N9       A40       PSL / MILES, T J                                       782   00000000275002720W     ANDREWS      00015000FWL          00020000FSL          00035900FWL          00034700FSL          0.0                         O00000000 NNNN09748797 NN       00349279"
    
    parser = W1Parser()
    record = parser._parse_da_permit(line)
    
    assert isinstance(record, DaPermitRecord)
    assert record.record_id == "02"
    assert record.permit_number == 911978 # 0911978
    assert record.sequence_number == 99
    assert record.county_code == 3 # 003
    assert record.lease_name.strip() == "SPDTX SWD"
    assert record.district == 10
    assert record.well_number.strip() == "17" # '  17  '
    assert record.total_depth == 5975
    assert record.operator_number == 900327
    assert record.type_application == "01"
    
    # Check some date fields
    assert record.received_date == "20251125"
    assert record.issued_date == "20251203"
    
    # Check flags
    assert record.p12_filed_flag == "N"
    
    # Check location fields
    assert record.surface_abstract.strip() == "782" # From '782   '
    assert record.surface_nearest_city.strip() == "ANDREWS"
    
    # Check API -- Last field
    # 503 is predicted start.
    # Line ends: ...00349279
    assert record.api_number == "00349279"
