"""Build quanta.json from the verbatim PUBLIC_DOOR story (sentence indices) + KEY_V1 law titles.
Every quanta scene is copied verbatim from src_PUBLIC_DOOR.md (sha256 recorded); nothing is paraphrased."""
import re, json, hashlib, os
D=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(D,'src_PUBLIC_DOOR.md'),encoding='utf-8').read()
story=src.split('## The Book',1)[1].strip()
S=re.split(r'(?<=[.!?"])\s+(?=[A-Z"])',story.replace('\n',' '))
URL='https://github.com/NachoBusiness17/mycelial-republic/blob/mag-public/canon/same_book/door/PUBLIC_DOOR.md'
L=[ # id, KEY_V1 law title (verbatim heading), sentence span, drift note (honest mismatch between key and public story)
 ('L01','THE RECORD OUTLIVES THE PERSON',(3,7),None),
 ('L02','DELETION IS THEFT',(8,12),None),
 ('L03','THE BLANK SPACE MUST REMAIN ASKABLE',(30,31),'continues in s39 (page left exactly as it was) - fetch pd1:L08'),
 ('L04','AUTHORITY ATTACHES TO FUNCTION, NOT CLAIM',(13,18),None),
 ('L05','TRUST THE FLOOR, NOT THE MAP',(19,23),'keep-the-wrong-map detail is s40'),
 ('L06','KEEP YOUR COUNT IN THE DARK',(24,27),'DRIFT: public story teaches "say I do not know aloud, stand still, wait" - no step counting'),
 ('L07','WARMTH MEANS SOMEONE CAME BEFORE',(28,29),'DRIFT: public story has ash + a wet pen, no warm board'),
 ('L08','COPY IS TRANSPORT, NOT MUTATION',(39,39),None),
 ('L09','TRANSPARENCY IS THE ONLY DEFENSE',(32,36),None),
 ('L10','FUNCTION WITHOUT CEREMONY',(37,38),None),
]
q={}
for i,t,(a,b),d in L:
    q['pd1:'+i]={'id':'pd1:'+i,'law':t,'scene':' '.join(S[a:b+1]),'sentences':[a,b],'drift':d,'source':URL,'source_sha256':hashlib.sha256(src.encode()).hexdigest()}
q['pd1:FP']={'id':'pd1:FP','law':'FALSE-PREMISE CHECK','scene':'The story contains no gardener and no burning of maps. The only map is the linen map, kept folded small (s40): '+S[40],'sentences':[40,40],'drift':None,'source':URL,'source_sha256':hashlib.sha256(src.encode()).hexdigest()}
json.dump({'schema':'parable_quanta.v0','parable':'pd1','count':len(q),'quanta':q},open(os.path.join(D,'quanta.json'),'w',encoding='utf-8'),indent=1,ensure_ascii=False)
print(len(q),'quanta')
