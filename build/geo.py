# -*- coding: utf-8 -*-
"""地中海东部真实底图（Natural Earth 公有领域数据，构建时投影为静态 SVG，无 CDN）+ 叠加层（城市、路线、书信路线）。"""
import json, math, os
from shapely.geometry import shape, box
NE = "/workspace/ne"
BBOX = (10.5, 40.5, 29.8, 43.6)   # lon0, lon1, lat0, lat1
W = 1200
lo0, lo1, la0, la1 = BBOX
MID = (la0 + la1) / 2
SX = W / (lo1 - lo0); SY = SX / math.cos(math.radians(MID)); H = round((la1 - la0) * SY)
def P(lon, lat): return ((lon - lo0) * SX, (la1 - lat) * SY)

C = {  # key: (中文名, lon, lat, dx, dy, anchor)
 "jerusalem":("耶路撒冷",35.23,31.78,10,16,"start"), "antioch":("叙利亚的安提阿",36.16,36.20,10,-6,"start"), "tarsus":("大数",34.90,36.92,8,-8,"start"),
 "damascus":("大马士革",36.29,33.51,10,4,"start"), "caesarea":("凯撒利亚",34.89,32.50,-10,4,"end"), "salamis":("撒拉米",33.90,35.18,8,-8,"start"),
 "paphos":("帕弗",32.41,34.76,-8,14,"end"), "perga":("别加",30.85,36.96,6,16,"start"), "pantioch":("彼西底的安提阿",31.19,38.31,-8,-8,"end"),
 "iconium":("以哥念",32.49,37.87,8,-6,"start"), "lystra":("路司得",32.36,37.58,-8,12,"end"), "derbe":("特庇",33.36,37.35,8,12,"start"),
 "troas":("特罗亚",26.16,39.75,-8,4,"end"), "philippi":("腓立比",24.29,41.01,6,-10,"start"), "thessalonica":("帖撒罗尼迦",22.94,40.64,-8,-8,"end"),
 "berea":("庇哩亚",22.20,40.52,-8,12,"end"), "athens":("雅典",23.73,37.98,6,14,"start"), "corinth":("哥林多",22.88,37.91,-8,-6,"end"),
 "ephesus":("以弗所",27.34,37.94,-8,10,"end"), "miletus":("米利都",27.28,37.53,-8,14,"end"), "colossae":("歌罗西",29.26,37.79,8,14,"start"),
 "laodicea":("老底嘉",29.11,37.84,-6,-8,"end"), "rome":("罗马",12.48,41.89,8,-8,"start"), "crete":("克里特（革哩底）",24.95,35.20,0,26,"middle"),
 "malta":("米利大（马耳他）",14.40,35.90,0,22,"middle"), "syracuse":("叙拉古",15.29,37.08,8,4,"start"), "puteoli":("部丢利",14.12,40.82,8,12,"start"),
 "nicopolis":("尼哥波立",20.73,39.01,-8,4,"end"), "pontus":("本都（阿米苏斯）",36.33,41.29,-8,-8,"end"), "cappadocia":("加帕多家",35.48,38.72,8,4,"start"),
 "bithynia":("庇推尼（尼哥米底亚）",29.92,40.77,0,-12,"middle"), "ancyra":("安卡拉（北加拉太）",32.85,39.93,8,4,"start"), "patmos":("拔摩",26.55,37.31,-6,12,"end"),
 "alexandria":("亚历山大",29.92,31.20,0,18,"middle"), "smyrna":("士每拿",27.14,38.42,-8,4,"end"), "pergamum":("别迦摩",27.18,39.12,-8,-4,"end"), "thyatira":("推雅推喇",27.84,38.91,8,-4,"start"),
 "sidon":("西顿",35.37,33.56,-8,0,"end"), "myra":("每拉",29.98,36.26,0,16,"middle"), "tyre":("推罗",35.20,33.27,-8,10,"end"),
}
WP = {"seleucia":(35.93,36.12),"attalia":(30.70,36.89),"neapolis":(24.41,40.94),"amphipolis":(23.85,40.82),"cenchreae":(22.99,37.88),
      "assos":(26.34,39.49),"cos":(27.29,36.89),"rhodes":(28.22,36.44),"patara":(29.32,36.26),"ptolemais":(35.08,32.92),"cnidus":(27.37,36.69),
      "fairhavens":(24.80,34.93),"rhegium":(15.65,38.11),"sea1":(31.0,35.2),"sea2":(27.5,35.6),"sea3":(20.0,35.5),"crete_s":(23.6,34.6),"sea4":(33.5,34.3),"sea5":(25.0,38.6),"sea6":(25.5,37.2)}
def ll(k):
    if k in C: return C[k][1], C[k][2]
    return WP[k]
