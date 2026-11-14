# -*- coding: utf-8 -*-
import re
from common import md, esc
from p_hist import tbl
import maps
PROV = [("🛣️ Esri 街道","Esri World Street Map，全球 CDN，最快（实测 ≈0.1 秒）","默认首选"),("🛣️ OpenStreetMap","开源世界地图官方瓦片","全球通用"),("⛰️ Esri 地形","World Topo，带地形晕渲","看山地与河谷"),
        ("🧭 Esri 国家地理","National Geographic 挂图风格（原生 ≤16 级）","教学挂图感"),("⛰️ OpenTopoMap","等高线地形图（原生 ≤17 级）","看海拔落差"),("🛰️ Esri 卫星","World Imagery 卫星影像","看今日实景"),
        ("🏛️ DARE 罗马帝国","哥德堡大学《罗马帝国数字地图》：古地名、罗马道路（原生 ≤11 级）","看一世纪的世界"),("⛰️ CyclOSM","地形晕渲 + 道路，OSM France 服务器","地形备用"),
        ("🌄 Esri 自然地貌","World Physical Map（原生 ≤8 级，放大时自动拉伸）","看大地形"),("🌄 Esri 山体晕渲","World Shaded Relief（原生 ≤13 级）","看山脊谷地"),
        ("🛣️ OSM 法国 / 德国 / 人道主义","三个独立服务器的 OSM 镜像","网络备用"),("🚌 ÖPNV","memomaps.de 交通风格","再备用"),("🌫️ Esri 浅灰 · 🌙 夜色","低干扰底图，叠加路线最清楚；夜色配夜间主题","专注路线 / 夜读"),
        ("🇨🇳 高德","中国大陆网络通常可达；境外只有国界轮廓（原生 ≤9 级）","大陆网络最后备用")]
GEO_T = [("🏜️ 旷野","以色列在旷野四十年试探神而失败（申8:2）","耶稣在旷野四十天，三次引申命记得胜（{{太4:1-11}}）","@@旷野：第一个以色列跌倒处，真以色列得胜处@@"),
         ("⛰️ 山","西奈山颁律（出19–20）；锡安山是神的居所","登山宝训（{{太5:1}}）、登山变像（{{太17:1-8}}）、加利利山上的大使命（{{太28:16}}）","^^比摩西更大的那一位在山上说话^^"),
         ("🌊 海","深渊与海象征混乱与敌对（诗74:13；但7:2-3）","耶稣斥责风和海（{{可4:39}}），在海面上行走（{{约6:19}}）","**唯有创造主能管辖海**（伯9:8）"),
         ("🏛️ 圣殿","神在祂百姓中间的居所（王上8）","「这里有一人比殿更大」（{{太12:6}}）；「以他的身体为殿」（{{约2:21}}）","==神同在的应许在基督里应验==（以马内利）"),
         ("🚪 城门外","赎罪祭牲的身体烧在营外（利16:27）","耶稣被带到城外的各各他钉死（{{约19:17}}）","^^祂在城门外受苦，使我们成圣^^"),
         ("🫗 井与水","旷野磐石出水（出17）；先知应许活水（赛55:1；结47）","雅各井旁的活水（{{约4:14}}）；住棚节宣告「活水的江河」（{{约7:37-38}}）","@@旧的水源 → 基督所赐的活水@@"),
         ("🧭 外邦之地","神应许万国因亚伯拉罕的后裔得福（创22:18）","推罗、西顿、低加波利的神迹（{{可7:24-37}}）；外邦百夫长的信心（{{太8:10-11}}）","==亚伯拉罕之约向万国展开=="),]
