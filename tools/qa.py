# Playwright QA: horizontal overflow + clipped content + header overlap + screenshots at 375/768/1440
import asyncio, json, os, sys, subprocess, time
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"docs"); OUT=os.path.join(ROOT,"build","qa"); os.makedirs(OUT,exist_ok=True)
PAGES=[f for f in sorted(os.listdir(D)) if f.endswith(".html")]
JS=r"""()=>{const de=document.documentElement,vw=de.clientWidth,res={sw:de.scrollWidth,vw:vw,off:[],clip:[],hdr:[]};
const scrollers=n=>{for(let p=n.parentElement;p;p=p.parentElement){const s=getComputedStyle(p);if(/(auto|scroll|hidden)/.test(s.overflowX)&&p!==document.body&&p!==de)return true;if(p.id==='toc'||p.id==='navdrop')return true}return false};
document.querySelectorAll('main *').forEach(n=>{const r=n.getBoundingClientRect();if(!r.width||getComputedStyle(n).position==='fixed')return;
 if((r.right>vw+1||r.left<-1)&&!scrollers(n))res.off.push((n.className||n.tagName)+' '+Math.round(r.left)+'→'+Math.round(r.right));
 const s=getComputedStyle(n);if(['P','LI','TD','B','SPAN','A','H2','H3','H4','SMALL'].includes(n.tagName)&&s.overflowX==='visible'&&n.scrollWidth>n.clientWidth+2&&n.clientWidth>0&&s.display!=='inline'&&!scrollers(n))res.clip.push(n.tagName+'.'+n.className+':'+n.textContent.slice(0,20))});
const hs=[...document.querySelectorAll('.top > *')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.getBoundingClientRect());
for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.right>b.left+1&&b.right>a.left+1&&a.bottom>b.top&&b.bottom>a.top)res.hdr.push(i+'x'+j)}
res.off=res.off.slice(0,8);res.clip=res.clip.slice(0,8);return res}"""
async def main():
    import socket; so=socket.socket(); so.bind(("127.0.0.1",0)); PORT=so.getsockname()[1]; so.close()
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1","-d",D],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    rep={}; bad=0
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in ((375,812),(768,1024),(1440,900)):
            ctx=await b.new_context(viewport={"width":w,"height":h},device_scale_factor=1); pg=await ctx.new_page(); errs=[]
            pg.on("pageerror",lambda e:errs.append(str(e)))
            for f in PAGES:
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}",wait_until="networkidle")
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))"); await pg.wait_for_timeout(250)
                assert "四福音书" in await pg.title(), f; r=await pg.evaluate(JS); r["errs"]=errs[:]; errs.clear()
                ok = r["sw"]<=r["vw"] and not r["off"] and not r["clip"] and not r["hdr"] and not r["errs"]
                bad += (not ok); rep[f"{w}/{f}"]=r
                print(("OK " if ok else "BAD"),w,f,"sw",r["sw"],"vw",r["vw"],r["off"][:3],r["clip"][:3],r["hdr"],r["errs"][:2])
                await pg.screenshot(path=os.path.join(OUT,f"{w}-{f[:-5]}.png"),full_page=False)
            await ctx.close()
        await b.close()
    srv.terminate(); json.dump(rep,open(os.path.join(OUT,"qa.json"),"w"),ensure_ascii=False,indent=1); print("BAD PAGES",bad)
asyncio.run(main())
