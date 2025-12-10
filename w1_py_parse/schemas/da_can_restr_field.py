from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)

DA_CAN_RESTR_FIELD_FIELDS = [
    ("record_id", 1, 2, "str"), # 07
    ("field_number", 3, 8, "str"),
    # Filler at 11 (len 5) -> ends 15?
    # Manual: 03 FILLER PIC 9(05). 11.
    # 02 RRC-TAPE-FILLER PIC X(0495). 16.
    # Ignoring fillers as requested.
]
