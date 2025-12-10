from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)

DA_FIELD_BHL_FIELDS = [
    ("record_id", 1, 2, "str"), # 05
    ("bhl_section", 3, 8, "str"),
    ("bhl_block", 11, 10, "str"),
    ("bhl_abstract", 21, 6, "str"),
    ("bhl_survey", 27, 55, "str"),
    ("bhl_acres", 82, 8, "str"), # 6.2 digits -> 8 chars
    ("bhl_nearest_well", 90, 28, "str"),
    ("bhl_lease_feet_1", 118, 8, "str"),
    ("bhl_lease_direction_1", 126, 13, "str"),
    ("bhl_lease_feet_2", 139, 8, "str"),
    ("bhl_lease_direction_2", 147, 13, "str"),
    ("bhl_survey_feet_1", 160, 8, "str"),
    ("bhl_survey_direction_1", 168, 13, "str"),
    ("bhl_survey_feet_2", 181, 8, "str"),
    ("bhl_survey_direction_2", 189, 13, "str"),
    ("bhl_county", 202, 13, "str"), # Manual says 15 chars in description, but list says 13. Next starts at 215. 202+13=215. Trust list (13).
    ("bhl_pntrt_dist_1", 215, 8, "str"),
    ("bhl_pntrt_dir_1", 223, 13, "str"),
    ("bhl_pntrt_dist_2", 236, 8, "str"),
    ("bhl_pntrt_dir_2", 244, 13, "str"),
]
