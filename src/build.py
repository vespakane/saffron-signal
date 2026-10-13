# Builds ../index.html from src.html + assets.json (run make_assets.py first if the screenshots change).
import json, re, os
here=os.path.dirname(os.path.abspath(__file__))
a=json.load(open(os.path.join(here,'assets.json')))
s=open(os.path.join(here,'src.html')).read()
missing=set(re.findall(r'\{\{(\w+)\}\}',s))-set(a)
assert not missing, missing
for k,v in a.items(): s=s.replace('{{%s}}'%k,v)
open(os.path.join(here,'..','index.html'),'w').write(s)
# artifact copy: no document wrapper (the artifact host adds its own)
art=re.sub(r'^<!doctype html>\n<html lang="en">\n<head>\n((<meta|<link)[^\n]*\n)+','',s)
art=art.replace('</head>\n<body>\n','').replace('</body>\n</html>\n','')
if os.environ.get('ARTIFACT_OUT'): open(os.environ['ARTIFACT_OUT'],'w').write(art)
print('index.html', len(s)//1024,'KB; artifact starts with:', art[:40].replace('\n',' '))
