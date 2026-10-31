import json,os,re,urllib.request
AB="创 出 利 民 申 书 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 诗 箴 传 歌 赛 耶 哀 结 但 何 珥 摩 俄 拿 弥 鸿 哈 番 该 亚 玛 太 可 路 约 徒 罗 林前 林后 加 弗 腓 西 帖前 帖后 提前 提后 多 门 来 雅 彼前 彼后 约壹 约贰 约叁 犹 启".split()
NR={a:i+1 for i,a in enumerate(AB)}
C=os.path.join(os.path.dirname(__file__),'cache')
def chap(b,c):
    f=f'{C}/{b}_{c}.json'
    if not os.path.exists(f):
        u=f'https://api.getbible.net/v2/cus/{b}/{c}.json'
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'curl/8.0'}),timeout=30))
        json.dump({str(v['verse']):v['text'].strip() for v in d['verses']},open(f,'w'),ensure_ascii=False)
    return json.load(open(f))
def verses(ref):
    """ref like 创3:15 or 创12:1-3 or 申6:4-5"""
    m=re.match(r'^(\D+?)(\d+):(\d+)(?:-(\d+))?$',ref.strip())
    if not m: raise ValueError(ref)
    b,c,v1,v2=m[1],int(m[2]),int(m[3]),int(m[4] or m[3])
    ch=chap(NR[b],c)
    t=''.join(ch[str(v)] for v in range(v1,v2+1))
    t=re.sub(r'\s+','',t); t=re.sub(r'[A-Za-z]','',t)
    if t.count('「')!=t.count('」'): t=t.replace('「','').replace('」','')
    return t
if __name__=='__main__':
    for r in ['创3:15','创12:1-3','申6:4-5','出20:2']: print(r,verses(r))