LIFE = [("🏠","平顶房","木梁上铺树枝和泥土，可以「拆了房顶」把瘫子缒下来（{{可2:4}}）；屋顶也是祷告、晾晒之处。"),
        ("⛵","一世纪渔船","1986 年加利利海西北岸干旱，泥中出土一艘约 8.2 米长的一世纪木船，可容十余人——与门徒同船渡海的情景吻合（{{可4:36}}）。"),
        ("🍷","婚宴","婚宴常持续七天，酒用完是主人家的羞辱；耶稣在迦拿变水为酒（{{约2:1-11}}），预表弥赛亚筵席的喜乐（赛25:6）。"),
        ("🪨","滚石坟墓","富人的凿岩坟墓以圆石封门；妇女们担心「谁给我们把石头从墓门滚开呢」（{{可16:3}}）。"),
        ("🕰️","犹太时辰","从日出算起：「巳初」约上午九点钉十字架（{{可15:25}}），「午正到申初」遍地黑暗（{{可15:33}}）。"),
        ("🌙","四更天","罗马式守夜把夜分为四更；「夜里约有四更天」即凌晨三至六点，耶稣在海面上走向门徒（{{可6:48}}）。")]
MONEY = [["第纳尔（银币）","一个劳工一天的工价","{{太20:2}}；{{太22:19}}"],["小钱（勒普顿）","最小的铜币，约第纳尔的 1/128","{{可12:42}}"],["丁税（两个银币）","每个犹太成年男子每年的圣殿税","{{太17:24}}"],["三十块钱","出卖耶稣的价银，应验撒迦利亚书","{{太26:15}}；亚11:12"],["一百第纳尔 vs 一千万银子","饶恕的比喻：所欠的是天文数字","{{太18:24-28}}"]]
WALK=[("伯利恒 → 耶路撒冷",9,"约 2 小时","博士从耶路撒冷再走一小段，就到大卫的城（{{太2:1-8}}）","#a78bfa"),
      ("耶利哥 → 耶路撒冷",27,"约 1 天（上升 1,000 多米）","好撒玛利亚人的路；耶稣最后一次上耶路撒冷（{{路10:30}}；{{路19:1-28}}）","#fb923c"),
      ("拿撒勒 → 迦百农",45,"约 1.5 天","耶稣离开拿撒勒，住在迦百农（{{太4:13}}）","#2dd4bf"),
      ("耶路撒冷 → 以马忤斯",11,"约 2–3 小时","「离耶路撒冷约有二十五里」（{{路24:13}}）","#34d399"),
      ("拿撒勒 → 耶路撒冷（经约旦河谷）",120,"约 4–5 天","十二岁上京过逾越节，回程走了一天才发现孩子不在（{{路2:41-45}}）","#ffc94a"),
      ("迦百农 → 该撒利亚腓立比",45,"约 1.5 天（北上进入外邦地）","彼得认信：「你是基督」（{{可8:27-29}}）","#60a5fa"),
      ("耶路撒冷 → 罗马（海路）",2300,"约 1–2 个月","福音「直到地极」——路加的第二卷书以罗马作结（徒28）","#ff5c93")]
def walk():
    mx=130; rows=[]
    for k,(n,km,t,d,c) in enumerate(WALK):
        w=min(100,km/mx*100); far=km>mx
        rows.append(f'<div class="wk reveal" style="--c:{c};--w:{w:.1f}%;--i:{k}"><div class="wk-h"><b>{esc(n)}</b><span>{km:,} 公里 · {esc(t)}</span></div><div class="wk-bar"><i></i>{"<em>⋯ 远超此比例</em>" if far else ""}<span class="walker">🚶</span></div><p>{md(d)}</p></div>')
    return '<div class="walk glass">'+"".join(rows)+'<p class="note">'+md("按一般步行每天约 30 公里估算；距离为今日道路的近似值。@@走路的福音@@：耶稣的教导大多是在路上、在同行中完成的（{{可10:32}}）。")+'</p></div>'
FEASTS=[("逾越节","尼散月 14（3–4 月）","🐑","羔羊的血，出埃及","^^神的羔羊^^，在逾越节被钉（{{约1:29}}；{{约19:36}}）","#ff5c93"),
        ("除酵节","尼散月 15–21","🫓","除去旧酵","在基督里作新团（林前5:7-8）；最后晚餐设立圣餐（{{路22:19-20}}）","#fb923c"),
        ("初熟节","安息日的次日","🌾","献上第一捆庄稼","七日的头一日复活：「睡了之人初熟的果子」（林前15:20）","#ffc94a"),
        ("五旬节","初熟节后第 50 天（5–6 月）","🔥","西奈颁律 / 麦收","圣灵浇灌，教会诞生（徒2）；律法写在心上","#34d399"),
        ("吹角节","提斯利月 1（9–10 月）","📯","吹角召聚","「号筒的大声」招聚选民（{{太24:31}}）","#2dd4bf"),
        ("赎罪日","提斯利月 10","🩸","大祭司进至圣所","一次献上、永远的赎罪；幔子裂开（{{可15:38}}）","#60a5fa"),
        ("住棚节","提斯利月 15–22","⛺","旷野住棚、取水点灯","「道成了肉身，住（支帐棚）在我们中间」；活水与世界的光（{{约7:37-38}}；{{约8:12}}）","#a78bfa")]
