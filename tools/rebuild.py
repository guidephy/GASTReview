"""Embed CONTENT.json in index.html. Python standard library only."""
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((root/'CONTENT.json').read_text())
encoded=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
p=root/'index.html'
s,n=re.subn(r'(<script id="card-data" type="application/json">)[\s\S]*?(</script>)',lambda m:m[1]+encoded+m[2],p.read_text(),count=1)
assert n==1
p.write_text(s)
print('Embedded teaching content updated.')
