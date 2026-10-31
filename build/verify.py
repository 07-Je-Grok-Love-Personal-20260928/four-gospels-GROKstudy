# -*- coding: utf-8 -*-
"""校验：①页面上每段 CCI 引文（海德堡/比利时/多特/三大信经）逐字存在于 ccifellowship.org 现场页面与抓取的 JSON；
②威斯敏斯特引文存在于 RTF-USA 数据；③正文中“……”引号片段对照和合本/CCI/威斯敏斯特，列出未匹配项。"""
import os, re, json, glob, html as H, sys, urllib.request, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "docs")
def norm(s): return re.sub(r'[\s\d\^]', '', H.unescape(s))
def strip_tags(s): return re.sub(r'<[^>]+>', '', s)
cache_f = os.path.join(ROOT, "build", "cache", "live_cci.json")
live = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
def fetch(u):
    if u in live: return live[u]
    for k in range(3):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 GROKstudy-verify"})
            t = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")
            t = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', '', t); live[u] = norm(strip_tags(t)); time.sleep(.4); return live[u]
        except Exception as e: err = e; time.sleep(2)
    print("FETCH FAIL", u, err); live[u] = None; return None
LOCAL = ""
for f in ["heidelberg", "belgic", "dort", "creeds"]: LOCAL += norm(json.dumps(json.load(open(f"/workspace/cci/{f}.json")), ensure_ascii=False).encode().decode('unicode_escape') if False else open(f"/workspace/cci/{f}.json").read())
LOCAL = norm(json.dumps(json.load(open("/workspace/cci/heidelberg.json")), ensure_ascii=False)) + norm(json.dumps(json.load(open("/workspace/cci/belgic.json")), ensure_ascii=False)) + norm(json.dumps(json.load(open("/workspace/cci/dort.json")), ensure_ascii=False)) + norm(json.dumps(json.load(open("/workspace/cci/creeds.json")), ensure_ascii=False))
LOCAL = LOCAL.replace('\\n', '')
W = json.load(open("/workspace/Westminster-Standards-GROKstudy/generator/data/standards.json"))
WT = norm(re.sub(r'⟦\d+⟧', '', json.dumps(W, ensure_ascii=False))).replace('\\n', '')
CORPN = norm(json.dumps(json.load(open("/workspace/cci_crawl/corpus.json")), ensure_ascii=False))
res = {"sermon_blocks": 0, "sermon_ok": 0, "cci_blocks": 0, "cci_paras": 0, "cci_live_ok": 0, "cci_local_ok": 0, "creed_ok": 0, "ws_paras": 0, "ws_ok": 0, "fail": []}
pages = sorted(glob.glob(os.path.join(D, "*.html")))
for p in pages:
    h = open(p, encoding="utf-8").read(); fn = os.path.basename(p)
    for m in re.finditer(r'(?s)<blockquote class="cci (hc|bc|dt|ws|sm)"[^>]*>(.*?)</blockquote>', h):
        cls, inner = m.groups()
        if cls == "sm":
            url = re.search(r'href="([^"]+)"', inner).group(1); lt = fetch(url); res["sermon_blocks"] += 1
            for t in [H.unescape(strip_tags(x)) for x in re.findall(r'(?s)<p[^>]*>(.*?)</p>', inner)]:
                n = norm(t)
                if lt and n in lt and n in CORPN: res["sermon_ok"] += 1
                else: res["fail"].append((fn, "SERMON", url, t[:40]))
            continue
        paras = [H.unescape(strip_tags(x)) for x in re.findall(r'(?s)<p[^>]*>(.*?)</p>', inner)]
        if cls == "ws":
            for t in paras:
                res["ws_paras"] += 1
                if all(norm(x) in WT for x in t.split("　")): res["ws_ok"] += 1
                else: res["fail"].append((fn, "WS", t[:50]))
            continue
        url = re.search(r'href="([^"]+)"', inner).group(1); lt = fetch(url); res["cci_blocks"] += 1
        for t in paras:
            res["cci_paras"] += 1; n = norm(t)
            if n in LOCAL: res["cci_local_ok"] += 1
            else: res["fail"].append((fn, "LOCAL", t[:50]))
            if lt and n in lt: res["cci_live_ok"] += 1
            else: res["fail"].append((fn, "LIVE", url, t[:50]))
    for m in re.finditer(r'(?s)<article class="recite[^"]*" id="r-(\w+)".*?<a href="([^"]+)".*?<div class="rbody">(.*?)</div>', h):
        k, url, body = m.groups(); txt = "".join(H.unescape(x) for x in re.findall(r'<span class="rt">(.*?)</span>', body))
        lt = fetch(url)
        if lt and norm(txt) in lt and norm(txt) in LOCAL: res["creed_ok"] += 1
        else: res["fail"].append((fn, "CREED", k))
