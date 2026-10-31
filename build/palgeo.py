# -*- coding: utf-8 -*-
"""巴勒斯坦真实底图（Natural Earth 10m 公有领域数据，构建时投影为静态 SVG）+ 耶稣生平路线叠加层。"""
import json, math
from shapely.geometry import shape, box
from geo import smooth
NE = "/workspace/ne"
lo0, lo1, la0, la1 = 34.15, 36.55, 30.95, 33.68
W = 720; MID = (la0+la1)/2
SX = W/(lo1-lo0); SY = SX/math.cos(math.radians(MID)); H = round((la1-la0)*SY)
def P(lon, lat): return ((lon-lo0)*SX, (la1-lat)*SY)
C = {  # key:(名, lon, lat, dx, dy, anchor, 说明)
 "jerusalem":("耶路撒冷",35.23,31.78,-10,4,"end","圣殿；受难、复活、升天之城（路9:51 起定意前往）"),
 "bethlehem":("伯利恒",35.20,31.70,-8,14,"end","大卫的城；耶稣降生（太2:1；路2:4-7；弥5:2）"),
 "bethany":("伯大尼",35.26,31.77,9,14,"start","马利亚、马大、拉撒路的家；拉撒路复活（约11）；升天（路24:50）"),
 "nazareth":("拿撒勒",35.30,32.70,-9,12,"end","耶稣长大之地；会堂宣言（路4:16-30）"),
 "cana":("迦拿",35.34,32.75,-8,5,"end","变水为酒、医大臣之子（约2；4:46）"),
 "capernaum":("迦百农",35.575,32.88,-8,-8,"end","加利利事工的“本城”（太9:1）；彼得的家"),
 "bethsaida":("伯赛大",35.63,32.91,8,-6,"start","彼得、安得烈、腓力的家乡（约1:44）；五饼二鱼附近（路9:10）"),
 "magdala":("抹大拉",35.52,32.82,-8,8,"end","抹大拉的马利亚的家乡"),
 "nain":("拿因",35.35,32.63,8,14,"start","叫寡妇的儿子复活（路7:11-17）"),
 "gerasa":("格拉森",35.65,32.83,8,10,"start","赶出“群”鬼，猪群投海（可5:1-20）"),
 "cphilippi":("凯撒利亚腓立比",35.69,33.25,8,4,"start","彼得认信“你是基督”（太16:13-20）"),
 "tyre":("推罗",35.20,33.27,-8,4,"end","叙利非尼基妇人的信心（可7:24-30）"),
 "sidon":("西顿",35.37,33.56,-8,4,"end","耶稣经过西顿（可7:31）"),
 "sychar":("叙加",35.28,32.21,-8,4,"end","雅各井旁的撒玛利亚妇人（约4）"),
 "jericho":("耶利哥",35.44,31.87,8,-4,"start","撒该、瞎子巴底买（路19；可10:46）"),
 "bethabara":("约但河外伯大尼",35.55,31.84,8,12,"start","约翰施洗之处（约1:28）；耶稣受洗"),
 "emmaus":("以马忤斯",34.99,31.84,-8,4,"end","复活的主与两个门徒同行（路24:13-35）"),
 "caesarea":("凯撒利亚",34.89,32.50,-8,4,"end","罗马巡抚驻地（彼拉多碑文出土地）"),
 "machaerus":("马盖耳斯堡",35.63,31.56,8,4,"start","希律安提帕的要塞；据约瑟夫记载施洗约翰在此被斩"),
 "tiberias":("提比哩亚",35.53,32.79,8,16,"start","希律安提帕的新都（约6:23）"),
}
WP = {"samaria":(35.25,32.27),"egypt":(34.30,31.10),"coast1":(34.80,31.95),"coast2":(34.95,32.45),"jv1":(35.56,32.40),"jv2":(35.55,32.10),"wild":(35.38,31.62),
      "judea":(35.45,31.95),"dec":(35.85,32.72),"hermon":(35.78,33.32),"perea1":(35.62,32.25),"perea2":(35.62,31.98),"galmt":(35.40,32.80),"shore":(35.56,32.86),"jv3":(35.52,32.55)}
