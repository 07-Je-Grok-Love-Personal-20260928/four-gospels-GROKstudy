# -*- coding: utf-8 -*-
"""v2 地图模块：每张图 = 🎨 离线讲解图（内联 SVG，永不依赖网络） + 🛰️ 实时地图（本地 Leaflet，多瓦片源自动回退）+ 📜 历史文化讲解。"""
import json, math, re
from shapely.geometry import shape, box
from common import md, esc
import palgeo, geo
NE = "/workspace/ne"

# ---------- 地点库 (lat, lon) ----------
PL = {k: (v[2], v[1], v[0], v[6]) for k, v in palgeo.C.items()}   # key:(lat,lon,名,说明)
PL.update({
 "beatitudes": (32.881, 35.556, "八福山（传统地点）", "登山宝训（太5–7）的传统地点，俯瞰加利利海北岸"),
 "tabor": (32.687, 35.390, "他泊山", "一说为登山变像之处（太17:1-8）；另一说为黑门山"),
 "gadara": (32.655, 35.679, "加大拉", "低加波利城；马太记“加大拉人的地方”（太8:28）"),
 "kursi": (32.826, 35.650, "格拉森/库尔西（湖东岸）", "“群”鬼入猪、猪群闯下山崖投在海里（可5:1-20）的可能地点"),
 "ephraim": (31.955, 35.300, "以法莲城", "拉撒路复活后耶稣退到靠近旷野的以法莲城（约11:54）"),
 "bethesda": (31.7814, 35.2357, "毕士大池", "医治病了三十八年的人（约5:1-9）；考古发现五个廊子的双池"),
 "siloam": (31.7705, 35.2345, "西罗亚池", "生来瞎眼的人去洗（约9:7）；2004 年发掘出第二圣殿时期的台阶池"),
 "temple": (31.7781, 35.2354, "圣殿山", "希律圣殿；洁净圣殿（可11:15-17）；圣殿中的辩论（太21–23）"),
 "antonia": (31.7798, 35.2329, "安东尼亚堡", "罗马驻军营楼，俯视圣殿外院；一说为彼拉多审判处"),
 "gethsemane": (31.7795, 35.2398, "客西马尼园", "祷告、汗如血点、被捕（路22:39-53；约18:1）"),
 "olivet": (31.7784, 35.2440, "橄榄山", "骑驴进城出发处；橄榄山讲论（太24）；为城哀哭（路19:41）"),
 "herodpal": (31.7762, 35.2280, "希律宫（今大卫塔一带）", "巡抚到耶路撒冷时的驻地，多数学者认为彼拉多在此审判（约19:13“铺华石处”）"),
 "caiaphas": (31.7716, 35.2316, "大祭司该亚法府（传统地点）", "夜审耶稣；彼得三次不认主（可14:53-72）"),
 "upper": (31.7717, 35.2290, "马可楼（传统楼房）", "最后晚餐、设立圣餐（可14:12-26）；五旬节前门徒聚集"),
 "golgotha": (31.7785, 35.2296, "各各他（圣墓教堂）", "钉十字架与安葬；四世纪起的传统地点，当时位于城墙外（来13:12）"),
 "joppa": (32.054, 34.752, "约帕", "地中海港口；上耶路撒冷之路的起点"),
 "inn": (31.826, 35.344, "好撒玛利亚人客店（传统地点）", "耶路撒冷下耶利哥的险路（路10:30-35）"),
 "deadsea": (31.50, 35.48, "死海（约 −430 米）", "地表最低点；盐海"),
 "sepphoris": (32.753, 35.279, "塞佛瑞斯", "安提帕早期的首府，距拿撒勒约 6 公里"),
 "jordanbapt": (31.837, 35.550, "约但河外伯大尼（施洗处）", "约翰施洗之处（约1:28）；耶稣受洗（可1:9）"),
})
WPL = {"egypt": (30.9, 32.3, "埃及（逃难）", "约瑟带婴孩逃往埃及，应验“我从埃及召出我的儿子”（太2:15）")}
PL.update(WPL)
def pt(k, num=None, col=None):
    la, lo, n, i = PL[k]; d = {"la": la, "lo": lo, "n": n, "i": i}
    if num is not None: d["k"] = num
    if col: d["c"] = col
    return d

# ---------- 通用模块 ----------
def module(mid, ic, title, sub, concept, live, notes, color="#ffc94a", caption=""):
    """concept: SVG/HTML 字符串；live: dict(center, zoom, base, pts, lines, polys)；notes: [(icon, md文本)]"""
    nt = "".join(f'<li><span class="ni">{a}</span><span>{md(t)}</span></li>' for a, t in notes)
    data = esc(json.dumps(live, ensure_ascii=False, separators=(",", ":")))
    return (f'<figure class="mapmod" id="{mid}" style="--mc:{color}"><header class="mm-h"><span class="mm-ic">{ic}</span><div><b>{esc(title)}</b><small>{md(sub)}</small></div></header>'
            f'<div class="mm-grid"><div class="mm-concept"><div class="mm-tag">🎨 讲解图 · 离线可用</div>{concept}<div class="mm-info" aria-live="polite">👆 点按图中地点，查看事件与经文。</div></div>'
            f'<div class="mm-live" data-map="{data}"><div class="mm-tag">🛰️ 实时地图 · 17 源实测 · 自动切换</div><div class="mm-layers" role="group" aria-label="底图来源"></div>'
            f'<div class="mm-canvas" role="region" aria-label="{esc(title)}实时地图"><div class="mm-ph">🛰️ 滑动到这里时自动载入实时地图……<br><small>若网络不通，左侧讲解图照常可用</small></div></div>'
            f'<div class="mm-bar"><button type="button" class="mm-btn" data-a="fit">🎯 全部地点</button><button type="button" class="mm-btn" data-a="play">▶ 播放路线</button><button type="button" class="mm-btn" data-a="drag">✋ 拖动</button><button type="button" class="mm-btn" data-a="full">⛶ 全屏</button></div>'
            f'<div class="mm-status" aria-live="polite">底图：待载入</div><div class="mm-health" aria-live="polite"></div></div></div>'
            f'<ul class="mm-notes">{nt}</ul>{f"<figcaption>{md(caption)}</figcaption>" if caption else ""}</figure>')

