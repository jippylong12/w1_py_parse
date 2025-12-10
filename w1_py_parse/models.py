from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import json

@dataclass
class RRCRecord:
    record_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

@dataclass
class Schema01Record(RRCRecord):
    status_number: int
    status_sequence_number: int
    county_code: int
    lease_name: str
    district: int
    operator_number: int
    converted_date_comp: str
    date_app_received: str
    operator_name: str
    hb1407_problem_flag: str
    status_of_app_flag: str
    not_enough_money_flag: str
    too_much_money_flag: str
    p5_problem_flag: str
    p12_problem_flag: str
    plat_problem_flag: str
    w1a_problem_flag: str
    other_problem_flag: str
    rule37_problem_flag: str
    rule38_problem_flag: str
    rule39_problem_flag: str
    no_money_flag: str
    permit_number: int
    issue_date: str
    withdrawn_date: str
    walkthrough_flag: str
    other_problem_text: str
    well_number: str
    built_from_old_master_flag: str
    status_renumbered_to: int
    status_renumbered_from: int
    application_returned_flag: str
    ecap_filing_flag: str

