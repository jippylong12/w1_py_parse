from typing import List, Tuple, Union

# Field structure: (Name, Start Position (1-based), Length, Type)
# Types: 'int', 'str', 'date' (implicit in some cases, but sticking to basic types for parsing)
# We will treat everything as 'str' initially for safety, or 'int' where explicit.

# Manual Definitions:
# 02 RRC-TAPE-RECORD-ID PIC X(02). 1
# 05 DA-STATUS-NUMBER PIC 9(07). 3
# 05 DA-STATUS-SEQUENCE-NUMBER PIC 9(02). 10
# 05 DA-COUNTY-CODE PIC 9(03). 12
# 05 DA-LEASE-NAME PIC X(32). 15
# 05 DA-DISTRICT PIC 9(02). 47
# 05 DA-OPERATOR-NUMBER PIC 9(06). 49
# 05 DA-CONVERTED-DATE COMP PIC S9(08). 55 <- This is binary/packed? Manual says COMP.
#    Wait, "COMP PIC S9(08)" usually implies binary. However, in these flat files provided as text, 
#    often it's expanded or it's not actually binary in the text download. 
#    Looking at sample data:
#    Line 1: 01091197899003SPDTX ...
#    01 (ID)
#    0911978 (Status Number - 7 digits)
#    99 (Seq Num - 2 digits)
#    003 (County - 3 digits)
#    SPDTX SWD... (Lease Name)
#    The manual says DA-CONVERTED-DATE is at 55. 
#    Let's check the sample line around pos 55.
#    Line 1 chars 49-54 (6 chars) = '109003' (Operator Num?)
#    Char 55 starts... '27    20251125'...
#    Wait, let's trace carefully.
#    1: 01
#    3: 0911978 (7) -> DA-STATUS-NUMBER
#    10: 99 (2) -> DA-STATUS-SEQUENCE-NUMBER
#    12: 003 (3) -> DA-COUNTY-CODE
#    15: SPDTX SWD                       (32 chars) -> DA-LEASE-NAME
#    47: 10 (2) -> DA-DISTRICT
#    49: 900327 (6) -> DA-OPERATOR-NUMBER
#    55:    20251 (8??) -> DA-CONVERTED-DATE? 
#    The sample has "    2025" at pos 55? 
#    Let's counting chars manually or visually.
#    01 0911978 99 003 SPDTX SWD.......
#    Text: "01091197899003SPDTX SWD                       10900327    20251125"
#    01 (2)
#    0911978 (7)
#    99 (2)
#    003 (3)
#    SPDTX SWD                       (32) -> Ends at 15+32-1 = 46. Correct.
#    10 (2) -> 47-48. Correct.
#    900327 (6) -> 49-54. Correct. 
#    Pos 55: "    20251125"
#    The manual says "05 DA-CONVERTED-DATE COMP PIC S9(08) VALUE ZERO. 55"
#    AND "05 DA-DATE-APP-RECEIVED... 59" redfines it? Or follows it?
#    Wait, manual:
#    05 DA-CONVERTED-DATE COMP PIC S9(08) VALUE ZERO. 55
#    05 DA-DATE-APP-RECEIVED.
#    10 DA-APP-RCVD-CENTURY PIC X(02) VALUE SPACES. 59
#    10 DA-APP-RCVD-YEAR PIC X(02) VALUE SPACES. 61
#    ...
#    If DA-CONVERTED-DATE is COMP, it might be 4 bytes binary taking up "logical" 8 digits? 
#    BUT in the text file, we see "    2025" at 55?
#    Actually, reading further: "THIS IS DA-DATE-APP-RECEIVED IN A COMPACT FORMAT USED FOR PROGRAMMING PURPOSES."
#    Usually in these legacy RRC dumps, they expand COMP fields to text or spaces if it's a text file export.
#    Let's look at the sample: `10900327    20251125`
#    10 (Dist) 900327 (OpNum). Next is `    2025`.
#    Pos 55-58 is `    `. 
#    Pos 59-66 is `20251125`.
#    Manual says `DA-DATE-APP-RECEIVED` starts at 59.
#    So `DA-CONVERTED-DATE` at 55 is likely 4 spaces (ignored/padding in this text version) or it's a 4-byte generic filler in this text dump.
#    I will parse `DA-CONVERTED-DATE` as 4 bytes at 55, and `DA-DATE-APP-RECEIVED` as 8 bytes at 59.
    
