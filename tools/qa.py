# v2 Playwright QA：5 种宽度 × 13 页；逐一点击/展开全部交互元素，检查横向溢出、裁切、顶栏重叠、弹层越界、JS 错误、地图载入与底图切换
import asyncio, json, os, sys, subprocess, time, socket
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"docs"); OUT=os.path.join(ROOT,"build","qa"); os.makedirs(OUT,exist_ok=True)
PAGES=[f for f in sorted(os.listdir(D)) if f.endswith(".html")]
WIDTHS=[int(x) for x in os.environ.get("WIDTHS","360,390,768,1024,1440").split(",")]
CHECK=r"""()=>{const de=document.documentElement,vw=de.clientWidth,res={sw:de.scrollWidth,vw:vw,off:[],clip:[],hdr:[]};
const scrollers=n=>{for(let p=n.parentElement;p;p=p.parentElement){const s=getComputedStyle(p);if(/(auto|scroll|hidden|clip)/.test(s.overflowX)&&p!==document.body&&p!==de)return true;if(p.id==='toc'||p.id==='navdrop')return true}return false};
document.querySelectorAll('main *').forEach(n=>{if(n.closest('.leaflet-container,svg'))return;const r=n.getBoundingClientRect();if(!r.width||getComputedStyle(n).position==='fixed')return;
 if((r.right>vw+1||r.left<-1)&&!scrollers(n))res.off.push((n.className||n.tagName)+' '+Math.round(r.left)+'→'+Math.round(r.right));
 const s=getComputedStyle(n);if(['P','LI','TD','B','SPAN','A','H2','H3','H4','SMALL','BUTTON'].includes(n.tagName)&&s.overflowX==='visible'&&n.scrollWidth>n.clientWidth+2&&n.clientWidth>0&&s.display!=='inline'&&!scrollers(n))res.clip.push(n.tagName+'.'+n.className+':'+n.textContent.slice(0,20))});
const hs=[...document.querySelectorAll('.top > *')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.getBoundingClientRect());
for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.right>b.left+1&&b.right>a.left+1&&a.bottom>b.top&&b.bottom>a.top)res.hdr.push(i+'x'+j)}
res.off=res.off.slice(0,6);res.clip=res.clip.slice(0,6);return res}"""
async def safe_click(pg, loc, log, name):
    try:
        await loc.scroll_into_view_if_needed(timeout=3000); await loc.click(timeout=3000); return True
    except Exception as e:
        log.append(f"click-fail {name}: {str(e)[:80]}"); return False
