#!/usr/bin/env python3
"""Actual model evaluations; no answer-key data enters the harness."""
import argparse
import datetime
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from romanwiki.runtime import ROOT
from romanwiki.harness import ask,Chat,save
from romanwiki.store import search


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--label',default='connected');parser.add_argument('--first-two',action='store_true');args=parser.parse_args()
    folder=ROOT/'results'/f'{args.label}-{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}'
    folder.mkdir(parents=True)
    results=[]
    questions=json.loads((ROOT/'evaluation/expectations.json').read_text())
    for test in questions[:2] if args.first_two else questions:
        print('ASK:',test['question'],flush=True)
        try:
            record=ask(test['question']);sections={p['section'] for p in record['retrieved']}
            assessment={'expected_sections':test['sections'],'retrieval_recall_pass':set(test['sections'])<=sections,
                        'expected_behavior':test['expectation'],'claim_review':'PENDING: compare each claim with its quoted evidence',
                        'status_check':record['answer']['status']==('answered' if test['sections'] else 'insufficient')}
            record['evaluation']=assessment;results.append({'id':test['id'],**assessment})
            print(record['display'],flush=True)
        except Exception as e:
            record={'question':test['question'],'error':str(e)};results.append({'id':test['id'],'error':str(e)})
            print('ERROR:',e,flush=True)
        (folder/(test['id']+'.json')).write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    if not args.first_two:
        chat=Chat();modes=[]
        for text in ['what can we do?','what can you help me with?','Draft a three-sentence museum-trip invitation. My budget is $45.','make that shorter']:
            print('CHAT:',text,flush=True)
            try:
                record=chat.turn(text);modes.append(record);print(record['display'],flush=True)
            except Exception as e:modes.append({'input':text,'error':str(e)})
        for text in ['What is my museum-trip budget?']:
            try:modes.append(ask(text))
            except Exception as e:modes.append({'input':text,'error':str(e)})
        modes.append({'mode':'search','query':'Nicomedia aqueduct','retrieved':search('Nicomedia aqueduct'),'generation_called':False})
        (folder/'mode-checks.json').write_text(json.dumps(modes,indent=2,ensure_ascii=False)+'\n')
    (folder/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
    print('EVIDENCE:',folder,flush=True)
    return int(any('error' in r or not r['retrieval_recall_pass'] or not r['status_check'] for r in results))

if __name__=='__main__':sys.exit(main())
