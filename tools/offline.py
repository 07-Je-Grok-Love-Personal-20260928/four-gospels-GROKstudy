# 断网回退测试：拦截所有外部瓦片请求，确认讲解图仍显示、状态提示正确、无 JS 错误。用法：python3 tools/offline.py
import asyncio, os, sys, subprocess, time
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"docs"); PORT=8957
async def main():
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"-d",D,"--bind","127.0.0.1"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1); bad=0
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch()
            for f in ["maps","history","matthew"]:
                ctx=await b.new_context(viewport={"width":390,"height":844}); pg=await ctx.new_page(); errs=[]
                pg.on("pageerror",lambda e: errs.append(str(e)))
                await ctx.route(lambda u: not u.startswith(f"http://127.0.0.1:{PORT}"), lambda r: r.abort())
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}.html"); m=pg.locator(".mapmod").first
                await m.locator(".mm-canvas").scroll_into_view_if_needed()
                try: await pg.wait_for_function("el=>/连不上/.test(el.querySelector('.mm-status').textContent)",arg=await m.element_handle(),timeout=20000); st="fallback-msg"
                except Exception: st="NO MSG: "+(await m.locator(".mm-status").text_content() or ""); bad+=1
                vis=await m.locator(".mm-concept svg").first.is_visible()
                if not vis: bad+=1
                if errs: bad+=1
                print(f, st, "concept_visible", vis, "errs", errs[:2]); await ctx.close()
            await b.close()
    finally: srv.kill()
    print("OFFLINE BAD", bad)
asyncio.run(main())
