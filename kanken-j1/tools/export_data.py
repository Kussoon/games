"""Python標準ライブラリのみ。Excelを正とし、検査後に公開問題を出力する。"""
import json,sys,pathlib,zipfile,xml.etree.ElementTree as ET,re
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
FIELDS={'R1':'読み','R2':'表外の読み','R3':'熟字訓・当て字','R4':'共通の漢字','W1':'書き取り','E1':'誤字訂正','Y1':'四字熟語','S1':'対義語・類義語','P1':'故事・諺','T1':'文章題'}
def read_xlsx(path):
 with zipfile.ZipFile(path) as z:
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   strings=[''.join(t.text or '' for t in e.findall('.//s:t',NS)) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  rel={e.attrib['Id']:e.attrib['Target'] for e in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  result={}
  for e in ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',NS):
   target=rel[e.attrib['{'+NS['r']+'}id']]; target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   rows=[]
   for row in ET.fromstring(z.read(target)).findall('s:sheetData/s:row',NS):
    cells={}
    for c in row.findall('s:c',NS):
     col=0
     for ch in re.match('[A-Z]+',c.attrib['r'])[0]:col=col*26+ord(ch)-64
     v=c.find('s:v',NS); value=v.text if v is not None else ''
     if c.attrib.get('t')=='s':value=strings[int(value)]
     elif c.attrib.get('t')=='inlineStr':value=''.join(t.text or '' for t in c.findall('.//s:t',NS))
     cells[col-1]=value
    if cells:rows.append(cells)
   if not rows:result[e.attrib['name']]=[];continue
   headers=[rows[0].get(i,'') for i in range(max(rows[0])+1)]
   result[e.attrib['name']]=[{h:r.get(i,'') for i,h in enumerate(headers) if h} for r in rows[1:] if r.get(0)]
  return result
def evaluate(t):
 errors=[]
 def index(sheet,key):
  result={}
  for r in t[sheet]:
   if r[key] in result:errors.append('重複ID '+r[key])
   result[r[key]]=r
  return result
 k=index('01_漢字マスター','kanji_id');v=index('02_語彙マスター','vocab_id');q=index('03_問題マスター','question_id')
 if len({r['漢字'] for r in k.values()})!=len(k):errors.append('漢字重複')
 kv={x:[] for x in v};qv={x:[] for x in q}
 for r in t['05_語彙漢字関係']:
  if r['vocab_id'] not in v or r['kanji_id'] not in k:errors.append('語彙漢字参照切れ '+str(r));continue
  kv[r['vocab_id']].append(r['kanji_id'])
 for r in t['06_問題語彙関係']:
  if r['vocab_id'] not in v or r['question_id'] not in q:errors.append('問題語彙参照切れ '+str(r));continue
  qv[r['question_id']].append(r['vocab_id'])
 seen=set();public=[];blocked=[]
 for r in q.values():
  reasons=[];sig=(r['分野'],r['問題文'],r['対象部分'],r['正解'])
  if sig in seen:errors.append('問題重複 '+r['question_id'])
  seen.add(sig)
  if r['分野'] not in FIELDS:errors.append('分野不正 '+r['question_id'])
  if r['vocab_id'] not in v:errors.append('主語彙参照切れ '+r['question_id'])
  if r['公開可']!='○':reasons.append('問題公開可が○でない')
  for x in ['重複チェック','範囲チェック','正答チェック','例文チェック','著作権チェック']:
   if r[x]!='済':reasons.append(x+'未完了')
  if not r['問題文'] or not r['正解']:reasons.append('問題文／正解空欄')
  if r['出題形式'] not in ['入力','4択','自己採点']:reasons.append('出題形式不正')
  if str(r['難度']) not in ['1','2','3','4','5']:reasons.append('難度不正')
  if r['本番重要度'] not in ['A','B','C']:reasons.append('重要度不正')
  if r['出題形式']=='4択':
   choices=[r['正解']]+[r['誤答候補'+str(n)] for n in range(1,4)]
   if len(set(choices))!=4 or not all(choices):reasons.append('4択不成立')
  if not qv[r['question_id']] or r['vocab_id'] not in qv[r['question_id']]:reasons.append('問題語彙関係欠落')
  for vid in set(qv[r['question_id']]):
   vr=v[vid]
   if any(vr[x]!=y for x,y in [('公開可','○'),('公式範囲確認','済'),('辞書確認','済')]) or not vr['確認資料']:reasons.append(vid+' 語彙確認未完了')
   actual={c for c in vr['表記'] if re.match('[一-鿿]',c)}
   linked={k[kid]['漢字'] for kid in kv[vid]}
   if not actual.issubset(linked):reasons.append(vid+' 漢字関係欠落')
   for kid in kv[vid]:
    kr=k[kid]
    if kr['公開可']!='○' or kr['公式確認']!='済' or not all(kr[x] for x in ['標準字体','公式資料','公式頁','確認日']):reasons.append(kid+' 正本確認未完了')
  if reasons:blocked.append({'question_id':r['question_id'],'requested_public':r['公開可']=='○','reasons':list(dict.fromkeys(reasons))});continue
  public.append({'question_id':r['question_id'],'vocab_ids':list(dict.fromkeys(qv[r['question_id']])),'field':r['分野'],'format':r['出題形式'],'prompt':r['問題文'],'target':r['対象部分'],'answers':[r['正解']],'answer_reading':r['正解読み'],'distractors':[r['誤答候補'+str(n)] for n in range(1,4)] if r['出題形式']=='4択' else [],'explanation':r['解説'],'mnemonic':r['覚え方'],'difficulty':int(r['難度']),'priority':r['本番重要度']})
 return public,{'counts':{'kanji':len(k),'vocab':len(v),'questions':len(q),'public':len(public)},'field_counts':{f:sum(r['分野']==f for r in q.values()) for f in FIELDS},'structural_errors':errors,'blocked':blocked}
def main():
 base=pathlib.Path(__file__).resolve().parents[1];path=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else base/'kanken-jun1-master-v0.1.xlsx'
 t=read_xlsx(path);public,audit=evaluate(t)
 output=base/'data';output.mkdir(exist_ok=True)
 (output/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 # 公開可○を誤設定した場合は既存公開JSONも空にし、失敗として終了する。
 failed=bool(audit['structural_errors'] or any(r['requested_public'] for r in audit['blocked']))
 if failed:public=[]
 (output/'public-questions.json').write_text(json.dumps({'schema_version':'1.0','questions':public},ensure_ascii=False,indent=2))
 print(json.dumps(audit['counts'],ensure_ascii=False));print('構造エラー',len(audit['structural_errors']))
 if failed:raise SystemExit('公開条件違反：公開JSONは空で出力しました。audit.jsonを確認してください。')
if __name__=='__main__':main()