# ---------- 底图符号（内联，避免外部文件加载失败） ----------
def _prefix(svg, p):
    inner = re.sub(r'^<svg[^>]*>|</svg>$', '', svg.strip())
    for i in set(re.findall(r'id="([^"]+)"', inner)):
        inner = inner.replace(f'id="{i}"', f'id="{p}{i}"').replace(f'url(#{i})', f'url(#{p}{i})')
    return inner
def symbols(body, docs):
    s = []
    if '#sym-pal' in body:
        s.append(f'<symbol id="sym-pal" viewBox="0 0 {palgeo.W} {palgeo.H}">{_prefix(open(docs+"/assets/geo/pal.svg").read(), "p-")}</symbol>')
    if '#sym-med' in body:
        s.append(f'<symbol id="sym-med" viewBox="0 0 {geo.W} {geo.H}">{_prefix(open(docs+"/assets/geo/med.svg").read(), "m-")}</symbol>')
    if '#sym-gal' in body:
        s.append(GAL_SYM)
    return f'<svg class="symdefs" width="0" height="0" aria-hidden="true" focusable="false">{"".join(s)}</svg>' if s else ""
def usepal(): return f'<use href="#sym-pal" width="{palgeo.W}" height="{palgeo.H}"/>'
def hot(x, y, n, i, col="#ffc94a", r=7, dx=10, dy=5, an="start", num=None, fs=15, lab=True):
    lab = "" if not lab else f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}" font-size="{fs}">{esc(n)}</text>'
    nn = f'<text class="kn" x="{x:.1f}" y="{y+4.5:.1f}" text-anchor="middle" font-size="12">{num}</text>' if num is not None else ""
    return f'<g class="hot" tabindex="0" role="button" data-n="{esc(n)}" data-i="{esc(i)}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r if num is None else 10}" fill="{col}"/>{nn}{lab}</g>'

