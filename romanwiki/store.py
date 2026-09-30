import contextlib
import json
import re
import sqlite3
from .runtime import ROOT,WikiError
from .sources import attribution

STOP=set('a an the is are was were do did does how why what when where who which with to of in on for and or by from his her their me my it its this that according after people please wiki notes exactly'.split())
# General vocabulary expansion, not question/answer lookup. FTS indexes only original text.
EXPAND={'help':['relieve','supplies'],'homeless':['destitute','shelter'],
        'aqueduct':['aqueducts'],'specialist':['engineer','architect'],'fire':['conflagration'],
        'power':['rank','magistracy'],'died':['deaths','life']}

@contextlib.contextmanager
def connect():
    (ROOT/'data').mkdir(exist_ok=True)
    c=sqlite3.connect(ROOT/'data/evidence.sqlite');c.row_factory=sqlite3.Row
    c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS passages USING fts5(id UNINDEXED, source UNINDEXED, section UNINDEXED, path UNINDEXED, text, tokenize='porter unicode61')")
    try:
        with c:
            yield c
    finally:
        c.close()


def index(source,rows):
    with connect() as c:
        c.execute('DELETE FROM passages WHERE source=?',(source,))
        c.executemany('INSERT INTO passages VALUES(:id,:source,:section,:path,:text)',rows)


def search(question,limit=4):
    words=[w for w in re.findall(r'[a-zA-Z0-9]+',question.lower()) if w not in STOP]
    words=list(dict.fromkeys(words+[v for w in words for v in EXPAND.get(w,[])]))[:40]
    if not words:return []
    query=' OR '.join('"'+w+'"' for w in words)
    scoped=[]
    for source,names in {'augustus':['augustus'], 'tacitus':['tacitus','nero'], 'pliny':['pliny','trajan']}.items():
        if any(re.search(r'\b'+name+r'\b',question,re.I) for name in names):scoped.append(source)
    scope=' AND source IN ('+','.join('?' for _ in scoped)+')' if scoped else ''
    with connect() as c:
        rows=c.execute('SELECT *,bm25(passages) AS score FROM passages WHERE passages MATCH ?'+scope+' ORDER BY score,id LIMIT ?', (query,*scoped,limit)).fetchall()
    found=[dict(row) for row in rows]
    for row in found:
        row['attribution']=attribution(row['source'],row['section'].split(':')[1])
        if not (ROOT/row['path'].split('#')[0]).is_file():raise WikiError(f"Missing original: {row['path']}. Restore it and re-ingest.")
    return found