async def run_page(pg, url, f, w, errs):
    log=[]; stats={}
    await pg.goto(url, wait_until="load"); await pg.wait_for_timeout(300)
    assert "四福音书" in await pg.title(), f
    # 1 TOC open/close
    TV="(()=>{const r=document.querySelector('#toc').getBoundingClientRect();return r.right>50&&r.left>=-1})()"
    v0=await pg.evaluate(TV)
    await safe_click(pg, pg.locator("#tocbtn"), log, "tocbtn"); await pg.wait_for_timeout(450)
    v1=await pg.evaluate(TV)
    if v1==v0: log.append(f"toc toggle had no effect ({v0})")
    if w<=1100 and v1:
        try: await pg.locator("#scrim").click(position={"x":w-12,"y":400},timeout=3000)
        except Exception as e: log.append("scrim click fail "+str(e)[:60])
    elif w>1100 and not v1: await safe_click(pg, pg.locator("#tocbtn"), log, "tocbtn2")
    await pg.wait_for_timeout(900)
    if w>1100 and not await pg.evaluate(TV): log.append("toc not restored")
    if w<=1100 and await pg.evaluate(TV): log.append("mobile toc not closed")
    # 1b TOC 三级折叠 + 拖动调宽（v2.1.0）
    if w<=1100: await safe_click(pg, pg.locator("#tocbtn"), log, "tocbtn-open"); await pg.wait_for_timeout(450)
    for tx in ["all","l1","l2","all"]:
        await safe_click(pg, pg.locator(f'#toc [data-tx="{tx}"]'), log, "toc-"+tx); await pg.wait_for_timeout(80)
        if tx=="l1" and await pg.evaluate("[...document.querySelectorAll('#toc li.l2')].some(e=>e.offsetParent)"): log.append("toc l1-only still shows l2")
        if tx=="all" and await pg.evaluate("[...document.querySelectorAll('#toc li.l3,#toc li.l2')].some(e=>!e.offsetParent)"): log.append("toc expand-all hides items")
    tg=pg.locator("#toc .tg"); ntg=await tg.count(); stats["toc_tg"]=ntg; stats["toc_lv"]=await pg.evaluate("[1,2,3].map(l=>document.querySelectorAll('#toc li.l'+l).length)")
    for k in range(ntg):
        if await tg.nth(k).is_visible(): await tg.nth(k).click(timeout=2000); await tg.nth(k).click(timeout=2000)
    async def toc_ok(tag):
        r=await pg.evaluate("""(()=>{const t=document.querySelector('#toc'),tr=t.getBoundingClientRect();const bad=[...t.querySelectorAll('a,button,input')].filter(e=>e.offsetParent).filter(e=>{const r=e.getBoundingClientRect();return r.right>tr.right+1||r.left<tr.left-1}).length;return {sw:t.scrollWidth,cw:t.clientWidth,bad,vw:innerWidth,right:tr.right}})()""")
        if r["sw"]>r["cw"]+1 or r["bad"] or r["right"]>r["vw"]+1: log.append(f"toc overflow {tag} {r}")
    await toc_ok("expanded")
    rs=pg.locator("#tocrs")
    if await rs.is_visible():
        bb=await rs.bounding_box(); x0=bb["x"]+bb["width"]/2; y0=bb["y"]+min(300,bb["height"]/2)
        w0=await pg.evaluate("document.querySelector('#toc').getBoundingClientRect().width")
        await pg.mouse.move(x0,y0); await pg.mouse.down(); await pg.mouse.move(x0+160,y0,steps=6); await pg.mouse.up(); await pg.wait_for_timeout(250)
        w1=await pg.evaluate("document.querySelector('#toc').getBoundingClientRect().width")
        if w1<=w0+20 and w0<min(720,w*0.6)-30: log.append(f"toc drag-wider failed {w0}->{w1}")
        await toc_ok("wide")
        if w>1100:
            ml=await pg.evaluate("document.querySelector('main').getBoundingClientRect().left")
            if abs(ml-w1)>2: log.append(f"main not following toc width {ml} vs {w1}")
        bb=await rs.bounding_box(); await pg.mouse.move(bb["x"]+bb["width"]/2,y0); await pg.mouse.down(); await pg.mouse.move(40,y0,steps=6); await pg.mouse.up(); await pg.wait_for_timeout(250)
        w2=await pg.evaluate("document.querySelector('#toc').getBoundingClientRect().width")
        if w2<219: log.append(f"toc min clamp failed {w2}")
        await toc_ok("narrow"); stats["toc_drag"]=[round(w0),round(w1),round(w2)]
        if await pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"): log.append("page overflow after toc drag")
        await rs.dblclick(); await pg.wait_for_timeout(200)
    if w<=1100:
        await safe_click(pg, pg.locator("#tocx"), log, "tocx"); await pg.wait_for_timeout(450)
        if await pg.evaluate(TV): log.append("toc not closed by tocx")
    # 2 nav dropdown (mobile)
    if await pg.locator("#navbtn").is_visible():
        await safe_click(pg, pg.locator("#navbtn"), log, "navbtn"); await pg.wait_for_timeout(200)
        r=await pg.evaluate("(()=>{const r=document.querySelector('#navdrop').getBoundingClientRect();return [r.left,r.right,innerWidth]})()")
        if r[0]<-1 or r[1]>r[2]+1: log.append(f"navdrop overflow {r}")
        await pg.keyboard.press("Escape")
    # 3 legend + marks + theme
    await safe_click(pg, pg.locator("#legend summary"), log, "legend")
    await safe_click(pg, pg.locator("#markbtn"), log, "markbtn"); nm=await pg.evaluate("document.documentElement.classList.contains('nomark')")
    if not nm: log.append("marks toggle failed")
    await safe_click(pg, pg.locator("#markbtn2"), log, "markbtn2")
    await safe_click(pg, pg.locator("#themebtn"), log, "theme"); await safe_click(pg, pg.locator("#themebtn"), log, "theme2")
    # 4 verse popovers (first 3)
    vs=pg.locator("main .vs"); n=await vs.count(); stats["vs"]=n
    for i in range(min(3,n)):
        if await safe_click(pg, vs.nth(i*max(1,n//3)), log, "vs"):
            await pg.wait_for_timeout(150)
            r=await pg.evaluate("(()=>{const p=document.querySelector('#pop');if(!p)return null;const r=p.getBoundingClientRect();return [r.left,r.right,document.documentElement.clientWidth]})()")
            if not r: log.append("popover missing")
            elif r[0]<0 or r[1]>r[2]+1: log.append(f"popover overflow {r}")
            await pg.keyboard.press("Escape")
    # 5 expand all details, flip all cards
    stats["details"]=await pg.evaluate("(()=>{const d=[...document.querySelectorAll('main details')];d.forEach(x=>x.open=true);return d.length})()")
    fl=pg.locator(".flip"); nf=await fl.count(); stats["flip"]=nf
    for i in range(nf):
        await safe_click(pg, fl.nth(i), log, "flip")
    # 6 timeline filters
    tb=pg.locator(".tlf button"); 
    for i in range(await tb.count()): await safe_click(pg, tb.nth(i), log, "tlf")
    if await tb.count(): await safe_click(pg, tb.nth(0), log, "tlf0")
    # 7 recite modes
    rb=pg.locator(".rmodes button:not(.tts)"); stats["rmodes"]=await rb.count()
    for i in range(await rb.count()): await safe_click(pg, rb.nth(i), log, "rmode")
    for i in range(await rb.count()):
        t=await rb.nth(i).get_attribute("data-m")
        if t=="read" or t=="big": await safe_click(pg, rb.nth(i), log, "rmode-reset")
    # 8 memory page
    for sel in ["#fcshuf","#fcall","#czre",".cz2 .btn","#qzo button","#qznext","#qzre","#plan input"]:
        loc=pg.locator(sel)
        if await loc.count(): await safe_click(pg, loc.first, log, sel)
    # 9 map modules
    mods=pg.locator(".mapmod"); nm=await mods.count(); stats["maps"]=nm; stats["map_ok"]=0
    for i in range(nm):
        m=mods.nth(i)
        hots=m.locator(".mm-concept .hot")
        nh=await hots.count()
        for k in list(range(min(3,nh)))+([nh-1] if nh>3 else []):
            try: await hots.nth(k).click(timeout=2500)
            except Exception:
                # nested zones (e.g. temple courts): the outer zone's centre is covered by the inner one; activate via keyboard instead
                await hots.nth(k).focus(); await pg.keyboard.press("Enter")
        info=await m.locator(".mm-info").text_content()
        if "📍" not in (info or "") and await hots.count(): log.append(f"hot info not updated map{i}")
        lbs=m.locator(".maptools .lb[data-l]")
        if await lbs.count(): await safe_click(pg, lbs.first, log, "lb"); await safe_click(pg, lbs.first, log, "lb2"); await safe_click(pg, m.locator(".maptools .lb.play"), log, "play")
        vb=m.locator(".veilbtn")
        if await vb.count(): await safe_click(pg, vb, log, "veil")
        await m.locator(".mm-canvas").scroll_into_view_if_needed()
        try:
            await pg.wait_for_function("el=>el.querySelector('.leaflet-container')", arg=await m.element_handle(), timeout=8000)
            ok=True
        except Exception: ok=False; log.append(f"leaflet not initialised map{i}")
        if ok:
            try: await pg.wait_for_function("el=>/✅|已改用/.test(el.querySelector('.mm-status').textContent)", arg=await m.element_handle(), timeout=12000); stats["map_ok"]+=1
            except Exception: log.append(f"tiles not ok map{i}: "+(await m.locator('.mm-status').text_content() or ''))
            lb=m.locator(".mm-layers button"); nl=await lb.count(); stats.setdefault("layers",nl)
            if i==0:
                for k in range(nl): await safe_click(pg, lb.nth(k), log, "layer"); await pg.wait_for_timeout(250)
                await safe_click(pg, lb.nth(0), log, "layer0")
            else: await safe_click(pg, lb.nth(1), log, "layer1")
            for a in ["fit","play","drag","drag"]:
                b=m.locator(f'.mm-btn[data-a="{a}"]')
                if await b.count(): await safe_click(pg, b, log, a)
            fb=m.locator('.mm-btn[data-a="full"]')
            await safe_click(pg, fb, log, "full"); await pg.wait_for_timeout(300)
            r=await pg.evaluate("el=>{const r=el.querySelector('.mm-live').getBoundingClientRect();return [r.width,r.height,innerWidth,innerHeight]}", await m.element_handle())
            if abs(r[0]-r[2])>20: log.append(f"fullscreen size {r}")
            await safe_click(pg, fb, log, "full-off")
            # leaflet popups: click a marker
            mk=m.locator(".leaflet-marker-icon, path.leaflet-interactive").first
            try:
                await mk.click(timeout=2000, force=True); await pg.wait_for_timeout(200)
            except Exception: pass
    await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));scrollTo(0,0)")
    await pg.wait_for_timeout(300)
    r=await pg.evaluate(CHECK); r["log"]=log; r["stats"]=stats; r["errs"]=errs[:]; errs.clear()
    return r
async def main():
    so=socket.socket(); so.bind(("127.0.0.1",0)); PORT=so.getsockname()[1]; so.close()
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1","-d",D],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    rep={}; bad=0
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for w in WIDTHS:
            mob=w<700
            for f in PAGES:
              for attempt in range(3):
                try:
                    if not b.is_connected(): b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
                    ctx=await b.new_context(viewport={"width":w,"height":800 if mob else 900},device_scale_factor=1,is_mobile=mob,has_touch=mob); pg=await ctx.new_page(); errs=[]
                    pg.on("pageerror",lambda e,errs=errs:errs.append(str(e)))
                    pg.on("console",lambda m,errs=errs: errs.append("console:"+m.text) if m.type=="error" and "tile" not in m.text.lower() and "Failed to load resource" not in m.text else None)
                    r=await run_page(pg,f"http://127.0.0.1:{PORT}/{f}",f,w,errs); break
                except Exception as ex:
                    print("RETRY",w,f,str(ex)[:120],flush=True)
                    try: await ctx.close()
                    except Exception: pass
                    try: await b.close()
                    except Exception: pass
              else:
                  rep[f"{w}/{f}"]={"fatal":True}; bad+=1; continue
              if True:
                ok = r["sw"]<=r["vw"] and not r["off"] and not r["clip"] and not r["hdr"] and not r["errs"] and not r["log"]
                bad += (not ok); rep[f"{w}/{f}"]=r
                print(("OK " if ok else "BAD"),w,f,"sw",r["sw"],"vw",r["vw"],r["off"][:3],r["clip"][:3],r["hdr"],r["errs"][:2],r["log"][:4],r["stats"],flush=True)
                await pg.screenshot(path=os.path.join(OUT,f"{w}-{f[:-5]}.png"),full_page=False)
                await ctx.close()
        await b.close()
    srv.terminate(); json.dump(rep,open(os.path.join(OUT,"qa.json"),"w"),ensure_ascii=False,indent=1); print("BAD PAGES",bad)
asyncio.run(main())
