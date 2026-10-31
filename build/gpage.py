# -*- coding: utf-8 -*-
from common import md, esc, cq, wq, sq, verse_card, vtext
from geo import minimap
def flow(steps, end):
    s='<div class="flow">'
    for i,t in enumerate(steps): s+=f'<div class="fstep"><span class="n">{i+1}</span>{md(t)}</div><i class="farr">➜</i>'
    return s+f'<div class="fstep end">📖 {md(end)}</div></div>'
def sbar(ol):
    tot=sum(w for _,_,w in ol)
    return '<div class="sbar">'+"".join(f'<div class="seg" style="flex:{w/tot*100:.1f}" title="{esc(r)} {esc(t)}"><b>{esc(r)}</b><span>{esc(t)}</span></div>' for r,t,w in ol)+'</div>'
def tbl(head, rows):
    return '<div class="tbl"><table><thead><tr>'+"".join(f'<th>{h}</th>' for h in head)+'</tr></thead><tbody>'+"".join('<tr>'+"".join(f'<td>{md(c)}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def mindtree(e):
    br="".join(f'<li style="--gc:{e["col"]}"><span class="mt-b">{esc(r)}</span><ul><li><span>{esc(t)}</span></li></ul></li>' for r,t,_ in e["ol"])
    return f'<div class="mtree glass reveal"><div class="mt-root">{e["ic"]} {e["n"]} · {e["kw"]}</div><ul class="mt-l1">{br}</ul></div>'
def ladder(steps):
    s='<div class="ladder">'
    for i,(r,who,t) in enumerate(steps): s+=f'<div class="rung reveal" style="--i:{i}"><span class="rn">{i+1}</span><b>{md(r)}</b><small>{esc(who)}</small><p>{md(t)}</p></div>'
    return s+'</div>'
SPECIAL = {
 "mat": lambda: ('<h3 id="mat-sp1">📌 十处“应验”套语</h3><p class="note">马太常用「这一切的事成就，是要应验主藉先知所说的话」一类套语，把耶稣的一生与旧约连起来（括号内为所引旧约）。</p>'
   + tbl(["太","事件","旧约出处","圣经神学意义"],[["{{太1:22-23}}","童女怀孕","赛7:14","以马内利：神与人同在"],["{{太2:15}}","从埃及召出","何11:1","耶稣是真以色列、神的儿子"],["{{太2:17-18}}","伯利恒屠婴","耶31:15","被掳的哀哭中有新约的盼望（耶31:31）"],["{{太2:23}}","称为拿撒勒人","众先知（可能暗指赛11:1“枝子”）","卑微的“枝子”弥赛亚"],["{{太4:14-16}}","在加利利传道","赛9:1-2","外邦的加利利见了大光"],["{{太8:17}}","医病赶鬼","赛53:4","受苦的仆人担当我们的软弱"],["{{太12:17-21}}","不争竞不喧嚷","赛42:1-4","仆人把公理传给外邦"],["{{太13:35}}","用比喻讲论","诗78:2","把创世以来隐藏的事发明出来"],["{{太21:4-5}}","骑驴进城","亚9:9","谦和的王来到锡安"],["{{太27:9-10}}","三十块钱","亚11:12-13（并耶利米书）","被弃的牧人"]])
   + '<h3 id="mat-sp2">📚 五大讲论：新的“五经”</h3>'
   + tbl(["讲论","章","主题","结尾套语"],[["① 登山宝训","5–7","天国子民的义","{{太7:28}}"],["② 差遣讲论","10","天国的使者与逼迫","{{太11:1}}"],["③ 比喻讲论","13","天国的奥秘：已然与未然","{{太13:53}}"],["④ 群体讲论","18","天国子民彼此相待：谦卑、挽回、饶恕","{{太19:1}}"],["⑤ 末世讲论","24–25","天国的完成：儆醒与审判","{{太26:1}}"]])),
 "mrk": lambda: ('<h3 id="mrk-sp1">🪜 认信的阶梯：“这到底是谁？”</h3>'
   + ladder([("{{可1:1}}","作者","“神的儿子，耶稣基督福音的起头”"),("{{可1:11}}","天父","“你是我的爱子，我喜悦你。”"),("{{可1:24}}","污鬼","“我知道你是谁，乃是神的圣者。”"),("{{可4:41}}","门徒","“这到底是谁，连风和海也听从他了。”"),("{{可8:29}}","彼得","“你是基督。”"),("{{可14:61-62}}","耶稣自己","“我是。你们必看见人子坐在那权能者的右边”"),("{{可15:39}}","罗马百夫长","“这人真是神的儿子！”")])
   + '<h3 id="mrk-sp2">✝️ 三次受难预言的同一模式</h3>'
   + tbl(["","预言","门徒的误解","耶稣的教导"],[["第一次","{{可8:31}}","彼得劝阻（8:32）","{{可8:34}} 舍己、背十字架"],["第二次","{{可9:31}}","争论谁为大（9:34）","{{可9:35}} 作众人的用人"],["第三次","{{可10:33-34}}","雅各约翰求坐左右（10:37）","{{可10:45}} 人子来是要服事人"]])
   + '<p class="note">'+md("记忆：**预言 → 误解 → 教导**，三次重复。紧接着是医治瞎子巴底买（{{可10:46-52}}）——真正“看见”的人在路上跟随耶稣。")+'</p>'),
 "luk": lambda: ('<h3 id="luk-sp1">🎵 降生故事的四首诗歌</h3>'
   + tbl(["诗歌（拉丁传统名）","唱者","经文","主题"],[["马利亚颂（Magnificat）","马利亚","{{路1:46-55}}","神叫卑贱的升高；记念亚伯拉罕之约"],["撒迦利亚颂（Benedictus）","撒迦利亚","{{路1:68-79}}","记念圣约与起誓；大卫家的拯救之角"],["荣耀颂（Gloria）","天使天军","{{路2:14}}","在至高之处荣耀归与神"],["西面颂（Nunc Dimittis）","西面","{{路2:29-32}}","照亮外邦人的光；以色列的荣耀"]])
   + '<h3 id="luk-sp2">🗝️ 路加独有的比喻（节选）</h3>'
   + tbl(["比喻","经文","核心"],[["好撒玛利亚人","{{路10:30-37}}","谁是我的邻舍？——去照样行"],["无知的财主","{{路12:16-21}}","在神面前不富足"],["失羊 · 失钱 · 浪子","{{路15:4-32}}","天上为一个罪人悔改欢喜"],["不义的管家","{{路16:1-13}}","用今生钱财为永生打算"],["财主与拉撒路","{{路16:19-31}}","死后的分别；摩西和先知的话已足够"],["纠缠的寡妇","{{路18:1-8}}","常常祷告，不可灰心"],["法利赛人与税吏","{{路18:9-14}}","自以为义 vs 求怜悯——称义"]])),
 "jhn": lambda: ('<h3 id="jhn-sp1">✨ 七个神迹（“神迹之书”）</h3>'
   + tbl(["#","神迹","经文","显明"],[["1","变水为酒","{{约2:1-11}}","新约的喜乐取代旧约洁净礼"],["2","医治大臣的儿子","{{约4:46-54}}","话语的权能，远距离医治"],["3","医好毕士大的病人","{{约5:1-9}}","安息日的主，与父同工"],["4","五饼二鱼","{{约6:1-14}}","生命的粮"],["5","行在海面","{{约6:16-21}}","“是我，不要怕”"],["6","医治生来瞎眼的","{{约9:1-7}}","世界的光"],["7","叫拉撒路复活","{{约11:1-44}}","复活与生命"]])
   + '<h3 id="jhn-sp2">🔔 七个“我是”</h3>'
   + tbl(["#","“我是……”","经文","旧约背景"],[["1","生命的粮","{{约6:35}}","旷野的吗哪（出16）"],["2","世界的光","{{约8:12}}","住棚节的灯；云柱火柱"],["3","羊的门","{{约10:9}}","羊圈与救恩的入口"],["4","好牧人","{{约10:11}}","结34；诗23"],["5","复活与生命","{{约11:25}}","但12:2；结37"],["6","道路、真理、生命","{{约14:6}}","到父那里去的唯一道路"],["7","真葡萄树","{{约15:1}}","以色列是葡萄树（诗80；赛5）"]])
   + '<p class="note">'+md("另有不带比喻的“我是”：{{约8:58}}“还没有亚伯拉罕就有了我”，呼应出3:14 神的名，犹太人因此拿石头要打祂。")+'</p>'),
}
def gospel(e):
    i=e["id"]
    facts=[("✍️","作者",e["au"]),("📅","写作时间",e["date"]),("📍","写作地点",e["place"]),("👥","原初读者",e["to"]),("🎨","耶稣的画像",e["port"]),("🐾","传统象征",e["sym"]),("🔗","总纲经文",e["acts"]),("📏","篇幅",f'{e["ch"]} 章 · 印记：{e["stamp"]}')]
    fx="".join(f'<div class="fact"><span class="fi">{a}</span><b>{b}</b><p>{md(c)}</p></div>' for a,b,c in facts)
    angs="".join(f'<div class="ang"><b>{k}</b><p>{md(v)}</p></div>' for k,v in e["ang"].items())
    keys="".join(f'<li>{md(k)}</li>' for k in e["key"])
    hards="".join(f'<details class="hardq"><summary>⚠️ {md(q)}</summary><p>{md(a)}</p></details>' for q,a in e["hard"])
    confs="".join(cq(c) for c in e["conf"])+"".join(wq(*w) for w in e.get("ws",[]))
    serm=sq(*e["sermon"])+(sq(*e["sermon2"]) if "sermon2" in e else "")
    apps="".join(f'<li>{md(a)}</li>' for a in e["app"])
    ol="".join(f'<li><b>{esc(r)}</b> {md(t)}</li>' for r,t,_ in e["ol"])
    uq="".join(f'<li>{md(u)}</li>' for u in e["uniq"])
    loc = "写作地与原初读者所在地" if e["fr"]!=e["dest"] else "写作地（传统说法）"
    return f'''<section class="ep" id="{i}" style="--gc:{e["col"]}">
<div class="ep-banner glass reveal"><div class="kwbox"><span class="kwl">钥字</span><span class="kw">{e["kw"]}</span></div><p class="core">💎 {md(e["core"])}</p>{verse_card(e["kv"])}</div>
<h2 id="{i}-f">🪪 基本资料</h2><div class="facts-wrap"><div class="facts">{fx}</div><figure class="mm glass">{minimap(e)}<figcaption>{loc}（真实底图：Natural Earth；按经纬度定位）</figcaption></figure></div>
<h2 id="{i}-bg">🏺 背景与真实情境</h2><div class="two"><div class="card glass"><h4>历史背景</h4><p>{md(e["bg"])}</p></div><div class="card glass culture"><h4>🌍 文化区域特征</h4><p>{md(e["cul"])}</p></div></div>
<h2 id="{i}-why">❓ 为什么写（前因后果）</h2>{flow(e["why"], "于是写下《"+e["n"]+"》")}
<h2 id="{i}-what">📐 写了什么（结构）</h2>{sbar(e["ol"])}<ol class="outline">{ol}</ol>{mindtree(e)}<div class="angs">{angs}</div>
<h3 id="{i}-uq">🔎 本卷独有的材料</h3><div class="card glass"><ul class="keys">{uq}</ul></div>
{SPECIAL[i]()}
<h2 id="{i}-bt">📜 圣经神学：在整本圣经中的位置</h2><div class="card glass bt"><p>{md(e["bt"])}</p></div>
<h2 id="{i}-ct">🤝 圣约神学</h2><div class="card glass ct"><p>{md(e["ct"])}</p></div>
<h2 id="{i}-kh">🎯 重点与难点</h2><div class="two"><div class="card glass"><h4>⭐ 重点</h4><ul class="keys">{keys}</ul></div><div class="card glass"><h4>⚠️ 难点（点开看改革宗解答）</h4>{hards}</div></div>
<h2 id="{i}-cf">📘 信条对照（CCI 逐字）</h2><div class="confs">{confs}</div>
<h3 id="{i}-sm">🎙️ CCI 讲道节录</h3><div class="confs">{serm}</div>
<h2 id="{i}-ap">🌱 应用与记忆</h2><div class="two"><div class="card glass"><h4>今天怎样活</h4><ul class="apps">{apps}</ul></div><div class="flip" tabindex="0" role="button" aria-label="翻转记忆卡"><div class="fi-in"><div class="ff"><span>🧠 记忆钩</span><b>{e["n"]}</b><em>点按翻转</em></div><div class="fb"><p>{md(e["mn"])}</p></div></div></div></div>
</section>'''
