/* 四福音书深读 GROKstudy v2.1.0 · 2026-11-14 — 屏幕外/滚动中暂停装饰动画、CSS 滚动进度条、 无布局抖动的滚动、IntersectionObserver 目录高亮、标记开关、顺滑滚动、讲解图交互、信经朗读 */
(function(){
"use strict";
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var html=document.documentElement,mqWide=matchMedia('(min-width:1101px)'),wide=function(){return mqWide.matches};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
function on(el,ev,fn,o){if(el)el.addEventListener(ev,fn,o)}
/* ---------- TOC ---------- */
var toc=$('#toc');
function tocToggle(force){
  if(wide()){var off=force!==undefined?!force:!html.classList.contains('toc-off');html.classList.toggle('toc-off',off);store('fg-toc',off?'0':'1')}
  else{html.classList.toggle('toc-open',force!==undefined?force:!html.classList.contains('toc-open'))}
}
on($('#tocbtn'),'click',function(){tocToggle()});
on($('#tocx'),'click',function(){tocToggle(false)});
on($('#scrim'),'click',function(){html.classList.remove('toc-open')});
/* 目录跳转：屏幕外区块按估计高度占位，跳转后再校正一次落点 */
function fixLand(t){[260,700].forEach(function(ms){setTimeout(function(){var d=t.getBoundingClientRect().top-70;if(Math.abs(d)>8){if(lenis)lenis.scrollTo(t,{offset:-70,immediate:true});else scrollBy({top:d,behavior:'instant'})}},ms)})}
$$('#toc a').forEach(function(a){on(a,'click',function(e){if(!wide())html.classList.remove('toc-open');var li0=a.closest('li');if(li0&&li0.classList.contains('has')&&li0.classList.contains('shut'))tocSet(li0,true);var t=document.getElementById(a.getAttribute('href').slice(1));if(!t)return;
  if(lenis){e.preventDefault();lenis.scrollTo(t,{offset:-70,onComplete:function(){fixLand(t)}});history.replaceState(null,'',a.getAttribute('href'))}
  else{e.preventDefault();t.scrollIntoView({behavior:'instant',block:'start'});history.replaceState(null,'',a.getAttribute('href'));fixLand(t)}})});
/* 三级目录：折叠 / 展开 */
function tocSet(li,open){li.classList.toggle('shut',!open);var b=li.querySelector(':scope>.tcr>.tg');if(b)b.setAttribute('aria-expanded',open)}
$$('#toc .tg').forEach(function(b){on(b,'click',function(e){e.preventDefault();var li=b.closest('li');tocSet(li,li.classList.contains('shut'))})});
$$('#toc [data-tx]').forEach(function(b){on(b,'click',function(){var m=b.dataset.tx;$$('#toc li.has').forEach(function(li){var l1=li.classList.contains('l1'),l2=li.classList.contains('l2');tocSet(li,m==='all'||(m==='l2'&&l1))})})});
function tocReveal(a){for(var li=a.closest('li');li;li=li.parentElement&&li.parentElement.closest('#toc li')){if(li.classList.contains('has')&&li.classList.contains('shut')&&li.querySelector(':scope>ol').contains(a))tocSet(li,true)}}
on($('#tocq'),'input',function(){var q=this.value.trim().toLowerCase();$$('#toc li').forEach(function(li){var hit=!q||li.textContent.toLowerCase().indexOf(q)>=0;li.classList.toggle('hid',!hit);if(q&&hit&&li.classList.contains('has'))tocSet(li,true)})});
/* 拖动目录边缘调整宽度（鼠标 / 触控笔 / 平板触摸；键盘 ←→；双击复原），宽度存 localStorage */
var rs=$('#tocrs'),TW0=290;
function tocMax(){return wide()?Math.min(720,Math.round(innerWidth*0.6)):Math.round(innerWidth*0.92)}
function setTW(w,save){w=Math.max(220,Math.min(tocMax(),Math.round(w)));html.style.setProperty('--tocw',w+'px');if(save)store('fg-tocw',String(w));return w}
if(rs){
  var dragW=0,dragRaf=0,pid=null;
  on(rs,'pointerdown',function(e){if(e.button>0)return;e.preventDefault();pid=e.pointerId;try{rs.setPointerCapture(pid)}catch(x){}html.classList.add('tocdrag')});
  on(rs,'pointermove',function(e){if(pid===null||e.pointerId!==pid)return;dragW=e.clientX;if(!dragRaf)dragRaf=requestAnimationFrame(function(){dragRaf=0;setTW(dragW)})});
  function endDrag(e){if(pid===null)return;pid=null;html.classList.remove('tocdrag');setTW(parseFloat(getComputedStyle(html).getPropertyValue('--tocw'))||TW0,true);window.dispatchEvent(new Event('resize'))}
  on(rs,'pointerup',endDrag);on(rs,'pointercancel',endDrag);on(rs,'lostpointercapture',endDrag);
  on(rs,'dblclick',function(){html.style.removeProperty('--tocw');store('fg-tocw','');window.dispatchEvent(new Event('resize'))});
  on(rs,'keydown',function(e){var cur=parseFloat(getComputedStyle(html).getPropertyValue('--tocw'))||TW0;if(e.key==='ArrowLeft'){e.preventDefault();setTW(cur-24,true)}if(e.key==='ArrowRight'){e.preventDefault();setTW(cur+24,true)}});
}
/* ---------- nav / theme / marks ---------- */
on($('#navbtn'),'click',function(e){e.stopPropagation();$('#navdrop').classList.toggle('open')});
document.addEventListener('click',function(e){var nd=$('#navdrop');if(nd&&!e.target.closest('#navdrop'))nd.classList.remove('open')});
on($('#themebtn'),'click',function(){var t=html.dataset.theme==='light'?'night':'light';html.dataset.theme=t;store('fg-theme',t)});
var mb=$('#markbtn'),mb2=$('#markbtn2');
function marks(onv){html.classList.toggle('nomark',!onv);store('fg-mark',onv?'1':'0');if(mb){mb.setAttribute('aria-pressed',onv);mb.textContent='🖍️ 标记：'+(onv?'开':'关')}if(mb2)mb2.setAttribute('aria-pressed',onv)}
marks(!html.classList.contains('nomark'));
on(mb,'click',function(){marks(html.classList.contains('nomark'))});on(mb2,'click',function(){marks(html.classList.contains('nomark'))});
var lg=$('#legend');if(lg){if(store('fg-legend')==='1')lg.open=true;on(lg,'toggle',function(){store('fg-legend',lg.open?'1':'0')})}
document.addEventListener('keydown',function(e){
  if(/INPUT|TEXTAREA/.test(e.target.tagName)||e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key==='t'||e.key==='T')tocToggle();
  if(e.key==='m'||e.key==='M')marks(html.classList.contains('nomark'));
  if(e.key==='Escape'){html.classList.remove('toc-open');hidePop();var nd=$('#navdrop');if(nd)nd.classList.remove('open')}
});
/* ---------- 顺滑滚动（仅桌面精细指针；可关闭） ---------- */
var lenis=null,sb=$('#smoothbtn');
var smoothOK=matchMedia('(pointer:fine)').matches&&!reduce;
function setSmooth(v){
  store('fg-smooth',v?'1':'0');if(sb){sb.setAttribute('aria-pressed',v&&smoothOK);sb.textContent='🌊 顺滑滚动：'+(v&&smoothOK?'开':smoothOK?'关':'系统原生')}
  if(v&&smoothOK&&!lenis){
    var s=document.createElement('script');s.src='assets/vendor/lenis.min.js';s.async=true;
    s.onload=function(){try{lenis=new window.Lenis({lerp:0.11,wheelMultiplier:1,smoothWheel:true,autoRaf:true,prevent:function(n){return !!(n.closest&&n.closest('#toc,.tbl,.mm-canvas,.mm-layers,#navdrop,#pop,.fb,.mtree'))}});lenis.on('scroll',queue)}catch(e){lenis=null}};
    document.head.appendChild(s);
  }else if(!v&&lenis){lenis.destroy();lenis=null}
}
on(sb,'click',function(){setSmooth(store('fg-smooth')==='0')});
if(smoothOK)(window.requestIdleCallback||setTimeout)(function(){setSmooth(store('fg-smooth')!=='0')});else setSmooth(false);
/* ---------- 滚动：只读 scrollY，写 transform；无强制同步布局 ---------- */
var prog=$('#prog'),top=$('#totop'),ticking=false,maxS=1,shown=false,bodyH=0,vh=innerHeight;
/* 进度条：支持 CSS scroll-timeline 的浏览器完全交给合成线程，JS 不再写样式 */
var cssProg=!!(window.CSS&&CSS.supports&&CSS.supports('animation-timeline','scroll()'));if(cssProg)html.classList.add('sprog');
function measure(){maxS=Math.max(1,(bodyH||html.scrollHeight)-vh)}
function frame(){var y=window.scrollY;if(!cssProg)prog.style.transform='scaleX('+Math.min(1,y/maxS).toFixed(4)+')';var sh=y>600;if(sh!==shown){shown=sh;top.classList.toggle('show',sh)}ticking=false}
/* 滚动进行中：给 html 加 .scrolling，暂停“行进虚线”等需要重绘的装饰动画，滚动停下 160ms 后恢复 */
var sT=0,sOn=false;function scrolling(){if(!sOn){sOn=true;html.classList.add('scrolling')}clearTimeout(sT);sT=setTimeout(function(){sOn=false;html.classList.remove('scrolling')},160)}
function queue(){scrolling();if(!ticking){ticking=true;requestAnimationFrame(frame)}}
addEventListener('scroll',queue,{passive:true});addEventListener('resize',function(){vh=innerHeight;measure();if(!ticking){ticking=true;requestAnimationFrame(frame)}},{passive:true});
/* 文档高度由 ResizeObserver 提供（不在脚本执行时强制同步布局） */
if('ResizeObserver' in window)new ResizeObserver(function(es){var r=es[0];bodyH=(r.borderBoxSize&&r.borderBoxSize[0]?r.borderBoxSize[0].blockSize:r.contentRect.height)+ (parseFloat(getComputedStyle(document.body).marginTop)||0);measure()}).observe(document.body);
else addEventListener('load',function(){measure();frame()});
requestAnimationFrame(function(){requestAnimationFrame(frame)});
/* 装饰动画只在屏幕内播放（地图行进线、船、波浪、轨道图、热区） */
if('IntersectionObserver' in window){
  var anim=$$('.mapmod,.mm,.orbitf,.twoage,.svgwrap,.pchart,.jbox,.mapbox,.hero,.gwrap,.fwheel,.quick');
  anim.forEach(function(el){el.classList.add('ap')});
  var aio=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('ap',!e.isIntersecting)})},{rootMargin:'80px 0px'});
  anim.forEach(function(el){aio.observe(el)});
}
on(top,'click',function(){if(lenis)lenis.scrollTo(0);else scrollTo({top:0,behavior:reduce?'auto':'smooth'})});
/* scrollspy via IntersectionObserver */
var links=$$('#toc a'),map={},act=null;
links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
if('IntersectionObserver' in window&&links.length){
  var vis={};
  var spy=new IntersectionObserver(function(es){
    es.forEach(function(e){vis[e.target.id]=e.isIntersecting?e.boundingClientRect.top:undefined});
    var best=null,bt=1e9;for(var k in vis){if(vis[k]!==undefined&&vis[k]<bt){bt=vis[k];best=k}}
    if(best&&map[best]&&map[best]!==act){if(act)act.classList.remove('act');act=map[best];act.classList.add('act');tocReveal(act);
      if(wide()&&!html.classList.contains('toc-off')){var tr=toc.getBoundingClientRect(),ar=act.getBoundingClientRect();if(ar.top<tr.top+60||ar.bottom>tr.bottom-20)toc.scrollTo({top:toc.scrollTop+ar.top-tr.top-tr.height/3,behavior:'smooth'})}}
  },{rootMargin:'-64px 0px -55% 0px'});
  Object.keys(map).forEach(function(id){var h=document.getElementById(id);if(h)spy.observe(h)});
}
/* reveal */
if('IntersectionObserver' in window&&!reduce){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
  $$('.reveal').forEach(function(el){io.observe(el)});
}else $$('.reveal').forEach(function(el){el.classList.add('in')});
/* ---------- verse popover ---------- */
var pop=null;
function hidePop(){if(pop){pop.remove();pop=null}}
document.addEventListener('click',function(e){
  var b=e.target.closest('.vs');
  if(!b){if(!e.target.closest('#pop'))hidePop();return}
  e.preventDefault();e.stopPropagation();var same=pop&&pop._src===b;hidePop();if(same)return;
  pop=document.createElement('div');pop.id='pop';pop._src=b;pop.setAttribute('role','dialog');
  pop.textContent=b.dataset.t;var sm=document.createElement('small');sm.textContent='— '+b.textContent+'（和合本）';pop.appendChild(sm);
  document.body.appendChild(pop);
  var r=b.getBoundingClientRect(),pw=pop.offsetWidth,ph=pop.offsetHeight,vw=html.clientWidth,x=Math.min(Math.max(8,r.left+scrollX),scrollX+vw-pw-8),y=r.bottom+scrollY+8;
  if(r.bottom+ph+16>innerHeight&&r.top>ph+16)y=r.top+scrollY-ph-8;
  pop.style.left=x+'px';pop.style.top=y+'px';
});
addEventListener('resize',hidePop);
/* ---------- flip cards ---------- */
document.addEventListener('click',function(e){var f=e.target.closest('.flip');if(f&&!e.target.closest('.vs'))f.classList.toggle('on')});
document.addEventListener('keydown',function(e){var f=e.target.closest&&e.target.closest('.flip');if(f&&(e.key==='Enter'||e.key===' ')){e.preventDefault();f.classList.toggle('on')}});
/* ---------- timeline filter ---------- */
$$('.tlf button').forEach(function(b){on(b,'click',function(){
  $$('.tlf button').forEach(function(x){x.classList.toggle('on',x===b)});var f=b.dataset.f;
  $$('.tli').forEach(function(li){var show=f==='all'||(f==='ep'?li.classList.contains('ep'):li.classList.contains('c-'+f));li.classList.toggle('hid',!show);if(show)li.classList.add('in')});
})});
/* ---------- 讲解图：热点、图层、播放、幔子 ---------- */
$$('.mapmod').forEach(function(m){
  var info=$('.mm-info',m),svg=$('.mm-concept svg',m);
  $$('.mm-concept .hot',m).forEach(function(h){
    function sel(){$$('.hot.sel',m).forEach(function(x){x.classList.remove('sel')});h.classList.add('sel');if(!info)return;info.textContent='';var b=document.createElement('b');b.textContent='📍 '+h.dataset.n+'：';info.appendChild(b);info.appendChild(document.createTextNode(h.dataset.i||''))}
    on(h,'click',sel);on(h,'keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sel()}});
  });
  $$('.maptools .lb[data-l]',m).forEach(function(b){on(b,'click',function(){b.classList.toggle('on');$$('.lyr[data-l="'+b.dataset.l+'"]',m).forEach(function(g){g.classList.toggle('off',!b.classList.contains('on'))})})});
  var pl=$('.maptools .lb.play',m),gm=$('.gmap',m);
  if(pl&&gm)on(pl,'click',function(){gm.classList.remove('playing');void gm.getBoundingClientRect();gm.classList.add('playing')});
  var vb=$('.veilbtn',m),tp=$('.temple',m);
  if(vb&&tp)on(vb,'click',function(){tp.classList.toggle('torn');vb.classList.toggle('on',tp.classList.contains('torn'))});
  if(svg&&reduce&&svg.pauseAnimations)svg.pauseAnimations();
});
$$('.fw-wrap').forEach(function(w){var info=w.nextElementSibling;$$('.hot',w).forEach(function(h){function sel(){$$('.hot.sel',w).forEach(function(x){x.classList.remove('sel')});h.classList.add('sel');if(!info)return;info.textContent='';var b=document.createElement('b');b.textContent='🕎 '+h.dataset.n+'：';info.appendChild(b);info.appendChild(document.createTextNode(h.dataset.i||''))}
  on(h,'click',sel);on(h,'keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sel()}})})});
/* ---------- 信经背诵模式 + 朗读 ---------- */
var synth=window.speechSynthesis,speaking=null;
$$('.recite').forEach(function(r){
  var body=$('.rbody',r);
  $$('.rmodes button',r).forEach(function(b){on(b,'click',function(){
    var m=b.dataset.m;
    if(m==='big'){b.classList.toggle('on');body.classList.toggle('big');return}
    if(m==='tts'){
      if(!synth){b.textContent='🔇 浏览器不支持朗读';return}
      if(speaking===b){synth.cancel();speaking=null;b.classList.remove('on');b.textContent='🔊 朗读';return}
      synth.cancel();$$('.rmodes .tts.on').forEach(function(x){x.classList.remove('on');x.textContent='🔊 朗读'});
      var txt=$$('.rt',body).map(function(x){return x.dataset.o||x.textContent}).join('');
      var u=new SpeechSynthesisUtterance(txt);u.lang='zh-CN';u.rate=0.95;
      var vs=synth.getVoices().filter(function(v){return /zh/i.test(v.lang)});if(vs.length)u.voice=vs[0];
      u.onend=u.onerror=function(){if(speaking===b){speaking=null;b.classList.remove('on');b.textContent='🔊 朗读'}};
      speaking=b;b.classList.add('on');b.textContent='⏹ 停止朗读';synth.speak(u);return}
    $$('.rmodes button:not([data-m=big]):not([data-m=tts])',r).forEach(function(x){x.classList.toggle('on',x===b)});
    body.classList.remove('hint','hide');$$('.rt.show',body).forEach(function(x){x.classList.remove('show')});
    $$('.rt',body).forEach(function(x){if(x.dataset.o){x.textContent=x.dataset.o;delete x.dataset.o}});
    if(m==='hint'){body.classList.add('hint');$$('.rt',body).forEach(function(x){var t=x.textContent;x.dataset.o=t;var k=t.replace(/^\d+\)\s*/,'');var pre=t.slice(0,t.length-k.length);x.textContent='';x.appendChild(document.createTextNode(pre));var s=document.createElement('b');s.className='hint1';s.textContent=k.charAt(0);x.appendChild(s);x.appendChild(document.createTextNode(k.slice(1)))})}
    if(m==='hide')body.classList.add('hide');
  })});
  on(body,'click',function(e){var t=e.target.closest('.rt');if(t&&(body.classList.contains('hint')||body.classList.contains('hide')))t.classList.toggle('show')});
});
addEventListener('pagehide',function(){if(synth)synth.cancel()});
/* ---------- memory page ---------- */
var dEl=$('#qdata');
if(dEl){
  var D=JSON.parse(dEl.textContent);
  var shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a};
  var fc=$('#fcards');
  if(fc){on($('#fcshuf'),'click',function(){var fr=document.createDocumentFragment();shuffle($$('.flip',fc)).forEach(function(c){fr.appendChild(c)});fc.appendChild(fr)});
  on($('#fcall'),'click',function(){$$('.flip.on',fc).forEach(function(c){c.classList.remove('on')})});}
  var cz=$('#cloze');
  function mkCloze(){var fr=document.createDocumentFragment();shuffle(D.cz).slice(0,6).forEach(function(d){
    var t=d.t,cands=d.w.filter(function(w){return t.indexOf(w)>=0});
    var w=cands.length?cands[Math.floor(Math.random()*cands.length)]:t.slice(2,4),i=t.indexOf(w);
    var row=document.createElement('div');row.className='cz2';var p=document.createElement('p');
    p.appendChild(document.createTextNode(t.slice(0,i)));var g=document.createElement('span');g.className='gap';g.textContent=w;p.appendChild(g);p.appendChild(document.createTextNode(t.slice(i+w.length)));
    var s=document.createElement('small');s.textContent='— '+d.r;var b=document.createElement('button');b.className='btn';b.textContent='显示';b.addEventListener('click',function(){row.classList.toggle('rev')});
    row.appendChild(p);row.appendChild(s);row.appendChild(b);fr.appendChild(row);
  });cz.textContent='';cz.appendChild(fr)}
  if(cz){mkCloze();on($('#czre'),'click',mkCloze)}
  var qi=0,sc=0,done=false,ord=[];
  function newQ(){
    if(!ord.length)ord=shuffle(D.q);var k=ord.pop();
    var opts=shuffle(k.o.filter(function(x,i,a){return x!==k.a&&a.indexOf(x)===i})).slice(0,3);opts.push(k.a);done=false;
    $('#qzn').textContent='第 '+(++qi)+' 题 / 题库 '+D.q.length;$('#qzq').textContent=k.q;$('#qzf').textContent='';var o=$('#qzo');o.textContent='';
    shuffle(opts).forEach(function(t){var b=document.createElement('button');b.textContent=t;b.addEventListener('click',function(){if(done)return;done=true;var ok=t===k.a;if(ok)sc++;b.classList.add(ok?'ok':'no');$$('button',o).forEach(function(x){if(x.textContent===k.a)x.classList.add('ok')});$('#qzs').textContent='得分 '+sc+' / '+qi;$('#qzf').textContent=(ok?'✅ 正确！':'❌ 正确答案：'+k.a)+(k.x?'　'+k.x:'')});o.appendChild(b)});
  }
  if($('#quiz')){on($('#qznext'),'click',newQ);on($('#qzre'),'click',function(){qi=0;sc=0;ord=[];$('#qzs').textContent='得分 0';newQ()});newQ();}
  var saved={};try{saved=JSON.parse(store('fg-plan')||'{}')}catch(e){}
  $$('#plan input').forEach(function(c){c.checked=!!saved[c.dataset.d];on(c,'change',function(){saved[c.dataset.d]=c.checked;store('fg-plan',JSON.stringify(saved))})});
}
/* draw svg in twoage */
if('IntersectionObserver' in window)$$('.twoage').forEach(function(f){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){$$('.draw',f).forEach(function(d){d.classList.add('in')});o.disconnect()}})});o.observe(f)});
})();
