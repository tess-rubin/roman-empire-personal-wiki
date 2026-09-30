import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from romanwiki import sources,store,harness,runtime
from romanwiki.runtime import ROOT,WikiError

class SourceTests(unittest.TestCase):
    def test_unavailable_measurements_do_not_abort(self):
        with patch.object(runtime.psutil,'process_iter',side_effect=PermissionError('restricted')),patch.object(runtime.psutil,'swap_memory',side_effect=PermissionError('restricted')):
            sample=runtime.snapshot()
        self.assertIsNone(sample['swap'])
        self.assertEqual(sample['ollama_processes'],[])
        self.assertEqual(len(sample['measurement_errors']),2)

    def test_sections_and_originals(self):
        catalog=json.loads((ROOT/'config/sources.json').read_text())
        for source,info in catalog.items():
            path=ROOT/'vault/raw'/info['file']
            self.assertEqual(sources.checksum(path),info['sha256'])
            rows=sources.passages(source,path,info['sections'])
            self.assertEqual(set(r['section'].split(':')[1] for r in rows),set(info['sections']))
            self.assertEqual(len({r['id'] for r in rows}),len(rows))
            self.assertTrue(all(r['text'] for r in rows))
        pliny=sources.extract('pliny',ROOT/'vault/raw/pliny.html')
        self.assertIn('aqueduct',pliny[-2][2].lower())
        tacitus=sources.extract('tacitus',ROOT/'vault/raw/tacitus.html')
        self.assertTrue(tacitus[-1][2].endswith('cruelty, that they were being destroyed.'))
    def test_citation_failures(self):
        row={'id':'a:1:1','path':'vault/raw/a.html#1','text':'A sufficiently long quotation about power.'}
        answer={'status':'answered','claims':[{'text':'A claim','citations':[{'id':row['id'],'path':row['path'],'quote':row['text']}]}]}
        harness.validate(answer,[row])
        for field,value in [('id','fake'),('path','test/key.json'),('quote','This is invented evidence.')]:
            changed=json.loads(json.dumps(answer));changed['claims'][0]['citations'][0][field]=value
            with self.assertRaises(WikiError):harness.validate(changed,[row])
        with self.assertRaises(WikiError):harness.validate({'status':'answered','claims':[]},[row])
    def test_empty_is_not_runtime_error(self):
        with patch.object(harness,'search',return_value=[]),patch.object(harness,'save',return_value='test'),patch.object(harness,'generate') as gen:
            result=harness.ask('unmatched');gen.assert_not_called();self.assertEqual(result['answer']['status'],'insufficient')
        with patch.object(harness,'search',return_value=[{'text':'evidence'}]),patch.object(harness,'save'),patch.object(harness,'generate',side_effect=WikiError('Unavailable')):
            with self.assertRaisesRegex(WikiError,'Unavailable'):harness.ask('question')
    def test_chat_routing_and_context(self):
        def fake(messages,structured=False):return {'response':{'message':{'content':'Suggestion: a shorter plan.'}},'request':{'messages':messages}}
        chat=harness.Chat()
        with patch.object(harness,'generate',side_effect=fake),patch.object(harness,'save',return_value='test'),patch.object(harness,'search') as search:
            for q in ['what can we do?','Draft a museum plan with a $45 budget.','make that shorter']:
                result=chat.turn(q);self.assertFalse(result['retrieval_called'])
            search.assert_not_called();self.assertEqual(result['history_messages'],4)
        with patch.object(harness,'ask',return_value={'display':'cited'}) as ask:
            chat.turn('/notes aqueduct');ask.assert_called_once()
    def test_fts_only_source_evidence(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(store,'ROOT',Path(tmp)):
            raw=Path(tmp)/'vault/raw';raw.mkdir(parents=True);(raw/'a.html').write_text('source')
            store.index('a',[{'id':'a:1:1','source':'a','section':'a:1','path':'vault/raw/a.html','text':'Power and rank of magistrates.'}])
            self.assertEqual(len(store.search('power')),1)
            self.assertEqual(store.search('museum budget'),[])
            (raw/'a.html').unlink()
            with self.assertRaisesRegex(WikiError,'Missing original'):store.search('power')

if __name__=='__main__':unittest.main()