# ---------- 加利利海放大图（真实湖岸线） ----------
G0, G1, GA0, GA1 = 35.22, 35.80, 32.60, 32.97
GW = 900; GSX = GW/(G1-G0); GSY = GSX/math.cos(math.radians((GA0+GA1)/2)); GH = round((GA1-GA0)*GSY)
def GP(lon, lat): return ((lon-G0)*GSX, (GA1-lat)*GSY)
def _gal_sym():
    B = box(G0-.05, GA0-.05, G1+.05, GA1+.05); lake = ""; riv = ""
    for f in json.load(open(f"{NE}/ne_10m_lakes.geojson"))["features"]:
        if f["properties"].get("name") == "Sea of Galilee":
            g = shape(f["geometry"]).simplify(0.0008)
            lake = "M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in (GP(*c) for c in g.exterior.coords)) + "Z"
    for f in json.load(open(f"{NE}/ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        if f["properties"].get("name") != "Jordan": continue
        g = shape(f["geometry"]).intersection(B)
        for ln in getattr(g, "geoms", [g]):
            if ln.geom_type == "LineString": riv += "M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in (GP(*c) for c in ln.coords))
    hills = "".join(f'<ellipse cx="{GP(a,b)[0]:.0f}" cy="{GP(a,b)[1]:.0f}" rx="{rx}" ry="{ry}"/>' for a, b, rx, ry in [(35.33,32.86,170,120),(35.75,32.80,120,200),(35.40,32.66,110,60),(35.70,32.93,90,60)])
    return (f'<symbol id="sym-gal" viewBox="0 0 {GW} {GH}"><defs><linearGradient id="g-land" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4b6a43"/><stop offset=".55" stop-color="#7a7446"/><stop offset="1" stop-color="#8a6f45"/></linearGradient>'
            '<radialGradient id="g-hill"><stop offset="0" stop-color="#e7d39a" stop-opacity=".45"/><stop offset="1" stop-color="#e7d39a" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="g-lake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3aa0e0"/><stop offset="1" stop-color="#1b5e9e"/></linearGradient></defs>'
            f'<rect width="{GW}" height="{GH}" fill="url(#g-land)"/><g fill="url(#g-hill)">{hills}</g>'
            f'<path d="{riv}" fill="none" stroke="#5fb8ff" stroke-width="4" stroke-linecap="round"/><path d="{lake}" fill="url(#g-lake)" stroke="#bfe6ff" stroke-width="2"/></symbol>')
GAL_SYM = _gal_sym()
def galilee_concept():
    s = [f'<svg class="csvg" viewBox="0 0 {GW} {GH}" role="img" aria-label="加利利海事工情景图"><use href="#sym-gal" width="{GW}" height="{GH}"/>']
    # 波浪 + 小船（动画）
    lx, ly = GP(35.585, 32.80)
    s.append(f'<g class="waves" stroke="#d9f1ff" stroke-width="2" fill="none" opacity=".7"><path d="M{lx-70:.0f},{ly+40:.0f} q15,-10 30,0 t30,0 t30,0"/><path d="M{lx-40:.0f},{ly-60:.0f} q15,-10 30,0 t30,0 t30,0"/><path d="M{lx-20:.0f},{ly+110:.0f} q15,-10 30,0 t30,0"/></g>')
    s.append(f'<g class="boat" transform="translate({lx:.0f},{ly:.0f})"><g class="boat-in"><path d="M-34,0 L34,0 L24,14 L-24,14 Z" fill="#8b5a2b" stroke="#fff3" /><path d="M0,-2 L0,-52 L28,-8 Z" fill="#fff6e0"/><line x1="0" y1="0" x2="0" y2="-54" stroke="#5a3a1a" stroke-width="3"/></g></g>')
    s.append(f'<text x="{lx:.0f}" y="{ly+62:.0f}" text-anchor="middle" class="lk">加利利海</text><text x="{lx:.0f}" y="{ly+88:.0f}" text-anchor="middle" class="lk sm">海平面下约 210 米</text>')
    s.append(f'<text x="24" y="40" class="lk">⛵ 加利利海事工圈</text><text x="24" y="68" class="lk sm">🌪️ 风浪骤起（可4:37）· 🐟 渔业之湖</text>')
    jx, jy = GP(35.575, 32.655); s.append(f'<text x="{jx+10:.0f}" y="{jy:.0f}" class="lk sm">约但河 ↓</text>')
    P = [("capernaum","#ff6b8b"),("bethsaida","#ffc94a"),("beatitudes","#a3e635"),("magdala","#c084fc"),("tiberias","#60a5fa"),("kursi","#fb923c"),("gadara","#fb923c"),("cana","#f472b6"),("nazareth","#ffc94a"),("sepphoris","#94a3b8"),("tabor","#a3e635"),("nain","#2dd4bf")]
    side = {"capernaum":(-12,-12,"end"),"bethsaida":(12,-10,"start"),"beatitudes":(-12,22,"end"),"magdala":(-12,6,"end"),"tiberias":(-12,10,"end"),"kursi":(12,6,"start"),"gadara":(12,6,"start"),"cana":(12,5,"start"),"nazareth":(12,16,"start"),"sepphoris":(12,-6,"start"),"tabor":(12,5,"start"),"nain":(12,16,"start")}
    for k, c in P:
        la, lo, n, i = PL[k]; x, y = GP(lo, la); dx, dy, an = side[k]
        s.append(hot(x, y, n.split("（")[0], i, c, r=10, dx=dx*1.6, dy=dy*1.6, an=an, fs=24))
    s.append('</svg>')
    return "".join(s)
def galilee():
    pts = [pt(k) for k in ["capernaum","bethsaida","beatitudes","magdala","tiberias","kursi","gadara","cana","nazareth","sepphoris","tabor","nain"]]
    live = {"c": [32.80, 35.52], "z": 11, "base": "esri-topo", "pts": pts, "lab": 1}
    notes = [("🏠", "**迦百农是耶稣在加利利的「本城」**（{{太9:1}}）：彼得的家与会堂都在湖西北岸，考古已发掘出四世纪白石会堂叠在一世纪黑玄武岩地基上。"),
             ("🐟", "湖区渔业发达：[[革尼撒勒]]平原肥沃，[[抹大拉]]（Magdala Tarichaeae，意为「腌鱼之城」）以加工鱼产闻名。耶稣呼召渔夫「得人如得鱼」（{{可1:17}}）。"),
             ("🌪️", "湖面低于海平面约 210 米、四周环山，冷空气从高地灌下，常有**突发风暴**——这正是平静风浪（{{可4:35-41}}）与行在水面（{{约6:16-21}}）的真实地理背景。"),
             ("🧭", "湖东岸属外邦的[[低加波利]]：耶稣过到「那边去」（{{可4:35}}），在外邦地赶出「群」鬼——^^福音越过犹太边界的预演^^。"),
             ("🏛️", "[[提比哩亚]]是希律安提帕约主后 20 年为纪念皇帝提庇留所建的新都；福音书从未记载耶稣进入这座城，也未进塞佛瑞斯。")]
    return module("map-galilee", "⛵", "加利利海：事工的心脏地带", "湖岸线取自 Natural Earth 真实数据；小船与风浪为情景示意", galilee_concept(), live, notes, "#38bdf8")

# ---------- 地形剖面：从约帕上耶路撒冷、下耶利哥 ----------
def elevation_concept():
    D = [("约帕",0,0),("吕大",18,50),("伯和仑",38,500),("耶路撒冷",55,760),("橄榄山",57,820),("伯大尼",59,650),("旷野",68,250),("客店",72,150),("耶利哥",80,-258),("约但河",88,-380),("死海",94,-430)]
    W, H, x0, x1, top, bot = 900, 420, 50, 870, 40, 360
    def X(km): return x0 + (km+9)/103*(x1-x0)
    def Y(m): return top + (850-m)/(850+450)*(bot-top)
    pts = [(X(k), Y(m)) for _, k, m in D]
    path = geo.smooth(pts)
    area = path + f" L{X(94):.0f},{bot+40} L{X(0):.0f},{bot+40} Z"
    s = [f'<svg class="csvg elev" viewBox="0 0 {W} {H}" role="img" aria-label="约帕—耶路撒冷—耶利哥—死海地形剖面图"><defs><linearGradient id="el-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2c98a"/><stop offset=".55" stop-color="#9c7a45"/><stop offset="1" stop-color="#5b4426"/></linearGradient>'
         '<linearGradient id="el-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e3a8a" stop-opacity=".55"/><stop offset="1" stop-color="#0ea5e9" stop-opacity=".12"/></linearGradient></defs>'
         f'<rect width="{W}" height="{H}" rx="16" fill="url(#el-sky)"/>']
    for m in (800, 400, 0, -400):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(m):.0f}" y2="{Y(m):.0f}" class="gl"/><text x="{x0-6}" y="{Y(m)+4:.0f}" text-anchor="end" class="ax">{m}m</text>')
    s.append(f'<rect x="{x0}" y="{Y(0):.0f}" width="{X(0)-x0:.0f}" height="{bot+40-Y(0):.0f}" fill="#2563eb" opacity=".6"/><text x="{(x0+X(0))/2:.0f}" y="{Y(0)+40:.0f}" text-anchor="middle" class="ax">🌊 地中海</text>')
    s.append(f'<path d="{area}" fill="url(#el-g)" opacity=".95"/><path id="el-path" d="{path}" fill="none" stroke="#fff7d6" stroke-width="3"/>')
    s.append(f'<rect x="{X(90):.0f}" y="{Y(-430):.0f}" width="{x1-X(90):.0f}" height="30" fill="#38bdf8" opacity=".7"/>')
    s.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(0):.0f}" y2="{Y(0):.0f}" stroke="#60a5fa" stroke-dasharray="6 5" stroke-width="2"/><text x="{x1}" y="{Y(0)-6:.0f}" text-anchor="end" class="ax">海平面 0m</text>')
    info = {"约帕":"港口；彼得在此见异象（徒10），福音向外邦敞开","吕大":"沿海平原","伯和仑":"上山的古道；山地开始","耶路撒冷":"约 760 米；「上耶路撒冷」去守节（路2:42；诗122）","橄榄山":"约 820 米；骑驴进城从这里下坡（路19:37）",
            "伯大尼":"拉撒路的家，距城约 3 公里（约11:18）","旷野":"犹大旷野：施洗约翰与试探的地方（太3–4）","客店":"「从耶路撒冷下耶利哥去」的险路（路10:30）","耶利哥":"约 −258 米，世上最古老城市之一；撒该、巴底买（路19；可10）","约但河":"耶稣受洗（可1:9）","死海":"约 −430 米，地表最低点"}
    for n, k, m in D:
        x, y = X(k), Y(m); up = n in ("橄榄山","伯和仑","约帕","客店")
        tx, ty, an = (x - 12, y + 24, "end") if n == "耶路撒冷" else (x + 12, y + 20, "start") if n == "伯大尼" else (x, y - 14 if up or m > 300 else y + 24, "middle")
        s.append(f'<g class="hot" tabindex="0" role="button" data-n="{n}" data-i="{info[n]}"><circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{"#ffc94a" if n in ("耶路撒冷","耶利哥") else "#fff"}"/><text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{an}" font-size="15">{n}</text></g>')
    s.append(f'<text x="{X(30):.0f}" y="{Y(650):.0f}" class="arrow-t">⬆ 「上」耶路撒冷 · 上行之诗（诗120–134）</text>')
    s.append(f'<text x="{X(60):.0f}" y="{Y(-160):.0f}" text-anchor="middle" class="arrow-t">⬇ 「下」耶利哥：约 25 公里，落差约 1000 米</text>')
    s.append('<g class="walker"><circle r="8" fill="#ff6b8b" stroke="#fff" stroke-width="2"/><animateMotion dur="14s" repeatCount="indefinite" rotate="0"><mpath href="#el-path"/></animateMotion></g>')
    s.append(f'<text x="{x1}" y="{H-10}" text-anchor="end" class="ax">示意剖面：水平距离与高度为近似值（高度夸大约 50 倍）</text></svg>')
    return "".join(s)
