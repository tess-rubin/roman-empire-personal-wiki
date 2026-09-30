#!/usr/bin/env python3
"""Apply source-checked editorial revisions to EXISTING Gemma drafts only.
The original model responses remain in results/runs; this never fabricates model output.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from romanwiki.runtime import ROOT
from romanwiki.ingest import approve,load_state

EDITS={
'augustan-authority':(
'Augustus presents his supremacy as precedence in rank alongside formal equality with colleagues in office.',[
'In Res Gestae 34, Augustus says that after ending civil war he transferred control to the senate and Roman people during his sixth and seventh consulships. This is his own account, not independent proof of restored republican government. [augustus:34:1]',
'He claims precedence over everyone in rank, but no more power than his colleagues in any magistracy. The distinction is between standing and the formal power of an office. [augustus:34:1]',
'He reports receiving the title Father of his Country during his thirteenth consulship. [augustus:35:1]']),
'augustan-diplomacy':(
'Augustus depicts foreign rulers as seeking Roman friendship and his personal assistance.',[
'He lists kings who took refuge with him and says Phrates sent children and grandchildren to Italy as pledges of friendship, rather than after military defeat. [augustus:32:1]',
'He says Parthian and Median envoys received the kings they requested from him. The account emphasizes his role in royal appointments. [augustus:33:1]']),
'imperial-public-works':(
'The appended summary of the Res Gestae presents construction, restoration, and expenditure as imperial benefactions.',[
'The summary lists temples, the senate-house, the Augustan Forum, the Basilica Julia, and the theatre of Marcellus among new works. It speaks of Augustus in the third person. [augustus:S2:1]',
'It lists restoration of sacred buildings, the theatre of Pompey, aqueducts, and the Flaminian Way. [augustus:S3:1]',
'It reports 600,000,000 denarii contributed to the treasury, Roman plebs, or discharged soldiers; this is an attributed total, not an independently audited budget. [augustus:S1:1]',
'It also mentions spectacles and gifts to cities affected by earthquakes or fires, as well as individuals. The naval combat here is a spectacle; it should not be generalized into military expenditure. [augustus:S4:1]']),
'great-fire':(
'Tacitus describes a destructive fire, emergency relief, and continuing suspicion of Nero; he leaves the cause uncertain.',[
'Tacitus says authors offered conflicting accounts of whether the fire was accidental or contrived by the emperor. His report does not establish Nero’s responsibility. [tacitus:38:1]',
'He reports that Nero opened the Campus Martius, Agrippa’s public buildings, and his own gardens; erected temporary shelters; brought food from Ostia and nearby towns; and lowered the corn price to three sesterces a peck. [tacitus:39:1]',
'The story that Nero sang of Troy while Rome burned is explicitly a rumour in this account. [tacitus:39:1]',
'Tacitus reports punishment of Christians as Nero’s response to suspicion. His hostile characterization reflects his account, not a neutral description of that community. These chapters give no exact fire death toll. [tacitus:44:1]']),
'rebuilding':(
'Tacitus contrasts Nero’s new mansion with regulations intended to make the rebuilt city more orderly and resistant to fire.',[
'Tacitus describes Nero’s mansion and the ambitious engineering projects of Severus and Celer. [tacitus:42:1]',
'He describes measured streets, broader thoroughfares, limits on building height, open spaces, and colonnades; Nero promised to pay for the colonnades. [tacitus:43:1]',
'He reports fire-resistant stone construction, better public water access, equipment for stopping fires, and separate building walls. He also records criticism that the open streets increased exposure to heat. [tacitus:43:1] [tacitus:43:2]']),
'provincial-oversight':(
'Pliny and Trajan’s correspondence connects urban safety with the emperor’s concern about organized associations.',[
'After a fire at Nicomedia, Pliny reports missing firefighting equipment and proposes a company of 150 firemen. His criticism of bystanders is his interpretation. [pliny:XLII:1]',
'Trajan rejects the association because he fears factional assemblies. He favors equipment, assistance from householders, and help from the populace when necessary. [pliny:XLIII:1]',
'Letters XLIV–XLV record the renewal of vows for Trajan’s welfare and his acknowledgment, showing a different, ceremonial aspect of provincial correspondence. [pliny:XLIV:1] [pliny:XLV:1]']),
'nicomedia':(
'Pliny asks for technical help after failed aqueduct projects; Trajan also demands an investigation of wasted expenditure.',[
'Pliny reports two costly, unfinished attempts to build an aqueduct. He identifies a spring and proposes reusing stones and using brick for part of the work. [pliny:XLVI:1]',
'He requests an architect or someone skilled in waterworks so the new project does not repeat earlier failures. [pliny:XLVI:1]',
'Trajan requires provision of water and an inquiry into whose misconduct caused the waste. He raises concern about money being diverted to private purposes and asks Pliny to report the findings; the letter does not establish who was guilty. [pliny:XLVII:1]'])}

if __name__=='__main__':
    state=load_state();log=[]
    for key,mapping in state['notes'].items():
        if not mapping.get('staged'):continue
        p=ROOT/mapping['staged'];old=p.read_text();summary,details=EDITS[key]
        start=old.index('## Summary');end=old.index('## Local sources')
        revised=old[:start]+'## Summary\n\n'+summary+'\n\n## Supported details\n\n'+'\n\n'.join('- '+d for d in details)+'\n\n'+old[end:]
        revised=revised.replace('../../../vault/raw/','../../raw/')
        if 'Open the unchanged original HTML' not in revised:
            source=revised.split('source_id: ')[1].splitlines()[0]
            revised=revised.replace('## Local sources\n\n',f'## Local sources\n\n[[raw/{source}.html|Open the unchanged original HTML]] (open externally if prompted).\n\n')
        p.write_text(revised)
        log.append({'key':key,'draft_record':mapping['draft_record'],'action':'Editorial revision checked against original sections; original output retained','path':approve(key)})
    dest=ROOT/'results'/('note-review-'+str(__import__('time').time_ns())+'.json');dest.write_text(json.dumps(log,indent=2)+'\n');print(dest)