def feasts():
    import math
    cx=cy=260; R=190; n=len(FEASTS); s=['<div class="fw-wrap"><figure class="fwheel glass"><svg viewBox="0 0 520 520" role="img" aria-label="犹太节期轮"><circle cx="260" cy="260" r="236" class="fw-ring"/><circle cx="260" cy="260" r="150" class="fw-ring r2"/>']
    s.append('<g class="fw-rot">')
    for k,(nm,dt,ic,ot,nt,c) in enumerate(FEASTS):
        a=-math.pi/2+k*2*math.pi/n; x=cx+R*math.cos(a); y=cy+R*math.sin(a)
        s.append(f'<line x1="260" y1="260" x2="{x:.0f}" y2="{y:.0f}" stroke="{c}" class="fw-ray"/>')
    s.append('</g>')
    for k,(nm,dt,ic,ot,nt,c) in enumerate(FEASTS):
        a=-math.pi/2+k*2*math.pi/n; x=cx+R*math.cos(a); y=cy+R*math.sin(a)
        s.append(f'<g class="hot fw-n" tabindex="0" role="button" data-n="{esc(nm)}（{esc(dt)}）" data-i="旧约：{esc(ot)}。在基督里：{esc(re.sub(r"[{{}}^]","",nt))}" style="--d:{k*-0.7}s"><circle cx="{x:.0f}" cy="{y:.0f}" r="44" fill="{c}" fill-opacity=".25" style="stroke:{c};stroke-width:3"/><text x="{x:.0f}" y="{y-4:.0f}" text-anchor="middle" class="fw-ic">{ic}</text><text x="{x:.0f}" y="{y+22:.0f}" text-anchor="middle" class="fw-t">{nm}</text></g>')
    s.append('<circle cx="260" cy="260" r="80" fill="url(#fw-c)"/><defs><radialGradient id="fw-c"><stop offset="0" stop-color="#fff3c4"/><stop offset="1" stop-color="#f59e0b"/></radialGradient></defs><text x="260" y="254" text-anchor="middle" class="fw-c1">✝️ 基督</text><text x="260" y="280" text-anchor="middle" class="fw-c2">节期的实体</text></svg><figcaption>点按节期 · 春季四节（受难 · 复活 · 圣灵）已应验，秋季三节指向再来与完成</figcaption></figure>')
    s.append('<div class="fw-list">'+"".join(f'<div class="fwl" style="--c:{c}"><span>{ic}</span><div><b>{esc(nm)}</b> <small>{esc(dt)}</small><p>📜 {esc(ot)} → {md(nt)}</p></div></div>' for nm,dt,ic,ot,nt,c in FEASTS)+'</div></div>')
    s.append('<div class="mm-info fw-info" aria-live="polite">👆 点按节期轮上的节期，查看旧约含义与在基督里的应验。</div>')
    return "".join(s)