#    Let's continue.
#    67: WATERBRIDGE STATELINE LLC       (32) -> DA-OPERATOR-NAME.
#    99: 0 (1) -> FILLER? Sample has '0'. Manual says FILLER PIC X(01) at 99.
#    100: 0 (1) -> DA-HB1407-PROBLEM-FLAG. Sample '0'.
#    101: A (1) -> DA-STATUS-OF-APP-FLAG. Sample 'A'.
#    102: N (1) -> DA-NOT-ENOUGH-MONEY-FLAG.
#    103: N (1) -> DA-TOO-MUCH-MONEY-FLAG.
#    104: N (1) -> DA-P5-PROBLEM-FLAG.
#    105: N (1) -> DA-P12-PROBLEM-FLAG.
#    106: N (1) -> DA-PLAT-PROBLEM-FLAG.
#    107: N (1) -> DA-W1A-PROBLEM-FLAG.
#    108: N (1) -> DA-OTHER-PROBLEM-FLAG.
#    109: N (1) -> DA-RULE37-PROBLEM-FLAG.
#    110: N (1) -> DA-RULE38-PROBLEM-FLAG.
#    111: N (1) -> DA-RULE39-PROBLEM-FLAG.
#    112: N (1) -> DA-NO-MONEY-FLAG.
#    113: 0911978 (7) -> DA-PERMIT. (Sample: 0911978)
#    120: 20251203 (8) -> DA-ISSUE-DATE. (Sample: 20251203)
#    128: 00000000 (8) -> DA-WITHDRAWN-DATE. 
#    136: N (1) -> DA-WALKTHROUGH-FLAG.
#    137:                      (20) -> DA-OTHER-PROBLEM-TEXT. (Sample: spaces)
#    157: 17  N (6?) -> DA-WELL-NUMBER. Sample `17  N0`? 
#         Wait, Sample around 157: "...00000N                      17  N000..."
#         Let's re-sync.
#         136 (Walkthrough) is 'N'.
#         137 (Other Problem Text) is 20 chars. Ends 156.
#         157 (Well Number) is 6 chars. Ends 162.
#         Sample at 157: `17  N0`... Wait.
#         Let's look at the sample text again.
#         `...00000N                      17  N000...`
#         The `N` before the spaces is likely 136.
#         Then 20 spaces (137-156).
#         Then `17  N0`. This looks like `17  ` (4 chars) then `N` then `0`? 
#         Well Number is 6 chars. `17  N0` is 6 chars? No "17  N" is 5.
#         Let's count spaces.
#         After 136 'N':
#         `                      ` (22 spaces?)
#         Manual: 137 (20 chars).
#         Sample check: `...0000N                      17  N...`
#         If current pos is 137. 20 chars -> 156.
#         Pos 157 starts `17`.
#         Visual check: `17  N`...
#         If Well Number is 6 chars: `17  N `? 
#         Manual at 163: DA-BUILT-FROM-OLD-MASTER-FLAG (1 char).
#         Manual at 164: renumbered to (9).
#         Manual at 173: renumbered from (9).
#         Manual at 182: app returned (1).
#         Manual at 183: ecap filing (1).
#         Manual at 184: Filler (29).
#         Manual at 187: RRC-TAPE-FILLER (324).
#         Wait, 184 + 29 = 213. 
#         But if next field is 187, then 184 is length 3.
#         I noted this in planning.
#         Let's assume text layout matches the explicit positions.

DA_ROOT_FIELDS = [
    ("record_id", 1, 2, "str"),
    ("status_number", 3, 7, "int"),
    ("status_sequence_number", 10, 2, "int"),
    ("county_code", 12, 3, "int"),
    ("lease_name", 15, 32, "str"),
    ("district", 47, 2, "int"),
    ("operator_number", 49, 6, "int"),
    ("converted_date_comp", 55, 4, "str"), # 4 bytes based on gap to 59
    ("date_app_received", 59, 8, "str"), # Century+Year+Month+Day
    ("operator_name", 67, 32, "str"),
    # ("filler_99", 99, 1, "str"),
    ("hb1407_problem_flag", 100, 1, "str"),
    ("status_of_app_flag", 101, 1, "str"),
    ("not_enough_money_flag", 102, 1, "str"),
    ("too_much_money_flag", 103, 1, "str"),
    ("p5_problem_flag", 104, 1, "str"),
    ("p12_problem_flag", 105, 1, "str"),
    ("plat_problem_flag", 106, 1, "str"),
    ("w1a_problem_flag", 107, 1, "str"),
    ("other_problem_flag", 108, 1, "str"),
    ("rule37_problem_flag", 109, 1, "str"),
    ("rule38_problem_flag", 110, 1, "str"),
    ("rule39_problem_flag", 111, 1, "str"),
    ("no_money_flag", 112, 1, "str"),
    ("permit_number", 113, 7, "int"),
    ("issue_date", 120, 8, "str"),
    ("withdrawn_date", 128, 8, "str"),
    ("walkthrough_flag", 136, 1, "str"),
    ("other_problem_text", 137, 20, "str"),
    ("well_number", 157, 6, "str"),
    ("built_from_old_master_flag", 163, 1, "str"),
    ("status_renumbered_to", 164, 9, "int"),
    ("status_renumbered_from", 173, 9, "int"),
    ("application_returned_flag", 182, 1, "str"),
    ("ecap_filing_flag", 183, 1, "str"),
    # Discrepancy handling:
    # Manual: 184 FILLER X(29). Next: 187.
    # We trust start positions. 187 - 184 = 3 bytes.
    # ("filler_184", 184, 3, "str"), 
    # ("tape_filler", 187, 324, "str"),
]
