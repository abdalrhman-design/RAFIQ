/* ---------- POI labels: name appears when the player is near; tap/click opens a definition card ---------- */
const POI={list:[],els:[],open:null,R:5.5,_v:new THREE.Vector3()};
function poiSet(list){POI.list=list||[];for(const el of POI.els)el.classList.add('hidden')}
function poiLayer(){let L=$('poiLayer');if(!L){L=document.createElement('div');L.id='poiLayer';document.body.appendChild(L);
    const card=document.createElement('div');card.id='poiCard';card.className='hidden';card.innerHTML='<button id="poiClose" aria-label="إغلاق">✕</button><div class="pic" id="poiIcon"></div><h3 id="poiTitle"></h3><p id="poiDesc"></p><button class="btn" id="poiOk">فهمت</button>';document.body.appendChild(card);
    const close=()=>{card.classList.add('hidden');POI.open=null;if(typeof hush==="function")hush()};$('poiClose').onclick=$('poiOk').onclick=close;card.addEventListener('click',e=>{if(e.target===card)close()})}
  return L}
function poiOpen(p){const card=$('poiCard');POI.open=p;$('poiIcon').textContent=p.icon||"📌";$('poiTitle').textContent=p.name;$('poiDesc').innerHTML=typeof p.desc==="function"?p.desc():(p.desc||"");card.classList.remove('hidden');
  if(typeof speak==="function"&&G.sound){const t=$('poiDesc').textContent;speak(p.name+". "+t)}}
function poiFrame(){const L=poiLayer(),show=G.state==="play"&&!POI.open;let k=0;const W=innerWidth,H=innerHeight;
  if(show){const cands=[];for(const p of POI.list){if(p.when&&!p.when())continue;let x,y,z;if(p.obj){p.obj.getWorldPosition(POI._v);x=POI._v.x;y=POI._v.y;z=POI._v.z}else{x=p.x;z=p.z;y=p.y!==undefined?p.y:(typeof p.yf==="function"?p.yf():0)}
      const d=Math.hypot(P.x-x,P.z-z),R=p.r||POI.R;if(d>R)continue;cands.push({p,x,y:y+(p.h!==undefined?p.h:2.1),z,d})}
    cands.sort((a,b)=>a.d-b.d);
    for(const c of cands.slice(0,6)){POI._v.set(c.x,c.y,c.z).project(camera);if(POI._v.z>1)continue;const sx=(POI._v.x+1)/2*W,sy=(1-POI._v.y)/2*H;if(sx<-80||sx>W+80||sy<-40||sy>H+40)continue;
      let el=POI.els[k];if(!el){el=document.createElement('button');el.className='poi';L.appendChild(el);POI.els[k]=el}k++;
      el.classList.remove('hidden');el.textContent=(c.p.icon?c.p.icon+" ":"")+c.p.name;el.style.transform=`translate(-50%,-100%) translate(${sx.toFixed(1)}px,${sy.toFixed(1)}px) scale(${(.75+.35*(1-c.d/(c.p.r||POI.R))).toFixed(3)})`;
      el.style.opacity=Math.min(1,((c.p.r||POI.R)-c.d)/1.2).toFixed(2);el.onclick=()=>poiOpen(c.p)}}
  for(let i=k;i<POI.els.length;i++)POI.els[i].classList.add('hidden')}
const poiStrip=s=>String(s).replace(/<[^>]+>/g,"");