def elevation():
    pts = [pt(k, i+1) for i, k in enumerate(["joppa","emmaus","jerusalem","olivet","bethany","inn","jericho","jordanbapt","deadsea"])]
    live = {"c": [31.82, 35.15], "z": 9, "base": "esri-topo", "pts": pts, "lines": [{"n": "约帕 → 耶路撒冷 → 耶利哥 → 约但河", "c": "#ff6b8b", "p": [[p["la"], p["lo"]] for p in pts[:8]]}]}
    notes = [("⛰️", "**「上」与「下」是真实地形**：耶路撒冷坐落在约 760 米的犹大山脊，无论从哪里来都要「上」去；去耶利哥则是一路「下」到海平面以下。"),
             ("🛣️", "好撒玛利亚人的比喻（{{路10:30-37}}）发生在这条荒僻险峻、强盗出没的下坡路上——祭司与利未人正是从圣殿「下来」，却绕道而过。"),
             ("🎵", "犹太人守节时唱[[上行之诗]]（诗120–134）登上锡安；耶稣「定意向耶路撒冷去」（{{路9:51}}），这次「上去」却是==为立约之血而去==。"),
             ("🌵", "从橄榄山往东数公里就是[[犹大旷野]]：施洗约翰在旷野预备主的道（{{可1:3}}），耶稣在旷野四十天受试探——@@旷野＝以色列失败之处，基督得胜之处@@。")]
    return module("map-elev", "⛰️", "地形剖面：上耶路撒冷，下耶利哥", "从地中海到死海不到 100 公里，落差约 1200 米", elevation_concept(), live, notes, "#fb923c")

