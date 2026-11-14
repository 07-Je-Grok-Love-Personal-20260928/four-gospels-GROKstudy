# 性能测量：Playwright 滚动帧率 / 长任务 + Lighthouse（移动 / 桌面）。用法：python3 tools/perf.py <label> [docs_dir]
import asyncio, json, os, sys, subprocess, time
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABEL=sys.argv[1] if len(sys.argv)>1 else "run"; D=sys.argv[2] if len(sys.argv)>2 else os.path.join(ROOT,"docs")
OUT=os.path.join(ROOT,"build","perf"); os.makedirs(OUT,exist_ok=True)
PORT=int(os.environ.get("PORT","8931")); PAGES=os.environ.get("PAGES","index,matthew,maps,synoptic,creeds").split(",")
INJ="""window.__ft=[];window.__lt=[];(function(){let l=performance.now();function f(t){__ft.push(t-l);l=t;requestAnimationFrame(f)}requestAnimationFrame(f);
try{new PerformanceObserver(e=>e.getEntries().forEach(x=>__lt.push(x.duration))).observe({type:'longtask',buffered:true})}catch(e){}})();"""
async def scroll_test(br, f, mobile):
    ctx=await br.new_context(viewport={"width":390,"height":844} if mobile else {"width":1440,"height":900}, device_scale_factor=3 if mobile else 1, is_mobile=mobile, has_touch=mobile)
    pg=await ctx.new_page(); cdp=await ctx.new_cdp_session(pg)
    if mobile: await cdp.send("Emulation.setCPUThrottlingRate",{"rate":4})
    await pg.goto(f"http://127.0.0.1:{PORT}/{f}.html", wait_until="load"); await pg.wait_for_timeout(1500)
    await pg.evaluate(INJ); await pg.wait_for_timeout(300); await pg.evaluate("__ft.length=0;__lt.length=0")
    H=await pg.evaluate("document.documentElement.scrollHeight-innerHeight"); steps=0; t0=time.time()
    while time.time()-t0<8:
        if mobile: await pg.evaluate("window.scrollBy(0,140)")
        else: await pg.mouse.wheel(0,160)
        await pg.wait_for_timeout(16); steps+=1
    await pg.wait_for_timeout(500)
    r=await pg.evaluate("({ft:__ft,lt:__lt,y:scrollY})")
    ft=sorted(r["ft"]); n=len(ft); await ctx.close()
    avg=sum(ft)/n if n else 0
    return {"frames":n,"fps":round(1000/avg,1) if avg else 0,"p95_ms":round(ft[int(n*.95)],1) if n else 0,"jank_gt50":sum(1 for x in ft if x>50),"longtasks":len(r["lt"]),"lt_total_ms":round(sum(r["lt"])),"scrolled":round(r["y"]),"height":H}
def lh(f, mode):
    o=os.path.join(OUT,f"lh_{LABEL}_{f}_{mode}.json")
    cmd=["lighthouse",f"http://127.0.0.1:{PORT}/{f}.html","--quiet","--output=json",f"--output-path={o}","--only-categories=performance","--chrome-flags=--headless=new --no-sandbox"]
    if mode=="desktop": cmd.append("--preset=desktop")
    subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=240)
    j=json.load(open(o)); a=j["audits"]
    return {"score":round(j["categories"]["performance"]["score"]*100),"LCP_ms":round(a["largest-contentful-paint"]["numericValue"]),"TBT_ms":round(a["total-blocking-time"]["numericValue"]),"CLS":round(a["cumulative-layout-shift"]["numericValue"],3),"FCP_ms":round(a["first-contentful-paint"]["numericValue"])}
async def main():
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"-d",D,"--bind","127.0.0.1"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    res={}
    try:
        async with async_playwright() as p:
            br=await p.chromium.launch(args=["--enable-gpu-rasterization"])
            for f in PAGES:
                res[f]={"scroll_mobile":await scroll_test(br,f,True),"scroll_desktop":await scroll_test(br,f,False)}
            await br.close()
        if os.environ.get("LH","1")=="1":
            for f in PAGES:
                for m in ("mobile","desktop"):
                    try: res[f]["lh_"+m]=lh(f,m)
                    except Exception as e: res[f]["lh_"+m]=str(e)[:80]
    finally: srv.kill()
    json.dump(res,open(os.path.join(OUT,f"perf_{LABEL}.json"),"w"),ensure_ascii=False,indent=1)
    for f,v in res.items(): print(f, json.dumps(v,ensure_ascii=False))
asyncio.run(main())
