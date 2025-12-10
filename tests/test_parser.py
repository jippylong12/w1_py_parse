import unittest
import os
from w1_py_parse import RRCParser, Schema01Record

class TestRRCParser(unittest.TestCase):
    def setUp(self):
        self.sample_file = os.path.join(os.path.dirname(__file__), '../sample_data.txt')

    def test_parse_sample_file(self):
        parser = RRCParser()
        parser.parse_file(self.sample_file)
        
        # Filter for schema 01 records
        records_01 = [r for r in parser.records if isinstance(r, Schema01Record)]
        
        # There are 2 '01' lines in the sample file
        self.assertEqual(len(records_01), 2)
        
        # Verify first record
        rec = records_01[0]
        
        self.assertEqual(rec.record_id, '01')
        self.assertEqual(rec.status_number, 911978)
        self.assertEqual(rec.status_sequence_number, 99)
        self.assertEqual(rec.county_code, 3)
        self.assertEqual(rec.lease_name, "SPDTX SWD")
        self.assertEqual(rec.district, 10)
        self.assertEqual(rec.operator_number, 900327)
        self.assertEqual(rec.date_app_received, "20251125")
        self.assertEqual(rec.operator_name, "WATERBRIDGE STATELINE LLC")
        
        # Partial flags check
        self.assertEqual(rec.status_of_app_flag, "A")
        self.assertEqual(rec.hb1407_problem_flag, "0") 
        
        self.assertEqual(rec.permit_number, 911978)
        self.assertEqual(rec.issue_date, "20251203")
        
        # Check Well Number - it had some confusing spacing in sample
        # "17  N" stripped might be "17  N" or "17" if N is separate?
        # My implementation strips whitespace.
        # "17  N" -> "17  N"
        self.assertEqual(rec.well_number, "17")
        self.assertEqual(rec.built_from_old_master_flag, "N")
        
    def test_json_export(self):
        parser = RRCParser()
        parser.parse_file(self.sample_file)
        json_output = parser.to_json()
        self.assertIn('"record_id": "01"', json_output)
        self.assertIn('"lease_name": "SPDTX SWD"', json_output)

if __name__ == '__main__':
    unittest.main()
