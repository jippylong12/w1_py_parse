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

class W1RecordGroup(dict):
    """
    A custom dictionary that represents a grouped record (hierarchical)
    and provides a .to_json() method.
    """
    def to_json(self) -> str:
        def default_serializer(obj):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            return str(obj)
        return json.dumps(self, default=default_serializer)

@dataclass
class DaRootRecord(RRCRecord):
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

@dataclass
class DaPermitRecord(RRCRecord):
    permit_number: int
    sequence_number: int
    county_code: int
    lease_name: str
    district: int
    well_number: str
    total_depth: int
    operator_number: int
    type_application: str
    other_explanation: str
    address_unique_number: int
    zip_code_prefix: str
    zip_code_suffix: str
    fiche_set_number: int
    onshore_county: int
    received_date: str
    issued_date: str
    amended_date: str
    extended_date: str
    spud_date: str
    surface_casing_date: str
    well_status: str
    well_status_date: str
    expired_date: str
    cancelled_date: str
    cancellation_reason: str
    p12_filed_flag: str
    substandard_acreage_flag: str
    rule_36_flag: str
    h9_flag: str
    rule_37_case_number: int
    rule_38_docket_number: int
    location_formation_flag: str
    surface_section: str
    surface_block: str
    surface_survey: str
    surface_abstract: str
    surface_acres: str
    surface_miles_from_city: str
    surface_direction_from_city: str
    surface_nearest_city: str
    surface_lease_feet_1: str
    surface_lease_direction_1: str
    surface_lease_feet_2: str
    surface_lease_direction_2: str
    surface_survey_feet_1: str
    surface_survey_direction_1: str
    surface_survey_feet_2: str
    surface_survey_direction_2: str
    nearest_well_feet: str
    nearest_well_direction: str
    nearest_well_format_flag: str
    final_update: str
    cancelled_flag: str
    spud_in_flag: str
    directional_well_flag: str
    sidetrack_well_flag: str
    moved_indicator: str
    permit_conv_issued_date: int
    rule_37_granted_code: str
    horizontal_well_flag: str
    duplicate_permit_flag: str
    nearest_lease_line: str
    api_number: str

@dataclass
class DaFieldRecord(RRCRecord):
    field_number: int
    field_application_well_code: str
    field_completion_well_code: str
    field_completion_code: str
    field_transfer_code: str
    field_validation_century: int
    field_validation_year: int
    field_validation_month: int
    field_validation_day: int
    field_completion_century: int
    field_completion_year: int
    field_completion_month: int
    field_completion_day: int
    field_rule37_flag: str
    field_rule38_flag: str

@dataclass
class DaFieldSpecificRecord(RRCRecord):
    field_district: int
    field_lease_name: str
    field_total_depth: int
    field_well_number: str
    field_acres: str

@dataclass
class DaFieldBhlRecord(RRCRecord):
    bhl_section: str
    bhl_block: str
    bhl_abstract: str
    bhl_survey: str
    bhl_acres: str
    bhl_nearest_well: str
    bhl_lease_feet_1: str
    bhl_lease_direction_1: str
    bhl_lease_feet_2: str
    bhl_lease_direction_2: str
    bhl_survey_feet_1: str
    bhl_survey_direction_1: str
    bhl_survey_feet_2: str
    bhl_survey_direction_2: str
    bhl_county: str
    bhl_pntrt_dist_1: str
    bhl_pntrt_dir_1: str
    bhl_pntrt_dist_2: str
    bhl_pntrt_dir_2: str

@dataclass
class DaCanRestrRecord(RRCRecord):
    restriction_key: int
    restriction_type: str
    restriction_remark: str
    restriction_flag: str

@dataclass
class DaCanRestrFieldRecord(RRCRecord):
    field_number: str

@dataclass
class DaFreeRestrRecord(RRCRecord):
    restriction_key: int
    restriction_type: str
    restriction_remark: str
    restriction_flag: str

@dataclass
class DaFreeRestrFieldRecord(RRCRecord):
    field_number: str

@dataclass
class DaPermitBhlRecord(RRCRecord):
    bhl_section: str
    bhl_block: str
    bhl_abstract: str
    bhl_survey: str
    bhl_acres: str
    bhl_nearest_well: str
    bhl_lease_feet_1: str
    bhl_lease_direction_1: str
    bhl_lease_feet_2: str
    bhl_lease_direction_2: str
    bhl_survey_feet_1: str
    bhl_survey_direction_1: str
    bhl_survey_feet_2: str
    bhl_survey_direction_2: str
    bhl_county: str
    bhl_pntrt_dist_1: str
    bhl_pntrt_dir_1: str
    bhl_pntrt_dist_2: str
    bhl_pntrt_dir_2: str

@dataclass
class DaAlternateAddressRecord(RRCRecord):
    address_key: str
    address_line: str

@dataclass
class DaRemarkRecord(RRCRecord):
    remark_sequence_number: int
    remark_date_century: int
    remark_date_year: int
    remark_date_month: int
    remark_date_day: int
    remark_line: str

@dataclass
class DaCheckRegisterRecord(RRCRecord):
    register_date_century: int
    register_date_year: int
    register_date_month: int
    register_date_day: int
    register_number: int
