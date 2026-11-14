/* 四福音书深读 v2.1.0 · 实时地图：本地 Leaflet 1.9.4 懒加载；17 个实测全球底图 + 健康探测；瓦片失败自动回退；全部失败保留离线讲解图 */
(function(){
"use strict";
var OSM='&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>',ESRI='Tiles &copy; Esri';
/* v2.1.0：17 个底图源均经实测（2026-11-14，耶路撒冷 z6/z9/z12 返回真实瓦片）；已剔除需密钥 / 返回占位图的 CARTO、Stadia、Thunderforest、Wikimedia、Mapy。mz = 原生最大缩放（超出则放大显示，避免“Map data not yet available”占位图） */
var PROV=[
 {id:'esri-street',g:'🛣️',n:'Esri 街道',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',a:ESRI,mz:19},
 {id:'osm',g:'🛣️',n:'OpenStreetMap',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',a:OSM,mz:19},
 {id:'esri-topo',g:'⛰️',n:'Esri 地形',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',a:ESRI,mz:19},
 {id:'esri-natgeo',g:'🧭',n:'Esri 国家地理',u:'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',a:ESRI+', National Geographic',mz:16},
 {id:'otm',g:'⛰️',n:'OpenTopoMap 等高线',u:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',s:'abc',a:OSM+', SRTM | &copy; <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (CC-BY-SA)',mz:17},
 {id:'esri-img',g:'🛰️',n:'Esri 卫星',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',a:'Imagery &copy; Esri, Maxar, Earthstar Geographics',mz:19},
 {id:'dare',g:'🏛️',n:'DARE 罗马帝国古地图',u:'https://dh.gu.se/tiles/imperium/{z}/{x}/{y}.png',a:'&copy; <a href="https://dh.gu.se/dare/" target="_blank" rel="noopener">DARE</a> Johan Åhlfeldt, University of Gothenburg (CC BY)',mz:11},
 {id:'cyclosm',g:'⛰️',n:'CyclOSM 地形道路',u:'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',s:'abc',a:OSM+' | CyclOSM / OSM France',mz:19},
 {id:'esri-phys',g:'🌄',n:'Esri 自然地貌',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',a:ESRI+', US National Park Service',mz:8},
 {id:'esri-shade',g:'🌄',n:'Esri 山体晕渲',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',a:ESRI,mz:13},
 {id:'osm-fr',g:'🛣️',n:'OSM 法国镜像',u:'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',s:'abc',a:OSM+' | OSM France',mz:19},
 {id:'osm-de',g:'🛣️',n:'OSM 德国镜像',u:'https://tile.openstreetmap.de/{z}/{x}/{y}.png',a:OSM+' (openstreetmap.de)',mz:19},
 {id:'osm-hot',g:'🛣️',n:'OSM 人道主义',u:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',s:'abc',a:OSM+' | HOT / OSM France',mz:19},
 {id:'opnv',g:'🚌',n:'ÖPNV 交通',u:'https://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png',a:OSM+' | memomaps.de (CC-BY-SA)',mz:18},
 {id:'esri-gray',g:'🌫️',n:'Esri 浅灰',u:'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',a:ESRI,mz:16},
 {id:'esri-dark',g:'🌙',n:'Esri 夜色',u:'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',a:ESRI,mz:16},
 {id:'gaode',g:'🇨🇳',n:'高德（大陆网络备用·境外仅轮廓）',u:'https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',s:'1234',a:'&copy; 高德地图 AutoNavi',mz:9}
];
/* 底图健康探测：每个来源并行请求 1 张巴勒斯坦 z6 瓦片（≈20KB），6 秒超时；结果在本次会话缓存 30 分钟，供所有地图共用 */
var probeP=null;
function probe(){
  if(probeP)return probeP;
  probeP=new Promise(function(res){
    try{var c=JSON.parse(sessionStorage.getItem('fg-tiles')||'null');if(c&&Date.now()-c.t<18e5)return res(c.h)}catch(e){}
    var h={},left=PROV.length;
    PROV.forEach(function(p){
      var u=p.u.replace('{s}',p.s?p.s.charAt(0):'').replace('{z}','6').replace('{x}','38').replace('{y}','26'),im=new Image(),t0=performance.now(),done=false;
      function fin(ok){if(done)return;done=true;h[p.id]=ok?Math.round(performance.now()-t0):-1;if(--left===0){try{sessionStorage.setItem('fg-tiles',JSON.stringify({t:Date.now(),h:h}))}catch(e){}res(h)}}
      im.onload=function(){fin(im.naturalWidth>=200)};im.onerror=function(){fin(false)};setTimeout(function(){fin(false)},6000);im.decoding='async';im.referrerPolicy='strict-origin-when-cross-origin';im.src=u;
    });
  });
  return probeP;
}
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,touch=matchMedia('(pointer:coarse)').matches;
var lfP=null;
function loadLeaflet(){
  if(lfP)return lfP;
  lfP=new Promise(function(res,rej){
    if(window.L)return res(window.L);
    var c=document.createElement('link');c.rel='stylesheet';c.href='assets/vendor/leaflet.css';document.head.appendChild(c);
    var s=document.createElement('script');s.src='assets/vendor/leaflet.js';s.async=true;s.onload=function(){window.L?res(window.L):rej()};s.onerror=rej;document.head.appendChild(s);
  });
  return lfP;
}
function status(box,t,cls){var s=box.querySelector('.mm-status');if(s){s.textContent=t;s.className='mm-status'+(cls?' '+cls:'')}}
function init(box){
  if(box._init)return;box._init=1;
  var cfg;try{cfg=JSON.parse(box.dataset.map)}catch(e){return}
  var canvas=box.querySelector('.mm-canvas'),ph=box.querySelector('.mm-ph'),bar=box.querySelector('.mm-layers');
  status(box,'正在载入地图引擎（本站本地文件）…');
  loadLeaflet().then(function(L){
    if(ph)ph.remove();
    var map=L.map(canvas,{center:cfg.c,zoom:cfg.z,scrollWheelZoom:false,dragging:!touch,tap:false,preferCanvas:true,zoomSnap:0.5,worldCopyJump:true,attributionControl:true});
    box._map=map;
    /* 滚轮只在点按地图后才缩放，避免劫持页面滚动 */
    map.on('click focus',function(){map.scrollWheelZoom.enable()});canvas.addEventListener('mouseleave',function(){map.scrollWheelZoom.disable()});
    var all=[],bounds=[];
    (cfg.polys||[]).forEach(function(p){var g=L.polygon(p.p,{color:p.c,weight:2,dashArray:'6 4',fillOpacity:.22}).addTo(map);g.bindPopup(pop(p.n,p.i));all.push(g);p.p.forEach(function(x){bounds.push(x)})});
    var lines=(cfg.lines||[]).map(function(l){var g=L.polyline(l.p,{color:l.c,weight:3.5,opacity:.9,dashArray:'8 6'}).addTo(map);g.bindTooltip(l.n,{sticky:true});l.p.forEach(function(x){bounds.push(x)});return {g:g,l:l}});
    (cfg.pts||[]).forEach(function(p){
      var m;
      if(p.k!==undefined){m=L.marker([p.la,p.lo],{icon:L.divIcon({className:'',html:'<span class="mk" style="--c:'+(p.c||'#ffc94a')+'">'+p.k+'</span>',iconSize:[26,26],iconAnchor:[13,13]}),keyboard:true,title:p.n})}
      else m=L.circleMarker([p.la,p.lo],{radius:7,color:'#fff',weight:2,fillColor:p.c||'#ffc94a',fillOpacity:1});
      m.addTo(map).bindPopup(pop(p.n,p.i));
      if(cfg.lab)m.bindTooltip(p.n,{permanent:true,direction:'right',offset:[10,0],className:'lf-lab'});
      bounds.push([p.la,p.lo]);
    });
    function fit(){if(bounds.length>1)map.fitBounds(bounds,{padding:[24,24],maxZoom:cfg.z+2,animate:!reduce})}
    if(cfg.fit!==0)fit();
    /* 底图：按钮 + 自动回退 */
    var order=PROV.slice(),first=order.findIndex(function(p){return p.id===cfg.base});if(first>0)order.unshift(order.splice(first,1)[0]);
    var bad={},cur=null,curP=null,timer=null,btns={};
    order.forEach(function(p){var b=document.createElement('button');b.type='button';b.innerHTML='<i class="hd"></i>';b.appendChild(document.createTextNode(p.g+' '+p.n));b.title='切换底图：'+p.n;b.addEventListener('click',function(){bad[p.id]=0;use(p,true)});bar.appendChild(b);btns[p.id]=b});
    var probed=false;
    function applyHealth(h){
      var okN=0;order.forEach(function(p){var v=h[p.id],b=btns[p.id];b.classList.toggle('h-ok',v>=0);b.classList.toggle('h-bad',v<0);b.title=p.n+(v>=0?'（实测可用 · '+v+' ms）':'（当前网络连不上）');if(v>=0)okN++});
      /* 把实测可用的来源排在前面（保持推荐顺序），连不上的排到最后 */
      order.sort(function(a,b){return (h[a.id]<0)-(h[b.id]<0)});
      order.forEach(function(p){bar.appendChild(btns[p.id])});
      box._health=okN+'/'+order.length;
      return okN;
    }
    function next(reason){
      if(curP){bad[curP.id]=1;btns[curP.id].classList.add('bad')}
      var nx=order.find(function(p){return !bad[p.id]});
      if(!nx){if(cur)map.removeLayer(cur);cur=null;status(box,'⚠️ 所有在线底图暂时都连不上（网络不稳定或被屏蔽）。左侧/上方的离线讲解图照常可用；路线与地点仍叠加在此。','err');return}
      status(box,'⚠️ '+curP.n+' '+reason+'，已自动切换到 '+nx.n,'warn');use(nx,false,true);
    }
    function use(p,manual,auto){
      clearTimeout(timer);if(cur)map.removeLayer(cur);
      Object.keys(btns).forEach(function(k){btns[k].classList.toggle('on',k===p.id)});if(manual)btns[p.id].classList.remove('bad');
      curP=p;var ok=0,err=0;
      var o={maxZoom:19,maxNativeZoom:p.mz,attribution:p.a,detectRetina:false,updateWhenIdle:touch,keepBuffer:2,crossOrigin:false};if(p.s)o.subdomains=p.s;
      cur=L.tileLayer(p.u,o);
      cur.on('tileload',function(){ok++;if(ok===1){clearTimeout(timer);if(!auto||manual)status(box,'✅ 底图：'+p.n+'（可在上方切换 '+PROV.length+' 种来源）');else setTimeout(function(){status(box,'✅ 已改用：'+p.n)},1800)}});
      cur.on('tileerror',function(){err++;if(ok===0&&err>=4&&curP===p)next('连接失败')});
      cur.addTo(map);cur.bringToBack();
      timer=setTimeout(function(){if(ok===0&&curP===p)next('8 秒无响应')},8000);
      if(!auto)status(box,'⏳ 正在载入底图：'+p.n+'…');
    }
    /* 先用推荐源立即开始；探测完成后若当前源不可用则切到最快的可用源 */
    use(order[0]);
    probe().then(function(h){var n=applyHealth(h);probed=true;
      if(h[curP.id]<0){var nx=order.find(function(p){return h[p.id]>=0&&!bad[p.id]});if(nx){bad[curP.id]=1;btns[curP.id].classList.add('bad');status(box,'⚠️ '+curP.n+' 在你的网络下连不上，已自动改用 '+nx.n,'warn');use(nx,false,true)}}
      else if(!n){status(box,'⚠️ 17 个在线底图在当前网络都连不上。离线讲解图照常可用；路线与地点仍叠加在此。','err')}
      var hs=box.querySelector('.mm-health');if(hs)hs.textContent='📡 底图实测：'+n+'/'+order.length+' 可用';
    });
    /* 工具条 */
    box.querySelectorAll('.mm-btn').forEach(function(b){b.addEventListener('click',function(){
      var a=b.dataset.a;
      if(a==='fit')fit();
      if(a==='play')play(b);
      if(a==='drag'){var en=!map.dragging.enabled();en?map.dragging.enable():map.dragging.disable();b.classList.toggle('on',en);b.textContent=en?'✋ 拖动：开':'✋ 拖动'}
      if(a==='full'){var f=box.classList.toggle('full');b.textContent=f?'✕ 退出全屏':'⛶ 全屏';document.documentElement.style.overflow=f?'hidden':'';if(f){map.dragging.enable()}setTimeout(function(){map.invalidateSize();fit()},60)}
    })});
    if(!touch){var db=box.querySelector('[data-a=drag]');if(db){db.classList.add('on');db.textContent='✋ 拖动：开'}}
    if(!lines.length){var pb=box.querySelector('[data-a=play]');if(pb)pb.remove()}
    var mover=null,raf=0;
    function play(b){
      if(raf){cancelAnimationFrame(raf);raf=0}
      if(!mover)mover=L.marker(lines[0].l.p[0],{icon:L.divIcon({className:'',html:'<span class="lf-mover"></span>',iconSize:[16,16],iconAnchor:[8,8]}),interactive:false}).addTo(map);
      var seq=[];lines.forEach(function(x){seq.push(x)});var li=0;
      fit();
      function runLine(){
        if(li>=seq.length){b.textContent='▶ 播放路线';return}
        var P=seq[li].l.p,segs=[],tot=0;for(var i=1;i<P.length;i++){var d=Math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]);segs.push(d);tot+=d}
        status(box,'▶ '+seq[li].l.n);seq[li].g.setStyle({weight:6,opacity:1});
        var dur=reduce?1:Math.max(2200,Math.min(6000,tot*9000)),t0=performance.now();
        function step(t){var k=Math.min(1,(t-t0)/dur),dist=k*tot,j=0;while(j<segs.length-1&&dist>segs[j]){dist-=segs[j];j++}
          var f=segs[j]?dist/segs[j]:1,a=P[j],c=P[j+1]||a;mover.setLatLng([a[0]+(c[0]-a[0])*f,a[1]+(c[1]-a[1])*f]);
          if(k<1)raf=requestAnimationFrame(step);else{seq[li].g.setStyle({weight:3.5,opacity:.9});li++;raf=requestAnimationFrame(function(){runLine()})}}
        raf=requestAnimationFrame(step);
      }
      b.textContent='⟲ 重新播放';runLine();
    }
    /* 尺寸变化（目录开合、旋转屏幕）时重算 */
    if('ResizeObserver' in window){var rt=0;new ResizeObserver(function(){clearTimeout(rt);rt=setTimeout(function(){map.invalidateSize()},120)}).observe(canvas)}
  }).catch(function(){
    status(box,'⚠️ 地图引擎载入失败，已保留离线讲解图。','err');if(ph)ph.innerHTML='🗺️ 实时地图暂不可用<br><small>请使用左侧离线讲解图</small>';
  });
}
function pop(n,i){var d=document.createElement('div');var b=document.createElement('b');b.textContent=n;d.appendChild(b);if(i){var s=document.createElement('span');s.textContent=i;d.appendChild(s)}return d}
var boxes=[].slice.call(document.querySelectorAll('.mm-live'));
if(!boxes.length)return;
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);var t=e.target;probe();(window.requestIdleCallback||function(f){return setTimeout(f,200)})(function(){init(t)},{timeout:1500})}})},{rootMargin:'400px 0px'});
  boxes.forEach(function(b){io.observe(b)});
}else boxes.forEach(init);
document.addEventListener('keydown',function(e){if(e.key==='Escape'){var f=document.querySelector('.mm-live.full');if(f){var b=f.querySelector('[data-a=full]');if(b)b.click()}}});
})();
