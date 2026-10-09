import unittest
from normalize_userscript import normalize, parse_metadata

SAFE='''// ==UserScript==\n// @name Project helper\n// @namespace https://example.invalid/\n// @version 1.2.3\n// @match https://chatgpt.com/*\n// @grant none\n// ==/UserScript==\nconsole.log('safe');\n'''
RISKY='''// ==UserScript==\n// @name Token helper\n// @namespace demo\n// @version 0.1\n// @match *://*/*\n// @grant GM_cookie\n// @grant unsafeWindow\n// @grant GM_xmlhttpRequest\n// @connect *\n// @require https://cdn.example.invalid/x.js\n// ==/UserScript==\nconst accessToken=localStorage.getItem('access_token');\neval('console.log(1)');\n'''

class NormalizeUserscriptTests(unittest.TestCase):
    def test_parse_repeated_metadata(self):
        meta=parse_metadata(RISKY)
        self.assertEqual(meta['grant'],['GM_cookie','unsafeWindow','GM_xmlhttpRequest'])
    def test_safe_is_local_low_risk(self):
        payload=normalize(SAFE,'platform:saas:chatgpt','greasyfork','2026-09-06T16:00:00Z')
        self.assertEqual(payload['resource']['augmentation']['risk_level'],'low')
        self.assertFalse(payload['resource']['publication']['radar_public'])
        self.assertEqual(payload['edge']['relation'],'augments')
        self.assertEqual(payload['observation']['kind'],'security')
    def test_risky_is_blocked(self):
        payload=normalize(RISKY,'platform:any','openuserjs','2026-09-06T16:00:00Z')
        aug=payload['resource']['augmentation']
        self.assertEqual(aug['risk_level'],'critical')
        self.assertEqual(aug['recommended_action'],'block')
        self.assertIn('GM_cookie',' '.join(aug['risk_reasons']))
        self.assertIn('eval()',' '.join(aug['risk_reasons']))

if __name__=='__main__': unittest.main()