def build():
    b = []
    cards = [("map-med","maps.html","🌍","罗马世界与四福音写作地"),("map-galilee","maps.html","⛵","加利利海事工圈"),("map-elev","maps.html","⛰️","地形剖面：上耶路撒冷"),("map-temple","maps.html","🏛️","希律圣殿平面"),
             ("map-pal","history.html","🗺️","巴勒斯坦七段路线"),("map-jer","history.html","🏙️","耶路撒冷受难周"),("map-herod","history.html","👑","希律分封与罗马巡抚"),
             ("map-mat","matthew.html","👑","马太的足迹"),("map-mrk","mark.html","🦁","马可的足迹"),("map-luk","luke.html","🩺","路加的足迹"),("map-jhn","john.html","🦅","约翰的足迹")]
    b.append('<h2 id="m0">🧭 地图总览：11 张地图 × 2 层</h2><div class="callout c-key"><b>💡 怎样用这些地图</b><p>'+md("每张地图 = **🎨 讲解图**（内联 SVG，离线也一定显示，可点按地点） + **🛰️ 实时地图**（Leaflet 本地打包，不依赖 CDN）。实时地图有 **17 个全球底图**：打开时先@@并行测速@@，把你网络下连得上的排在前面；某个源中途失败就@@自动换下一个@@；全部失败时讲解图照常可用。地图在滑到附近时才载入，不拖慢页面。")+'</p></div>')
    b.append('<div class="atlas">'+"".join(f'<a class="atl" href="{h if h!="maps.html" else ""}#{i}"><span>{ic}</span><b>{t}</b><small>{h.replace(".html","")}</small></a>' for i,h,ic,t in cards)+'</div>')
    b.append('<h2 id="mw">🗺️ 四张专题地图</h2>')
    b.append('<h3 id="m1">🌍 罗马世界：福音从耶路撒冷到万邦</h3>'+maps.med())
    b.append('<h3 id="m2">⛵ 加利利海：事工的心脏地带</h3>'+maps.galilee())
    b.append('<h3 id="m3">⛰️ 地形剖面：上耶路撒冷，下耶利哥</h3>'+maps.elevation())
    b.append('<h3 id="m4">🏛️ 希律圣殿：从隔离到开路</h3>'+maps.temple())
    b.append('<h2 id="mg">🧩 地理 · 距离 · 节期：读懂福音书的空间与时间</h2>')
    b.append('<h3 id="m5">🧩 地理就是神学：七个地方，一条救赎线</h3><p class="note">'+md("福音书作者不是随意记地名：同一个地方在旧约已有含义，福音书在基督里把它==带到应验==。")+'</p>'+tbl(["地点类型","旧约背景","福音书中","记忆钩"],GEO_T))
    b.append('<h3 id="m5d">🚶 步行距离：耶稣与门徒怎样走路</h3>'+walk())
    b.append('<h3 id="m5f">🕎 节期轮：一年七个节期，都在基督身上应验</h3>'+feasts())
    b.append('<h2 id="m6">🏺 一世纪生活与文化</h2><h3 id="m6a">🏠 生活场景</h3><div class="kws">'+"".join(f'<div class="kwc"><span>{a}</span><b>{t}</b><p>{md(d)}</p></div>' for a,t,d in LIFE)+'</div>')
    b.append('<h3 id="m6b">💰 福音书里的钱</h3>'+tbl(["币值","大约价值","经文"],MONEY))
    b.append('<h2 id="m7">🛰️ 底图来源与离线保障</h2><h3 id="m7a">⚙️ 载入与自动回退流程</h3><div class="flow">'+"".join(f'<div class="fstep"><span class="n">{k+1}</span>{t}</div>'+('<i class="farr">➜</i>' if k<4 else '') for k,t in enumerate(["滑到地图附近（IntersectionObserver）","载入本站自带的 Leaflet（无 CDN）","17 个底图并行测速 1 张瓦片（结果缓存 30 分钟），按钮亮绿点 / 红点","先用首选底图；它连不上 → 改用测速可用的下一个","中途 8 秒无瓦片或连续出错 → 再换；全部失败 → 讲解图照常可用"]))+'</div>')
    b.append('<h3 id="m7b">📡 17 个实测底图</h3>'+tbl(["底图","说明","适合"],[[f"**{a}**",c,d] for a,c,d in PROV]))
    b.append('<p class="note">'+md("底图版权分别属于 OpenStreetMap 贡献者、Esri 及其数据提供方、OpenTopoMap、DARE（Johan Åhlfeldt，哥德堡大学）与高德；地图右下角会显示当前底图署名。2026-11-14 实测：CARTO、Stadia/Stamen、Thunderforest 返回「API KEY REQUIRED」占位图，Wikimedia、Mapy.cz 拒绝外站调用（403），本站均未采用。")+'</p>')
    return "".join(b)
