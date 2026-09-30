import argparse
import json
import sys
from .runtime import WikiError,MODEL
from .harness import Chat,ask,save
from .store import search
from .ingest import ingest,approve,rename


def main():
    parser=argparse.ArgumentParser(prog='wiki',description='Roman Empire study buddy and local source research. Model: '+MODEL+'; loopback-only Ollama on port 11435.',epilog='Setup: scripts/start_ollama.sh, then explicitly pull weights while connected. Offline setup: pip install --no-index --find-links vendor -r requirements.txt. Errors distinguish missing originals, empty evidence, invalid citations and runtime failures. See README.md. Citation checks do not establish historical truth.')
    sub=parser.add_subparsers(dest='command')
    sub.add_parser('help',help='Show setup, commands and limitations')
    for command in ['ask','search']:
        p=sub.add_parser(command,help='Independent cited research' if command=='ask' else 'Original passages; no model required')
        p.add_argument('question');p.add_argument('--mode',choices=['local'],default='local')
    sub.add_parser('chat',help='Conversational study buddy; /notes QUESTION for evidence, /quit to exit')
    p=sub.add_parser('ingest',help='Preserve known originals, generate review drafts, update FTS index');p.add_argument('path');p.add_argument('--redraft',action='store_true')
    p=sub.add_parser('review',help='Accept a staged draft after checking its claims against sources');p.add_argument('key');p.add_argument('--approve',action='store_true',required=True)
    p=sub.add_parser('rename',help='Rename a reviewed note and update incoming links/mappings');p.add_argument('key');p.add_argument('title')
    args=parser.parse_args()
    try:
        if args.command in [None,'help']:parser.print_help()
        elif args.command=='ask':
            result=ask(args.question);print(result['display']);print('Saved:',result['record_path'])
        elif args.command=='search':
            rows=search(args.question);print(json.dumps(rows,indent=2,ensure_ascii=False));save({'mode':'search','query':args.question,'retrieved':rows,'retrieval_called':True,'generation_called':False})
        elif args.command=='ingest':print(json.dumps(ingest(args.path,args.redraft),indent=2))
        elif args.command=='review':print(approve(args.key))
        elif args.command=='rename':print(rename(args.key,args.title))
        elif args.command=='chat':
            chat=Chat();print('Clio • '+MODEL+' • local\n/notes QUESTION retrieves evidence; /quit exits. Recent context stays in this session.')
            while True:
                try:text=input('You> ')
                except EOFError:break
                if text.strip()=='/quit':break
                if not text.strip():continue
                try:print('Clio>',chat.turn(text)['display'])
                except WikiError as e:print('Error:',e,file=sys.stderr)
    except (WikiError,FileNotFoundError,ValueError) as e:
        save({'mode':args.command,'status':'error','error':str(e),'arguments':vars(args)})
        print('Error:',e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
