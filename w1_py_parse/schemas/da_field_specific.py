from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)

DA_FIELD_SPECIFIC_FIELDS = [
    ("record_id", 1, 2, "str"), # 04
    ("field_district", 3, 2, "int"),
    ("field_lease_name", 5, 32, "str"),
    ("field_total_depth", 37, 5, "int"),
    ("field_well_number", 42, 6, "str"),
    ("field_acres", 48, 8, "str"), # Adjusted position from 46 to 48
    ("filler", 56, 17, "str"),
    ("tape_filler", 73, 453, "str"), # Based on "02 RRC-TAPE-FILLER PIC X(0453). 58". Wait.
    # Manual: 03 FILLER PIC X(17) VALUE ZEROS. 56 -> Ends 56+17-1 = 72.
    # Manual: 02 RRC-TAPE-FILLER PIC X(0453). 58.
    # Discrepancy again? 
    # 56 + 17 = 73. So next starts at 73.
    # Manual says "58". That would overlap massively with the filler at 56.
    # Pos 58 vs 73.
    # If Filler is at 56 (len 17), it ends at 72.
    # RRC-TAPE-FILLER is likely the rest of the record.
    # I will stick to contiguous: 73. 
]
