from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)

DA_FREE_RESTR_FIELD_FIELDS = [
    ("record_id", 1, 2, "str"), # 09
    ("field_number", 3, 8, "str"),
    # Filler at 11 (len 5)
    # Tape filler 495 bytes at 16
    # Ignoring fillers.
]
