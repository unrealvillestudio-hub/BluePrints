import re,json,glob,os
D=os.path.dirname(os.path.abspath(__file__))
urls={os.path.basename(u.strip()).replace('.pdf.pdf','.pdf'):u.strip() for u in open(D+'/urls.txt') if u.strip()}
HDR_ES=['DESCRIPCIÓN','MODO DE USO','PRECAUCIONES','PRESENTACIONES','TECNOLOGÍA','FÓRMULA','FORMULACIÓN']
out={}
for f in sorted(glob.glob(D+'/txt/*.txt')):
    L=open(f).read().split('\n')
    # columna de corte: posición de DESCRIPTION: en la línea que tiene DESCRIPCIÓN:
    split=None
    for l in L:
        m=re.search(r'\b(DESCRIPTION|DIRECTIONS):',l)
        if m and ('DESCRIPCIÓN' in l or 'MODO DE USO' in l): split=m.start(); break
    if split is None:
        for l in L:
            m=re.search(r'\bDESCRIPTION:',l)
            if m: split=m.start(); break
    es=[l[:split].rstrip() if split else l for l in L]
    en=[l[split:].strip() if split and len(l)>split else '' for l in L]
    def sections(lines, hdrs):
        sec={}; cur='_head'
        for l in lines:
            s=l.strip()
            m=re.match(r'^([A-ZÁÉÍÓÚÑ /]{3,}):\s*(.*)$',s)
            if m and len(m.group(1))<40:
                cur=m.group(1).strip(); sec.setdefault(cur,[])
                if m.group(2): sec[cur].append(m.group(2))
                continue
            if s: sec.setdefault(cur,[]).append(s)
        return {k:re.sub(r'\s+',' ',' '.join(v)).strip() for k,v in sec.items()}
    S_es=sections(es,None); S_en=sections(en,None)
    name=os.path.basename(f)[:-4]
    foot=[l.strip() for l in L if 'NEURONECOSMETICA.COM' in l]
    line=re.sub(r'.*NEURONECOSMETICA\.COM\s*','',foot[-1]).strip() if foot else None
    out[name]={'pdf':name+'.pdf','url':urls.get(name+'.pdf'),'line':line,'split':split,'es':S_es,'en':S_en}
json.dump(out,open(D+'/fichas.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items():
    print(k, v['split'], v['line'], sorted(v['es'].keys()))