JOURNEYS = [
 ("j1","第一次宣教旅行（徒13–14，约46–48）","#f5b942",["antioch","seleucia","salamis","paphos","perga","pantioch","iconium","lystra","derbe","lystra","iconium","pantioch","perga","attalia","sea4","antioch"]),
 ("j2","第二次宣教旅行（徒15:36–18:22，约49–52）","#4fb3ff",["antioch","tarsus","derbe","lystra","iconium","pantioch","troas","neapolis","philippi","amphipolis","thessalonica","berea","athens","corinth","cenchreae","sea6","ephesus","sea2","sea1","caesarea","jerusalem","antioch"]),
 ("j3","第三次宣教旅行（徒18:23–21:17，约52–57）","#3fd39a",["antioch","tarsus","derbe","lystra","iconium","pantioch","ephesus","troas","philippi","thessalonica","berea","corinth","berea","thessalonica","philippi","troas","assos","miletus","cos","rhodes","patara","tyre","ptolemais","caesarea","jerusalem"]),
 ("j4","押解往罗马（徒27–28，约59–60）","#ff6b8b",["caesarea","sidon","myra","cnidus","fairhavens","crete_s","sea3","malta","syracuse","rhegium","puteoli","rome"]),
]
REGIONS = [("意大利",15.6,41.3),("马其顿",21.6,41.35),("亚该亚",21.9,37.2),("亚细亚",28.6,38.7),("加拉太",32.6,38.9),("庇推尼",31.0,40.3),("本都",37.9,40.7),
           ("加帕多家",36.4,38.0),("基利家",35.6,37.4),("叙利亚",37.6,35.1),("犹太",34.9,30.9),("地 中 海",18.8,33.4),("爱琴海",25.0,39.3),("黑 海",33.5,42.6),("埃及",31.5,30.2),("吕家河谷",29.6,37.3)]

def _ring(coords, tol):
    out=[]; lx=ly=None
    for lon,lat in coords:
        x,y=P(lon,lat)
        if lx is None or abs(x-lx)+abs(y-ly)>=tol: out.append((x,y)); lx,ly=x,y
    return out
def _d(rings, close=True):
    s=[]
    for r in rings:
        if len(r)<(3 if close else 2): continue
        s.append("M"+" ".join(f"{x:.1f},{y:.1f}" for x,y in r)+("Z" if close else ""))
    return "".join(s)
def base_svg(path):
    B=box(lo0-1,la0-1,lo1+1,la1+1)
    def polys(name, minarea):
        rings=[]
        for f in json.load(open(f"{NE}/{name}.geojson"))["features"]:
            g=shape(f["geometry"])
            if not g.intersects(B): continue
            g=g.intersection(B).simplify(0.6/SX)
            gs=getattr(g,"geoms",[g])
            for p in gs:
                if p.geom_type!="Polygon" or p.area<minarea: continue
                rings.append(_ring(p.exterior.coords,0.9))
        return rings
    land=polys("ne_50m_land",(2.5/SX)**2)
    lakes=polys("ne_50m_lakes",(6/SX)**2)
    rv=[]
    keep={"Nile","Rosetta Branch","Damietta Branch","Jordan","Euphrates","Firat","Al Furat","Tigris","Dicle","Tevere","Po","Danube","Kiz?lirmak","Byk Menderes","Sakarya","Haliacmon","Evros","Strymnas","Ceyhan"}
    for f in json.load(open(f"{NE}/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        if f["properties"].get("name") not in keep: continue
        g=shape(f["geometry"])
        if not g.intersects(B): continue
        g=g.intersection(B).simplify(0.8/SX)
        for ln in getattr(g,"geoms",[g]):
            if ln.geom_type=="LineString": rv.append(_ring(ln.coords,1.2))
    grat=""
    for lon in range(12,41,4):
        x,_=P(lon,0); grat+=f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{H}"/>'
    for lat in range(30,44,2):
        _,y=P(0,lat); grat+=f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}"/>'
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
         f'<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e3557"/><stop offset="1" stop-color="#0a2540"/></linearGradient>'
         f'<linearGradient id="land" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a4a3a"/><stop offset="1" stop-color="#5a5238"/></linearGradient></defs>'
         f'<rect width="{W}" height="{H}" fill="url(#sea)"/>'
         f'<g stroke="#7fb3ff" stroke-opacity=".10" stroke-width="1">{grat}</g>'
         f'<path d="{_d(land)}" fill="url(#land)" stroke="#a8c49a" stroke-opacity=".55" stroke-width="1"/>'
         f'<path d="{_d(lakes)}" fill="#0e3557" stroke="#7fb3ff" stroke-opacity=".4" stroke-width=".6"/>'
         f'<path d="{_d(rv,False)}" fill="none" stroke="#6fb6ff" stroke-opacity=".75" stroke-width="1.3" stroke-linejoin="round"/>'
         '</svg>')
    open(path,"w").write(svg); return len(svg)

