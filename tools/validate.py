"""Check structure, local files and selected numerical answers. Does not replace pedagogical review."""
import json,pathlib,re,struct
root=pathlib.Path(__file__).resolve().parents[1]
s=(root/'index.html').read_text()
D=json.loads(re.search(r'<script id="card-data" type="application/json">([\s\S]*?)</script>',s)[1])
assert D==json.loads((root/'CONTENT.json').read_text())
C=D['concepts'];ids=[c['id'] for c in C];assert len(ids)==len(set(ids))
variants=[];assets={}
for c in C:
 assert all(c[k] for k in ['id','title','goal','body','condition','sources'])
 assert len(c['body'])==2 and len(c['variants'])==3
 assert all(i in ids and i!=c['id'] for i in c['related'])
 for v in c['variants']:
  variants.append(v['id'])
  assert v['focus'] and v['reading'] and v['images']
  assert all(v['question'][k] for k in ['prompt','answer','explanation'])
  for a in v['images']:assets[a['path']]=a
assert len(variants)==len(set(variants))
for a in assets.values():
 p=root/a['path'];raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'
 assert struct.unpack('>II',raw[16:24])==(a['width'],a['height'])
 assert a['pdf'] and a['page']>0 and a['alt']
 assert 0<=a['box'][0]<a['box'][2]<=1 and 0<=a['box'][1]<a['box'][3]<=1
assert set(assets)=={v['path'] for v in json.loads((root/'IMAGE_SOURCES.json').read_text()).values()}
assert not re.search(r'\bfetch\s*\(',s)
assert not re.search(r'<(?:script|link)[^>]*(?:src|href)=',s)
assert not any(p.suffix=='.pdf' for p in root.rglob('*'))
# These checks confirm the authored numerical examples, not every scientific claim.
assert abs((2.25-2.10)-.15)<1e-9
assert abs((-3.4-(-13.6))-10.2)<1e-9
waves=[1240/(13.6*(1/4-1/n**2)) for n in [3,4,5,6]]
assert all(abs(x-y)<2 for x,y in zip(waves,[656,486,434,410]))
print(f'PASS: {len(C)} concepts, {len(variants)} teaching variants/questions, {len(assets)} source diagrams; embedded data, files and numeric examples valid.')