# ---------- 希律圣殿平面示意 ----------
def temple_concept():
    Z = [("外邦人院","20,40 880,40 880,520 20,520","#a3e635",".10","万国都可进入；耶稣在此推倒兑换银钱之人的桌子：「我的殿必称为万国祷告的殿」（可11:17）"),
         ("所罗门廊","840,60 875,60 875,500 840,500","#fde68a",".35","东侧柱廊；耶稣在此行走，宣告「我与父原为一」（约10:23-30）；初期教会在此聚集（徒3:11）"),
         ("皇家柱廊","40,470 860,470 860,515 40,515","#fde68a",".35","南侧巨型柱廊，兑换银钱、买卖祭牲的商贩多在此一带"),
         ("界墙 Soreg","210,110 760,110 760,430 210,430","#ff6b8b",".06","矮墙上刻希腊文警告：外邦人越过者自招死罪（1871 年出土）。基督「拆毁了中间隔断的墙」（弗2:14）"),
         ("妇女院","250,170 420,170 420,370 250,370","#f472b6",".22","奉献箱所在；耶稣称赞穷寡妇的两个小钱（可12:41-44）"),
         ("以色列院","420,170 480,170 480,370 420,370","#60a5fa",".25","以色列男子献祭时站立之处"),
         ("祭司院·祭坛","480,170 590,170 590,370 480,370","#fb923c",".25","燔祭坛与洗濯盆；每日早晚献祭"),
         ("圣所","590,200 690,200 690,340 590,340","#ffc94a",".30","灯台、陈设饼桌、香坛；撒迦利亚在此烧香时天使显现（路1:8-11）"),
         ("至圣所","712,200 760,200 760,340 712,340","#c084fc",".45","第二圣殿时约柜已不存在；大祭司一年一次带血进入（来9:7）"),
         ("安东尼亚堡","20,40 150,40 150,120 20,120","#94a3b8",".35","罗马驻军营楼，俯瞰外院，可迅速平息骚乱（徒21:31-35）")]
    s = ['<svg class="csvg temple" viewBox="0 0 900 560" role="img" aria-label="希律圣殿平面示意图"><rect width="900" height="560" rx="16" fill="#1a1530"/>']
    for n, p, c, o, i in Z:
        s.append(f'<g class="hot zone" tabindex="0" role="button" data-n="{n}" data-i="{esc(i)}"><polygon points="{p}" fill="{c}" fill-opacity="{o}" stroke="{c}" stroke-width="2"/></g>')
    s.append('<g class="veil" aria-hidden="true"><rect class="v1" x="692" y="200" width="18" height="70" fill="#a855f7"/><rect class="v2" x="692" y="270" width="18" height="70" fill="#7e22ce"/></g>')
    s.append('<rect x="505" y="240" width="40" height="40" fill="#fb923c"/><text x="525" y="300" text-anchor="middle" font-size="13">祭坛</text>')
    L = [("外邦人院",450,80),("所罗门廊",858,300),("皇家柱廊",450,500),("界墙",230,140),("妇女院",335,280),("以色列院",450,190),("祭司院",535,190),("圣所",640,276),("至圣所",736,190),("安东尼亚堡",85,86),("幔子",701,360)]
    for n, x, y in L:
        rot = f' transform="rotate(90 {x} {y})"' if n == "所罗门廊" else ""
        s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="16"{rot}>{n}</text>')
    s.append('<text x="880" y="548" text-anchor="end" font-size="12" class="ax">示意图，非比例 · 东方在右</text></svg>')
    s.append('<button type="button" class="mm-btn veilbtn">✂️ 演示：幔子从上到下裂为两半（可15:38）</button>')
    return "".join(s)
def temple():
    live = {"c": [31.7781, 35.2354], "z": 16, "base": "esri-img", "pts": [pt("temple"), pt("antonia"), pt("bethesda"), pt("siloam"), pt("olivet")], "lab": 1,
            "polys": [{"n": "希律圣殿平台（约 14 万平方米）", "c": "#ffc94a", "p": [[31.7808, 35.2346], [31.7795, 35.2373], [31.7755, 35.2363], [31.7761, 35.2337]]}]}
    notes = [("🏛️", "大希律约主前 20 年开始扩建圣殿（{{约2:20}} 的「四十六年」），平台面积约为雅典卫城的两倍；主后 70 年被罗马军焚毁，应验{{太24:2}}。"),
             ("🧱", "层层递进的院落表达了旧约的==隔离==：外邦人、妇女、以色列人、祭司、大祭司，越往里越少人能进。"),
             ("✂️", "耶稣断气时「殿里的幔子从上到下裂为两半」（{{可15:38}}）：^^道路已经开了^^，靠着祂的血可以坦然进入至圣所（{{来10:19-20}}）。"),
             ("🔥", "耶稣说「你们拆毁这殿，我三日内要再建立起来」——「但耶稣这话，是以他的身体为殿」（{{约2:19-21}}）：**真圣殿是基督自己**，如今也是祂的教会（林前3:16）。")]
    return module("map-temple", "🏛️", "希律圣殿：从隔离到开路", "平面关系为示意；实时地图可切到 Esri 卫星看今日圣殿山", temple_concept(), live, notes, "#c084fc")