def smooth(pts):
    if len(pts)<3: return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    d=f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts)-1):
        p0=pts[i-1] if i>0 else pts[i]; p1=pts[i]; p2=pts[i+1]; p3=pts[i+2] if i+2<len(pts) else p2
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d

def city(k, cls="", label=True, fs=15, r=5.5, info=""):
    n,lon,lat,dx,dy,an=C[k]; x,y=P(lon,lat)
    t=f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}" font-size="{fs}">{n}</text>' if label else ""
    return f'<g class="city {cls}" data-k="{k}" data-n="{n}" data-i="{info}" tabindex="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>{t}</g>'

def bigmap(eps, assets="assets"):
    """主地图：四次旅程 + 书信写作地→收信地。"""
    s=[f'<svg class="gmap" viewBox="0 0 {W} {H}" role="img" aria-label="保罗行程与新约书信地图"><image href="{assets}/geo/med.svg" width="{W}" height="{H}"/>']
    s.append('<g class="regions">'+"".join(f'<text x="{P(lo,la)[0]:.0f}" y="{P(lo,la)[1]:.0f}" text-anchor="middle">{n}</text>' for n,lo,la in REGIONS)+'</g>')
    for jid,name,col,ks in JOURNEYS:
        pts=[P(*ll(k)) for k in ks]
        s.append(f'<g class="lyr {jid}" data-l="{jid}"><path d="{smooth(pts)}" stroke="{col}" class="route"/></g>')
    # 书信线
    ls=[]
    for e in eps:
        if e["fr"]==e["dest"]: continue
        (x1,y1),(x2,y2)=P(*ll(e["fr"])),P(*ll(e["dest"]))
        mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1
        cx,cy=mx-dy/L*L*0.18,my+dx/L*L*0.18
        ls.append(f'<path d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}" class="eline g-{e["g"]}" marker-end="url(#arr)"><title>{e["n"]}：{C[e["fr"]][0]} → {C[e["dest"]][0]}</title></path>')
    s.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ffd36b"/></marker></defs>')
    s.append('<g class="lyr ep" data-l="ep">'+"".join(ls)+'</g>')
    info={}
    for e in eps:
        info.setdefault(e["fr"],[]).append(f'写《{e["n"]}》'); info.setdefault(e["dest"],[]).append(f'收《{e["n"]}》')
    s.append('<g class="cities">'+"".join(city(k,info=("；".join(info.get(k,[])))) for k in C if k not in ("patmos","alexandria"))+'</g></svg>')
    return "".join(s)

def minimap(e, assets="assets"):
    a,b=ll(e["fr"]),ll(e["dest"])
    (x1,y1),(x2,y2)=P(*a),P(*b)
    pad=150; x0=max(0,min(x1,x2)-pad); xa=min(W,max(x1,x2)+pad); y0=max(0,min(y1,y2)-pad*0.75); ya=min(H,max(y1,y2)+pad*0.75)
    w=xa-x0; h=ya-y0
    if w/h<1.6:  # 保持横幅
        nw=h*1.6; x0=max(0,min(W-nw,x0-(nw-w)/2)); w=min(W,nw)
    else:
        nh=w/1.6; y0=max(0,min(H-nh,y0-(nh-h)/2)); h=min(H,nh)
    sc=w/600; fs=max(13,15*sc)
    s=f'<svg class="mmap" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" role="img" aria-label="{e["n"]}写作地与收信地"><image href="{assets}/geo/med.svg" width="{W}" height="{H}"/>'
    if e["fr"]!=e["dest"]:
        dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1
        cx,cy=(x1+x2)/2-dy*0.18,(y1+y2)/2+dx*0.18
        s+=f'<defs><marker id="ma-{e["id"]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ffd36b"/></marker></defs>'
        s+=f'<path d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}" class="mline" stroke-width="{3*sc:.1f}" marker-end="url(#ma-{e["id"]})"/>'
    for k,c in ((e["fr"],"from"),(e["dest"],"to")):
        n,lon,lat,dx_,dy_,an=C[k]; x,y=P(lon,lat)
        lab=("✍ " if c=="from" else "📬 ")+n
        s+=f'<g class="city {c}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{6*sc:.1f}"/><text x="{x+dx_*sc:.0f}" y="{y+dy_*sc:.0f}" text-anchor="{an}" font-size="{fs:.0f}">{lab}</text></g>'
        if e["fr"]==e["dest"]: break
    return s+'</svg>'
if __name__=="__main__":
    print(base_svg("/tmp/med.svg"), W, H)
