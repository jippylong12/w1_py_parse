import unittest
import os
from w1_py_parse import W1Parser, DaRootRecord

class TestW1Parser(unittest.TestCase):
    def setUp(self):
        self.sample_file = os.path.join(os.path.dirname(__file__), '../sample_data.txt')

    def test_parse_sample_file(self):
        parser = W1Parser()
        parser.parse_file(self.sample_file)
        
        # Filter for schema 01 (DaRoot) records
        records_01 = [r for r in parser.records if isinstance(r, DaRootRecord)]
        
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
        
        self.assertEqual(rec.well_number, "17")
        self.assertEqual(rec.built_from_old_master_flag, "N")
        
    def test_json_export(self):
        parser = W1Parser()
        parser.parse_file(self.sample_file)
        json_output = parser.to_json()
        self.assertIn('"record_id": "01"', json_output)
        self.assertIn('"lease_name": "SPDTX SWD"', json_output)

    def test_schema_filtering(self):
        parser = W1Parser()
        # Parse only DAROOT (01)
        parser.parse_file(self.sample_file, schemas=['DAROOT'])
        self.assertEqual(len(parser.records), 2)
        self.assertTrue(all(r.record_id == '01' for r in parser.records))
        
        # Parse only a non-existent schema in this file (e.g. 02)
        parser2 = W1Parser()
        parser2.parse_file(self.sample_file, schemas=['DAPERMIT']) # 02
        self.assertEqual(len(parser2.records), 0)
        
        # Parse by ID
        parser3 = W1Parser()
        parser3.parse_file(self.sample_file, schemas=['01'])
        self.assertEqual(len(parser3.records), 2)

if __name__ == '__main__':
    unittest.main()