# ---------- 希律王国的分封（主前 4 年后） ----------
REGPOLY = [
 ("加利利（安提帕）", "#60a5fa", [(35.08,33.10),(35.62,33.10),(35.65,32.72),(35.55,32.55),(35.30,32.52),(35.05,32.80)], "安提帕（前4–主后39）；耶稣事工的主要区域"),
 ("比利亚（安提帕）", "#60a5fa", [(35.58,32.45),(35.85,32.38),(35.86,31.60),(35.58,31.62)], "约但河东；耶稣最后上耶路撒冷经过此地（可10:1）"),
 ("撒玛利亚（亚基老→巡抚）", "#fb923c", [(34.90,32.55),(35.55,32.55),(35.56,32.06),(34.85,32.06)], "撒玛利亚人与犹太人不相往来（约4:9）"),
 ("犹太（亚基老→巡抚）", "#ff6b8b", [(34.72,32.06),(35.56,32.06),(35.52,31.45),(34.95,31.40),(34.62,31.70)], "主后 6 年起由罗马巡抚直辖；彼拉多 26–36 年在任"),
 ("以土买（亚基老→巡抚）", "#f472b6", [(34.85,31.42),(35.45,31.45),(35.40,31.08),(34.85,31.08)], "希律家族的故乡（以东人的后裔）"),
 ("低加波利（叙利亚省）", "#a3e635", [(35.64,32.96),(36.12,32.92),(36.22,32.30),(35.86,32.20),(35.62,32.48)], "十座希腊化城市的联盟，外邦文化区"),
 ("腓力分封地", "#c084fc", [(35.62,33.38),(36.40,33.32),(36.62,32.82),(36.10,32.90),(35.66,32.92)], "希律腓力（前4–主后34）；凯撒利亚腓立比、伯赛大"),
]
def herod_concept():
    s = [f'<svg class="csvg" viewBox="0 0 {palgeo.W} {palgeo.H}" role="img" aria-label="希律王国分封示意图">{usepal()}']
    for n, c, poly, i in REGPOLY:
        d = "M" + " L".join(f"{palgeo.P(lo,la)[0]:.0f},{palgeo.P(lo,la)[1]:.0f}" for lo, la in poly) + "Z"
        cx = sum(palgeo.P(lo, la)[0] for lo, la in poly)/len(poly); cy = sum(palgeo.P(lo, la)[1] for lo, la in poly)/len(poly)
        s.append(f'<g class="hot zone" tabindex="0" role="button" data-n="{n}" data-i="{i}"><path d="{d}" fill="{c}" fill-opacity=".30" stroke="{c}" stroke-width="2.5" stroke-dasharray="7 4"/><text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" font-size="15">{n.split("（")[0]}</text></g>')
    for k, c in (("jerusalem","#ffc94a"),("caesarea","#94a3b8"),("tiberias","#60a5fa"),("cphilippi","#c084fc"),("machaerus","#60a5fa")):
        la, lo, n, i = PL[k]; x, y = palgeo.P(lo, la); s.append(hot(x, y, n, i, c, r=6, fs=13))
    s.append('</svg>')
    return "".join(s)
def herod():
    live = {"c": [32.25, 35.55], "z": 8, "base": "dare", "polys": [{"n": n, "c": c, "i": i, "p": [[la, lo] for lo, la in p]} for n, c, p, i in REGPOLY],
            "pts": [pt(k) for k in ("jerusalem", "caesarea", "tiberias", "cphilippi", "machaerus", "sepphoris")]}
    notes = [("👑", "大希律死（主前 4 年）后，罗马把王国分给三个儿子：**亚基老**（犹太、撒玛利亚、以土买）、**安提帕**（加利利、比利亚）、**腓力**（东北）。约瑟因怕亚基老而改住加利利（{{太2:22}}）。"),
             ("🦅", "主后 6 年亚基老被废，犹太改由罗马[[巡抚]]直辖，驻凯撒利亚——所以耶稣受审时既见彼拉多又被送到希律（{{路23:6-12}}）：两个政权，各管一方。"),
             ("🦊", "耶稣称安提帕为「那个狐狸」（{{路13:32}}）；他斩了施洗约翰（{{可6:14-29}}）。^^世上的王都摇动，唯有基督的国不能震动^^。"),
             ("🗺️", "实时地图默认使用 **DARE 罗马帝国数字地图**（瑞典哥德堡大学），可看到古地名与罗马道路；范围色块为本站示意。")]
    return module("map-herod", "👑", "政治版图：希律家族的分封与罗马巡抚", "边界为大致范围（古代边界本不精确）", herod_concept(), live, notes, "#60a5fa")

# ---------- 罗马世界：福音书写作地 ----------
def med_concept():
    W, H = geo.W, geo.H
    x0, y0, w, h = 0, 30, W, H-30
    s = [f'<svg class="csvg" viewBox="{x0} {y0} {w} {h}" role="img" aria-label="罗马世界与四福音书写作地"><use href="#sym-med" width="{W}" height="{H}"/>']
    jx, jy = geo.P(35.23, 31.78)
    G = [("rome","马可福音 · 罗马","#ff6b8b","彼得的见证，写给受尼禄逼迫的罗马信徒（约 55–65）"),("antioch","马太福音 · 安提阿/巴勒斯坦","#ffc94a","写给犹太基督徒为主的教会（约 50–60 年代）"),
         ("caesarea","路加福音 · 该撒利亚/罗马","#2dd4bf","献给提阿非罗；保罗在该撒利亚被囚两年间考察（约 60–62）"),("ephesus","约翰福音 · 以弗所","#a78bfa","使徒约翰晚年在以弗所写成（约 85–95）")]
    for k, n, c, i in G:
        x, y = geo.P(*geo.ll(k)); dx, dy = x-jx, y-jy; L = math.hypot(dx, dy) or 1
        cx, cy = (x+jx)/2 - dy*0.2, (y+jy)/2 + dx*0.2
        if L > 30: s.append(f'<path d="M{jx:.0f},{jy:.0f} Q{cx:.0f},{cy:.0f} {x:.0f},{y:.0f}" class="flowline" stroke="{c}"/>')
    for k, n, c, i in G:
        x, y = geo.P(*geo.ll(k)); an = "end" if k in ("caesarea",) else "start"
        s.append(hot(x, y, n, i, c, r=9, dx=-14 if an == "end" else 14, dy=-10 if k == "caesarea" else 6, an=an, fs=20))
    s.append(hot(jx, jy, "耶路撒冷", "福音从这里开始：「从耶路撒冷起直到万邦」（路24:47）", "#fff", r=8, dx=12, dy=20, fs=18))
    for n, lo, la in (("意大利", 15.6, 41.3), ("亚细亚", 28.6, 38.7), ("叙利亚", 37.6, 35.1), ("埃及", 31.5, 30.2), ("地 中 海", 18.8, 33.4)):
        x, y = geo.P(lo, la); s.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" class="rg">{n}</text>')
    s.append('</svg>')
    return "".join(s)
