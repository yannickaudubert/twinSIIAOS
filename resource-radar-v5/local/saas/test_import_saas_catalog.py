import json, tempfile, unittest
from pathlib import Path
from import_saas_catalog import import_catalog, write_records

CATALOG={"schema":"siiaos.saas-augmentation-catalog.v0.2","items":[{"id":"platform:saas:example","kind":"platform","title":"Example SaaS","capabilities":["documents"],"state":"observed","control_profile":{"ownership_model":"proprietary_saas","strategies":["augment","mirror"],"scores":{"augmentability":80,"reversibility":60,"governance":80,"siiaos_control":72,"lock_in":40}},"publication":{"local":True,"radar_public":False,"consultant_site":False,"visibility":"local_shared"}}]}

class SaaSCatalogTests(unittest.TestCase):
    def test_import_stays_local_and_scored(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'catalog.json'; src.write_text(json.dumps(CATALOG),encoding='utf-8')
            records=import_catalog(src); self.assertEqual(len(records),1); self.assertFalse(records[0]['publication']['radar_public']); self.assertEqual(records[0]['control_profile']['scores']['augmentability'],80)
    def test_writer_produces_canonical_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'catalog.json'; src.write_text(json.dumps(CATALOG),encoding='utf-8'); records=import_catalog(src); out=Path(tmp)/'out'; write_records(records,out); files=list(out.glob('*.json')); self.assertEqual(len(files),1); self.assertIn('control_profile',json.loads(files[0].read_text()))
    def test_rejects_public_seed(self):
        bad=json.loads(json.dumps(CATALOG)); bad['items'][0]['publication']['radar_public']=True
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'bad.json'; src.write_text(json.dumps(bad),encoding='utf-8')
            with self.assertRaises(ValueError): import_catalog(src)

if __name__=='__main__': unittest.main()