def ll(k): return (C[k][1], C[k][2]) if k in C else WP[k]
ROUTES = [
 ("j1","① 降生与童年（太2；路2）","#f5b942",["nazareth","samaria","jerusalem","bethlehem","egypt","coast1","coast2","nazareth"]),
 ("j2","② 受洗与试探（太3–4）","#4fb3ff",["nazareth","jv3","jv1","jv2","bethabara","wild","bethabara","jv2","jv1","cana"]),
 ("j3","③ 早期犹太事工（约2–4）","#3fd39a",["cana","capernaum","jv3","jv2","jerusalem","judea","sychar","cana"]),
 ("j4","④ 加利利大事工（太4–15）","#ff6b8b",["nazareth","capernaum","magdala","nain","tiberias","gerasa","bethsaida","capernaum"]),
 ("j5","⑤ 北方与外邦地区（可7–9）","#c084fc",["capernaum","tyre","sidon","hermon","dec","bethsaida","cphilippi","capernaum"]),
 ("j6","⑥ 最后上耶路撒冷（路9:51–19:44）","#fb923c",["capernaum","jv3","perea1","perea2","jericho","bethany","jerusalem"]),
 ("j7","⑦ 复活显现与升天（太28；路24；约21）","#fde047",["jerusalem","emmaus","jerusalem","jv2","jv1","shore","galmt","jv1","bethany"]),
]
REG = [("加 利 利",35.10,33.0),("撒 玛 利 亚",35.12,32.30),("犹 太",34.98,31.55),("比 利 亚",35.85,31.95),("低加波利",36.05,32.55),("腓 尼 基",35.05,33.48),("腓力分封地",36.05,33.05),("地 中 海",34.45,32.45),("加利利海",35.86,32.68),("死 海",35.62,31.35),("约但河",35.66,32.30),("犹大旷野",35.30,31.45),("以 土 买",34.80,31.15)]
def base_svg(path):
    B = box(lo0-.3, la0-.3, lo1+.3, la1+.3)
    def polys(name, minarea=0):
        rings = []
        for f in json.load(open(f"{NE}/{name}.geojson"))["features"]:
            g = shape(f["geometry"])
            if not g.intersects(B): continue
            g = g.intersection(B).simplify(0.5/SX)
            for p in getattr(g, "geoms", [g]):
                if p.geom_type != "Polygon" or p.area < minarea: continue
                rings.append([P(*c) for c in p.exterior.coords])
        return rings
    def d(rings, close=True): return "".join("M"+" ".join(f"{x:.1f},{y:.1f}" for x, y in r)+("Z" if close else "") for r in rings if len(r) > 1)
    land = polys("ne_10m_land"); lakes = polys("ne_10m_lakes")
    rv = []
    for f in json.load(open(f"{NE}/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        g = shape(f["geometry"])
        if not g.intersects(B): continue
        g = g.intersection(B)
        for ln in getattr(g, "geoms", [g]):
            if ln.geom_type == "LineString": rv.append([P(*c) for c in ln.coords])
    grat = "".join(f'<line x1="{P(lo,0)[0]:.0f}" y1="0" x2="{P(lo,0)[0]:.0f}" y2="{H}"/>' for lo in (34.5, 35, 35.5, 36, 36.5))
    grat += "".join(f'<line x1="0" y1="{P(0,la)[1]:.0f}" x2="{W}" y2="{P(0,la)[1]:.0f}"/>' for la in (31, 31.5, 32, 32.5, 33, 33.5))
    # 高地示意：犹太山地、加利利山地、撒玛利亚山地、黑门山
    hills = [(35.15,31.65,.18,.32),(35.25,32.25,.14,.22),(35.40,32.95,.22,.14),(35.80,33.40,.14,.14)]
    hs = "".join(f'<ellipse cx="{P(a,b)[0]:.0f}" cy="{P(a,b)[1]:.0f}" rx="{c*SX:.0f}" ry="{e*SY:.0f}"/>' for a, b, c, e in hills)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>'
           '<linearGradient id="sea" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3557"/><stop offset="1" stop-color="#0a2540"/></linearGradient>'
           '<linearGradient id="land" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3d4f3b"/><stop offset=".6" stop-color="#5a5238"/><stop offset="1" stop-color="#6b5a3a"/></linearGradient>'
           '<radialGradient id="hill"><stop offset="0" stop-color="#c9b27a" stop-opacity=".35"/><stop offset="1" stop-color="#c9b27a" stop-opacity="0"/></radialGradient></defs>'
           f'<rect width="{W}" height="{H}" fill="url(#sea)"/><g stroke="#7fb3ff" stroke-opacity=".10">{grat}</g>'
           f'<path d="{d(land)}" fill="url(#land)" stroke="#a8c49a" stroke-opacity=".6" stroke-width="1.2"/>'
           f'<g fill="url(#hill)">{hs}</g>'
           f'<path d="{d(lakes)}" fill="#1a5a8a" stroke="#7fb3ff" stroke-opacity=".7" stroke-width="1"/>'
           f'<path d="{d(rv, False)}" fill="none" stroke="#6fb6ff" stroke-opacity=".9" stroke-width="2" stroke-linejoin="round"/></svg>')
    open(path, "w").write(svg); return len(svg)
def city(k, fs=15, r=5.5):
    n, lon, lat, dx, dy, an, info = C[k]; x, y = P(lon, lat)
    return f'<g class="city" data-k="{k}" data-n="{n}" data-i="{info}" tabindex="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/><text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}" font-size="{fs}">{n}</text></g>'
def palmap(assets="assets"):
    s = [f'<svg class="gmap pal" viewBox="0 0 {W} {H}" role="img" aria-label="耶稣生平路线地图（巴勒斯坦）"><image href="{assets}/geo/pal.svg" width="{W}" height="{H}"/>']
    s.append('<g class="regions">'+"".join(f'<text x="{P(lo,la)[0]:.0f}" y="{P(lo,la)[1]:.0f}" text-anchor="middle">{n}</text>' for n, lo, la in REG)+'</g>')
    for jid, name, col, ks in ROUTES:
        s.append(f'<g class="lyr {jid}" data-l="{jid}"><path d="{smooth([P(*ll(k)) for k in ks])}" stroke="{col}" class="route"><title>{name}</title></path></g>')
    ex, ey = P(*WP["egypt"]); s.append(f'<text x="{ex+6:.0f}" y="{ey+22:.0f}" font-size="14" class="egy">↙ 往埃及（太2:13-15）</text>')
    s.append('<g class="cities">'+"".join(city(k) for k in C)+'</g></svg>')
    return "".join(s)
def jerusalem():
    """耶路撒冷受难周示意图（非比例）。"""
    pts = [("圣殿山",300,190,"#f5b942","洁净圣殿（可11:15）；圣殿中的辩论（太21–23）"),("安东尼亚堡",330,120,"#ff6b8b","罗马驻军；可能的审判处之一（铺华石处，约19:13）"),
           ("毕士大池",380,95,"#4fb3ff","医治三十八年的病人（约5）"),("客西马尼园",520,170,"#3fd39a","祷告与被捕（太26:36-56）"),("橄榄山",600,230,"#3fd39a","橄榄山讲论（太24）；升天（徒1:12）"),
           ("希律宫",120,240,"#c084fc","彼拉多在耶路撒冷的驻地（多数学者认为审判在此）"),("大祭司该亚法家",170,330,"#fb923c","夜审；彼得三次不认主（可14:53-72）"),
           ("楼房（锡安山）",150,390,"#fde047","最后晚餐（可14:15）"),("各各他",110,140,"#ff6b8b","钉十字架（约19:17）；附近园中新坟（约19:41）"),("西罗亚池",270,420,"#4fb3ff","生来瞎眼的人洗眼（约9:7）")]
    s = ['<svg class="jmap" viewBox="0 0 700 470" role="img" aria-label="耶路撒冷受难周示意图"><defs><linearGradient id="jg" x1="0" x2="1"><stop offset="0" stop-color="#2a2f45"/><stop offset="1" stop-color="#3a3350"/></linearGradient></defs>',
         '<rect width="700" height="470" rx="18" fill="url(#jg)"/>',
         '<path d="M90,110 L250,80 L420,80 L440,150 L430,300 L330,450 L200,440 L90,300 Z" fill="rgba(245,185,66,.08)" stroke="#f5b942" stroke-opacity=".6" stroke-width="3" stroke-dasharray="10 6"/>',
         '<path d="M470,40 C480,150 470,300 380,460" fill="none" stroke="#4fb3ff" stroke-width="4" opacity=".7"/><text x="488" y="70" class="lbl">汲沦溪</text>',
         '<rect x="240" y="150" width="140" height="90" rx="8" fill="rgba(245,185,66,.18)" stroke="#f5b942"/>',
         '<path class="pw" d="M150,390 C330,360 470,250 520,170 C420,150 260,250 170,330 C140,300 120,260 120,240 C200,200 280,140 330,120 C250,160 160,230 120,240 C110,200 110,170 110,140"/>']
    for i, (n, x, y, c, d) in enumerate(pts):
        s.append(f'<g class="jp" tabindex="0" data-n="{n}" data-i="{d}"><circle cx="{x}" cy="{y}" r="9" fill="{c}"/><text x="{x+13}" y="{y+5}">{n}</text></g>')
    s.append('<text x="680" y="455" text-anchor="end" class="lbl sm">示意图，非比例 · 虚线：受难夜的大致行程</text></svg>')
    return "".join(s)
if __name__ == "__main__": print(base_svg("/tmp/pal.svg"), W, H)