def med():
    pts = [{"la": 41.89, "lo": 12.48, "n": "罗马 · 马可福音", "i": "彼得的见证，写给受逼迫的罗马信徒（约 55–65）", "c": "#ff6b8b"},
           {"la": 36.20, "lo": 36.16, "n": "叙利亚的安提阿 · 马太福音（一说）", "i": "犹太人与外邦人同处的大城，第一个外邦人教会（徒11:26）", "c": "#ffc94a"},
           {"la": 32.50, "lo": 34.89, "n": "该撒利亚 · 路加福音（一说）", "i": "保罗被囚两年（徒24:27），路加可就近考察见证人", "c": "#2dd4bf"},
           {"la": 37.94, "lo": 27.34, "n": "以弗所 · 约翰福音", "i": "约翰晚年牧养亚细亚众教会", "c": "#a78bfa"},
           {"la": 31.78, "lo": 35.23, "n": "耶路撒冷", "i": "福音的起点（路24:47；徒1:8）", "c": "#ffffff"},
           {"la": 31.20, "lo": 29.92, "n": "亚历山大", "i": "传统认为马可后来在此建立教会", "c": "#94a3b8"}]
    live = {"c": [36.0, 25.0], "z": 4, "base": "dare", "pts": pts, "lab": 1, "lines": [{"n": "福音传向万邦", "c": p["c"], "p": [[31.78, 35.23], [p["la"], p["lo"]]]} for p in pts[:4]]}
    notes = [("🛣️", "**罗马和平**（Pax Romana）与罗马大道、海路、通用希腊语，使福音得以在一代人之内传遍地中海世界——^^「及至时候满足，神就差遣他的儿子」^^（{{加4:4}}）。"),
             ("📜", "四卷福音书写于四个不同的教会处境：犹太基督徒（马太）、受逼迫的罗马人（马可）、希腊化的外邦慕道者（路加）、面对异端与会堂压力的亚细亚教会（约翰）。==同一福音，向万民说话==。"),
             ("🕊️", "写作地多为早期教父（帕皮亚、爱任纽）的记载；改革宗看重这些外证，但信心的根基在于**圣灵在圣经中的自证**（BC 5）。")]
    return module("map-med", "🌍", "罗马世界：四福音书从哪里写给谁", "底图：Natural Earth 真实海岸线；实时地图默认 DARE 罗马帝国古地图", med_concept(), live, notes, "#a78bfa")

# ---------- 巴勒斯坦总图：耶稣生平七段路线 ----------
def pal_concept():
    return '<div class="mapscroll" tabindex="0" aria-label="可左右滑动查看完整地图">' + palgeo.palmap() + '</div>' 
def palestine():
    lines = []
    for jid, name, col, ks in palgeo.ROUTES:
        lines.append({"n": name, "c": col, "p": [[palgeo.ll(k)[1], palgeo.ll(k)[0]] for k in ks]})
    pts = [pt(k) for k in palgeo.C]
    live = {"c": [32.25, 35.35], "z": 8, "base": "esri-street", "pts": pts, "lines": lines}
    notes = [("🧭", "耶稣的事工按地理分三大区：**加利利**（大部分神迹与教训）→ **北方外邦地区**（推罗、西顿、凯撒利亚腓立比的转折）→ **犹太与耶路撒冷**（受难与复活）。马可正是按这个地理顺序写成。"),
             ("🚶", "从加利利到耶路撒冷约 120–150 公里，步行约 4–6 天；犹太人常绕道约但河东（比利亚）以避开撒玛利亚，耶稣却「必须经过撒玛利亚」（{{约4:4}}）。"),
             ("📍", "点按讲解图上的彩色按钮可开关各段路线，「▶ 播放路线」会依次画出七段行程；实时地图也有同样的动画。"),
             ("⚠️", "路线是依福音书地点连成的示意线，不代表精确道路；!!以马忤斯、格拉森!!等地点学界有不同说法。")]
    lg = "".join(f'<button type="button" class="lb on" data-l="{j}" style="--c:{c}">{n}</button>' for j, n, c, _ in palgeo.ROUTES)
    concept = f'<div class="maptools">{lg}<button type="button" class="lb play">▶ 播放</button></div>' + pal_concept()
    return module("map-pal", "🗺️", "巴勒斯坦：耶稣生平七段足迹", "底图：Natural Earth 10m 海岸线、湖泊与约但河（公有领域）", concept, live, notes, "#ffc94a")

# ---------- 耶路撒冷受难周 ----------
def jerusalem():
    ks = ["olivet", "temple", "upper", "gethsemane", "caiaphas", "antonia", "herodpal", "golgotha", "bethesda", "siloam"]
    pts = [pt(k, i+1) for i, k in enumerate(ks)]
    night = [pt(k) for k in ["upper", "gethsemane", "caiaphas", "herodpal", "golgotha"]]
    live = {"c": [31.7765, 35.2340], "z": 15, "base": "esri-img", "pts": pts, "lines": [{"n": "受难夜到受难日的大致路径", "c": "#ffd36b", "p": [[p["la"], p["lo"]] for p in night]}]}
    notes = [("🌿", "**星期日**从橄榄山骑驴下坡进城（{{路19:37-38}}）→ **星期四夜**楼房晚餐 → 过汲沦溪到客西马尼（{{约18:1}}）→ 被押到大祭司府 → **星期五清晨**解到彼拉多 → 出城到各各他。"),
             ("✝️", "各各他在当时的城墙之外：「耶稣要用自己的血叫百姓成圣，也就在城门外受苦」（{{来13:12}}），正如赎罪祭牲的身体要烧在营外（利16:27）。"),
             ("🏺", "考古：1961 年凯撒利亚出土「彼拉多碑文」；1990 年发现刻有「该亚法」名字的骨灰盒；毕士大池与西罗亚池都已发掘——@@福音书扎根于真实的地理与历史@@。")]
    concept = palgeo.jerusalem()
    return module("map-jer", "🏙️", "耶路撒冷：受难周的地点", "讲解图为非比例示意；实时地图默认 Esri 卫星影像", concept, live, notes, "#ff6b8b")

