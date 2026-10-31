# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import page, QUOTES, VER, DATE, md
from gsp1 import MAT, MRK; from gsp2 import LUK, JHN
from gpage import gospel
import geo, palgeo, p_whole, p_hist, p_syn, p_doc, p_creed, p_mem, p_misc
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(D, "assets", "geo"), exist_ok=True)
geo.base_svg(os.path.join(D, "assets", "geo", "med.svg")); palgeo.base_svg(os.path.join(D, "assets", "geo", "pal.svg"))
EPS = [MAT, MRK, LUK, JHN]
def W(fn, html):
    open(os.path.join(D, fn), "w", encoding="utf-8").write(html); print("wrote", fn, len(html)//1024, "KB")
W("index.html", page("index.html", "四福音书深读", "马太 · 马可 · 路加 · 约翰 · 整本圣经与圣约 · 时间故事地图 · 欧陆改革宗 · 三项联合信条与三大信经逐字对照", p_misc.index(EPS), "home"))
W("bible.html", page("bible.html", "整本圣经与圣约", "先看全景：福音书在创造—堕落—救赎—成全的救赎历史与恩典之约中的位置", p_whole.build()))
W("history.html", page("history.html", "时间 · 故事 · 地图", "主前 63–主后 95：第二圣殿时期、耶稣生平十幕、巴勒斯坦地图、耶路撒冷受难周、文化与群体", p_hist.build()))
SUB = {"mat":"君王弥赛亚与天国：应验旧约的大卫子孙、五篇讲论、大使命","mrk":"受苦的仆人：立刻行动的神的儿子，十字架是认信的高峰",
       "luk":"万人的救主：按次序考察的历史、寻找失丧的人、圣灵与祷告","jhn":"道成肉身的神子：七神迹、七个“我是”、信而得生命"}
for e in EPS: W(e["fn"], page(e["fn"], f'{e["ic"]} {e["n"]}', SUB[e["id"]], gospel(e)))
W("synoptic.html", page("synoptic.html", "对观 · 和谐 · 受难周", "对观问题与改革宗默示观、福音和谐对照表、受难周逐日、十架七言、复活显现", p_syn.build()))
W("doctrine.html", page("doctrine.html", "教义主题 · 信条对照", "十大教义主题，从福音书经文到三项联合信条（CCI 逐字）与威斯敏斯特标准", p_doc.build()))
W("creeds.html", page("creeds.html", "三大普世信经", "使徒信经 · 尼西亚信经 · 亚他那修信经：干净背诵版、深度对比、为何有三份", p_creed.build()))
W("memory.html", page("memory.html", "记忆 · 自测", "口诀、钥字、记忆卡、钥节填空、题库小考、记忆宫殿与通读计划", p_mem.build(EPS)))
json.dump([[k, str(a), b] for k, a, b in QUOTES], open(os.path.join(ROOT, "build", "quotes.json"), "w"), ensure_ascii=False, indent=0)
stats_f = os.path.join(ROOT, "build", "verify_stats.json")
stats = json.load(open(stats_f)) if os.path.exists(stats_f) else [["状态", "尚未运行 verify.py"]]
W("sources.html", page("sources.html", "来源 · 校验", "引用来源、逐字校验结果、局限说明与版本记录", p_misc.sources(stats)))
open(os.path.join(D, ".nojekyll"), "w").write("")
print("quotes:", len(QUOTES))