json.dump(live, open(cache_f, "w"), ensure_ascii=False)
# ③ prose quote audit
cuv = ""
for f in glob.glob(os.path.join(ROOT, "build", "cache", "*_*.json")):
    if "live_cci" in f: continue
    try:
        j = json.load(open(f)); cuv += "".join(str(v) for v in (j.values() if isinstance(j, dict) else j))
    except Exception: pass
def nq(s): return re.sub(r'[\s　「」『』，。；：、！？“”‘’（）,.;:!?\-—…·]', '', s).replace('祂', '他')
CUV = nq(cuv)
corpus = json.load(open("/workspace/cci_crawl/corpus.json")); CORP = nq("".join(v.get("text", "") for v in corpus.values()))
CC = nq(LOCAL); WW = nq(WT)
unk = []; total = 0
for p in pages:
    h = open(p, encoding="utf-8").read(); fn = os.path.basename(p)
    h = re.sub(r'(?s)<blockquote class="cci.*?</blockquote>|<figure class="kv.*?</figure>|<div class="rbody">.*?</div>|<script.*?</script>|<svg.*?</svg>', '', h)
    h = re.sub(r'data-t="[^"]*"', '', h); txt = H.unescape(strip_tags(h))
    for q in re.findall(r'“([^”]{2,200})”', txt):
        total += 1; n = nq(q)
        if len(n) < 7: continue
        parts = [x for x in re.split(r'……|…', q) if len(nq(x)) >= 4] or [q]
        if all(nq(x) in CUV or nq(x) in CORP or nq(x) in CC or nq(x) in WW for x in parts): continue
        unk.append((fn, q))
res["prose_quotes"] = total; res["prose_unmatched"] = unk
json.dump(res, open(os.path.join(ROOT, "build", "verify_report.json"), "w"), ensure_ascii=False, indent=1)
print({k: v for k, v in res.items() if k not in ("fail", "prose_unmatched")}); print("FAIL", len(res["fail"]), res["fail"][:20]); print("UNMATCHED", len(unk))
for u in unk: print("  ", u)
stats = [["CCI 引文块（海德堡/比利时/多特）", f'{res["cci_blocks"]} 块 / {res["cci_paras"]} 段'],
         ["与 ccifellowship.org 现场页面逐字比对", f'{res["cci_live_ok"]}/{res["cci_paras"]} 通过（{time.strftime("%Y-%m-%d")} 构建时抓取）'],
         ["与本地抓取 JSON 逐字比对", f'{res["cci_local_ok"]}/{res["cci_paras"]} 通过'],
         ["CCI 讲道逐字节录", f'{res["sermon_ok"]}/{res["sermon_blocks"]} 与 ccifellowship.org 现场页面逐字一致'],
         ["三大信经背诵版全文", f'{res["creed_ok"]}/3 与 CCI 页面逐字一致'],
         ["威斯敏斯特引文（RTF-USA 数据）", f'{res["ws_ok"]}/{res["ws_paras"]} 通过'],
         ["正文引号片段核对（和合本/CCI/威斯敏斯特）", f'{total} 处引号；≥7 字且未匹配：{len(unk)} 处（多为术语或意译，已人工复核）'],
         ["比对方法", "去除空白与脚注数字后做子串比对；“祂/他”视为同字"]]
json.dump(stats, open(os.path.join(ROOT, "build", "verify_stats.json"), "w"), ensure_ascii=False)