# ---------- 每卷福音书的地理足迹 ----------
GEO = {
 "mat": ["bethlehem", "egypt", "nazareth", "jordanbapt", "capernaum", "beatitudes", "gadara", "cphilippi", "jericho", "jerusalem", "tabor"],
 "mrk": ["jordanbapt", "capernaum", "kursi", "nazareth", "tyre", "bethsaida", "cphilippi", "jericho", "bethany", "golgotha"],
 "luk": ["nazareth", "bethlehem", "temple", "capernaum", "nain", "sychar", "jericho", "olivet", "golgotha", "emmaus"],
 "jhn": ["bethabara", "cana", "temple", "sychar", "bethesda", "tiberias", "siloam", "bethany", "ephraim", "golgotha"],
}
GNOTE = {
 "mat": [("👑", "马太以地理证明「应验」：**伯利恒**（弥5:2）、**埃及**（何11:1）、**拿撒勒**（「拿撒勒人」）、**迦百农**（赛9:1-2「外邦的加利利」）——^^王的足迹每一步都在先知书中^^。"),
         ("⛰️", "马太的耶稣常在「山上」：登山宝训（5–7）、登山变像（17）、橄榄山讲论（24）、加利利山上的大使命（28）——@@新摩西在山上颁布天国之律@@。")],
 "mrk": [("🦁", "马可的地理是一条**直线**：加利利 → 北方外邦地 → 凯撒利亚腓立比（8:27 转折）→「在路上」→ 耶路撒冷。"),
         ("🌊", "马可六次写耶稣「渡到那边去」：福音一再越过湖面进入外邦地（格拉森、推罗、低加波利），预演==万国蒙福==。")],
 "luk": [("🩺", "路加的地理以**耶路撒冷为中心**：开始于圣殿（1:9），中段是长长的「旅行叙事」（9:51–19:44），结束于圣殿（24:53）；使徒行传再从耶路撒冷走到罗马。"),
         ("🛤️", "以马忤斯路上，复活的主「从摩西和众先知起，凡经上所指着自己的话都给他们讲解明白」（{{路24:27}}）——^^整本旧约都指向基督^^。")],
 "jhn": [("🦅", "约翰的地理以**节期上耶路撒冷**为骨架：至少三次逾越节（2:13；6:4；11:55）、住棚节（7:2）、修殿节（10:22）——耶稣是节期所预表的实体。"),
         ("💧", "约翰特别记下**水池与井**：雅各井（4）、毕士大池（5）、西罗亚池（9）——旧的水源不能使人得生命，^^耶稣赐的是活水^^。")],
}
JER = {"temple", "golgotha", "bethesda", "siloam", "olivet", "upper", "jerusalem", "bethany", "gethsemane"}
def gospel_geo(e):
    ks = GEO[e["id"]]; col = e["col"]
    xy = []; jer = []
    for j, k in enumerate(ks):
        la, lo, n, i = PL[k]
        if k in JER: jer.append((j+1, n, i)); la, lo = 31.78, 35.23
        xy.append(palgeo.P(lo, la))
    inb = [p for k, p in zip(ks, xy) if k != "egypt"]
    x0 = min(p[0] for p in inb) - 70; x1 = max(p[0] for p in inb) + 70; y0 = min(p[1] for p in inb) - 40; y1 = max(p[1] for p in inb) + 40
    if x1 - x0 < 420: c = (x0 + x1)/2; x0, x1 = c - 210, c + 210
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(palgeo.W, x1); y1 = min(palgeo.H, y1)
    xy = [(max(x0+16, min(x1-16, x)), max(y0+16, min(y1-16, y))) if k == "egypt" else (x, y) for k, (x, y) in zip(ks, xy)]
    s = [f'<svg class="csvg" viewBox="{x0:.0f} {y0:.0f} {x1-x0:.0f} {y1-y0:.0f}" role="img" aria-label="{e["n"]}的地理足迹">{usepal()}']
    s.append(f'<path d="{geo.smooth(xy)}" class="gpath" stroke="{col}"/>')
    for j, k in enumerate(ks):
        if k in JER: continue
        la, lo, n, i = PL[k]; x, y = xy[j]
        an = "end" if lo > 35.5 else "start"
        s.append(hot(x, y, n, i, col, num=j+1, lab=(k == "egypt"), dx=14, dy=5, fs=17).replace(f'>{n}</text>', '>↙ 埃及</text>'))
    if jer:
        x, y = palgeo.P(35.23, 31.78)
        nums = "、".join(str(a) for a, _, _ in jer)
        info = "；".join(f"{a}. {n}：{i}" for a, n, i in jer)
        s.append(hot(x, y, f"耶路撒冷一带（{nums}）", info, col, num="✦", lab=False))
    s.append('</svg>')
    s.append('<ol class="glist">' + "".join(f'<li><span class="mk" style="--c:{col}">{j+1}</span>{esc(PL[k][2].split("（")[0])}</li>' for j, k in enumerate(ks)) + '</ol>')
    pts = [pt(k, j+1, col) for j, k in enumerate(ks)]
    live = {"c": [32.15, 35.35], "z": 8, "base": "esri-street", "pts": pts, "lines": [{"n": e["n"] + "的叙事顺序", "c": col, "p": [[p["la"], p["lo"]] for p in pts]}]}
    return module(f'map-{e["id"]}', e["ic"], f'{e["n"]}的地理足迹', "编号＝本卷叙事中首次出现的次序（示意）", "".join(s), live, GNOTE[e["id"]], col)
