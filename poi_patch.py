import pathlib,re
POI_JS=pathlib.Path('/home/claude/rafiq-hub/poi.js').read_text()
POI_CSS=pathlib.Path('/home/claude/rafiq-hub/poi.css').read_text()

HIST_DATA=r'''
/* ---- POI data: history ---- */
const HYK_POI={
 hyk_warrior:{icon:"🛡️",name:"محارب من الهكسوس",h:2.3,desc:"الهكسوس قبائل جاءت من آسيا واستولت على منف. حارب جنودهم بأسلحة لم يعرفها المصريون من قبل: الخيول والعجلات الحربية والقوس المركّب، فتغلّبوا على جيش مصر في البداية."},
 hyk_chariot:{icon:"🐎",name:"عجلة حربية",h:2.4,r:7,desc:"عربة خفيفة تجرّها الخيول دخلت مصر مع الهكسوس. تعلّم المصريون صناعتها واستخدامها، فصارت بعد ذلك سلاحًا مهمًّا في جيش الدولة الحديثة."},
 hyk_farmer:{icon:"🌾",name:"فلاح مصري",h:2.2,desc:"يزرع القمح على ضفاف النيل، لكنه يحمل جزءًا من محصوله إلى جابي الضرائب؛ فقد فرض الهكسوس الضرائب على المصريين."},
 hyk_official:{icon:"📜",name:"جابي الضرائب",h:2.3,desc:"موظف يجمع الضرائب من الفلاحين باسم حكام الهكسوس ويسجّلها. كان المصريون يدفعونها من محصولهم رغمًا عنهم."},
};
const HYK_STATIC=[
 {x:300,z:-31,h:7,r:10,icon:"🏰",name:"قلعة أواريس",desc:"أواريس مدينة في شرق الدلتا اتخذها الهكسوس عاصمة لهم وحصّنوها بأسوار ضخمة. حكموا منها الوجه البحري، بينما بقي الوجه القبلي في يد حكام طيبة."},
 {x:310,z:-24.5,h:3.4,r:6,icon:"⛺",name:"معسكر الهكسوس",desc:"خيام المحاربين حول النار، حيث يستريحون ويعدّون خيولهم وعجلاتهم الحربية للقتال."},
 {x:291.5,z:-19.5,h:4,r:6,icon:"🏛️",name:"معبد مهدّم",desc:"دمّر الهكسوس المعابد المصرية ولم يحترموا معتقدات المصريين، وكان هذا من أسباب غضب المصريين عليهم وثورتهم بعد ذلك."},
 {x:292.4,z:-12.6,h:2.8,r:5,icon:"⚖️",name:"محطة الضرائب",desc:"هنا يضع الفلاحون أكياس القمح ليسجّلها جابي الضرائب. فرض الهكسوس الضرائب على المصريين وأخذوا جزءًا من محاصيلهم."},
 {x:294.8,z:-7.4,h:2.4,r:5,icon:"🗿",name:"تمثال ملك ساقط",desc:"تمثال لملك مصري سقط عن قاعدته. بعد الملك أمنمحات الثالث ضعف ملوك الدولة الوسطى وتنازع حكام الأقاليم على الحكم، فطمع الهكسوس في مصر."},
];
function poiRefresh(){POI.world=G.world;POI.key=G.world+':'+exhibits.length+':'+HYK.ents.length;
  if(G.world==="hyk"){const L=HYK_STATIC.slice();for(const e of HYK.ents){const k=e.o&&e.o.userData.kind,d=HYK_POI[k];if(d)L.push(Object.assign({obj:e.o},d))}poiSet(L)}
  else{poiSet(exhibits.map(ex=>{const E=ex.E,st=E.type==="statue";return{x:ex.pos.x,z:ex.pos.z,y:0,h:st?2.6:3.1,r:5.5,icon:st?"🗿":"🖼️",name:E.title,
    desc:()=>G.mode==="study"?E.info.map(poiStrip).join(" "):(st?"تمثال":"لوحة")+" في قاعة «"+HALLS[E.hall].name.split(" · ")[0]+"». اقترب واضغط E ليسألك رفيق عنها، وستعرف قصتها."}}))}}
'''
GEO_DATA=r'''
/* ---- POI data: geography ---- */
const GEO_POI={
 desert:[
  {x:12,z:-15,h:3,r:8,icon:"🌴",name:"الواحة",desc:"مكان في الصحراء تظهر فيه المياه الجوفية على السطح، فينمو حوله النخيل ويعيش الناس والحيوانات."},
  {x:-14,z:-12,h:3,r:6,icon:"🏕️",name:"خيمة البدو",desc:"البدو يسكنون خيامًا خفيفة يحملونها معهم، ويرحلون وراء الماء والعشب لرعي إبلهم وأغنامهم."},
  {x:-11.6,z:-9.8,h:2.4,r:5,icon:"🌡️",name:"مقياس الحرارة",desc:"في الصحراء ترتفع الحرارة كثيرًا نهارًا وتنخفض ليلًا، لأن السماء صافية بلا سحب تحبس الدفء."},
  {x:8.6,z:-6.6,h:2.7,r:5,icon:"🐪",name:"الجمل",desc:"سفينة الصحراء: يخزّن الدهن في سنامه، ويتحمّل العطش أيامًا، وأقدامه العريضة تمنعه من الغوص في الرمل."},
  {x:17.2,z:-8.2,h:2.7,r:5,icon:"🐪",name:"الجمل",desc:"سفينة الصحراء: يخزّن الدهن في سنامه، ويتحمّل العطش أيامًا، وأقدامه العريضة تمنعه من الغوص في الرمل."},
  {x:-9,z:13,h:2.6,r:6,icon:"🏜️",name:"كثيب رملي",desc:"تلّ من الرمال تكوّنه الرياح عندما تحمل حبّات الرمل وتتركها. الكثبان تتحرّك ببطء مع الريح."}],
 forest:[
  {x:4.2,z:-16,h:2.2,r:9,icon:"🏞️",name:"نهر الأمازون",desc:"أكبر أنهار العالم من حيث كمية الماء. تغذّيه الأمطار الغزيرة التي تهطل على الغابة طوال السنة."},
  {x:6.4,z:-17.5,h:1.6,r:5,icon:"🛶",name:"قارب خشبي",desc:"سكان الغابة يتنقّلون بالقوارب لأن الأنهار هي طرقهم وسط الأشجار الكثيفة."},
  {x:-9,z:-5,h:7,r:7,icon:"🌳",name:"شجرة عملاقة",desc:"أشجار الغابة الاستوائية دائمة الخضرة ومتفاوتة الارتفاع، وأوراقها الكثيفة تحجب الشمس عن الأرض."},
  {x:-3.4,z:14.6,h:2.4,r:5,icon:"🌧️",name:"مقياس المطر",desc:"يقيس كمية المطر الساقط. في الغابة الاستوائية يمطر معظم أيام السنة لقربها من خط الاستواء."},
  {x:-6.6,z:15.6,h:2.8,r:5,icon:"🌿",name:"نبات استوائي",desc:"أوراق عريضة كبيرة تلتقط أكبر قدر من الضوء القليل الذي يصل إلى أرض الغابة."}],
 polar:[
  {x:-8.6,z:11.4,h:2.6,r:6,icon:"📍",name:"علامة القطب الجنوبي",desc:"هنا أقصى جنوب الأرض. القطب الجنوبي يقع في قارة أنتاركتيكا، وهي يابسة مغطّاة بطبقة جليد سميكة."},
  {x:-13.5,z:15,h:3,r:6,icon:"⛺",name:"خيمة البعثة",desc:"العلماء يعيشون في محطات وخيام مجهّزة ليدرسوا الجليد والطقس، فلا يسكن أحد القارة بشكل دائم."},
  {x:11.8,z:.8,h:2.4,r:5,icon:"🔭",name:"تلسكوب الشمس",desc:"في الصيف القطبي تدور الشمس قرب الأفق ولا تغيب لشهور، وفي الشتاء يسود الليل شهورًا."},
  {x:-.5,z:-14.5,h:2,r:7,icon:"🐧",name:"البطاريق",desc:"طيور لا تطير لكنها سبّاحة ماهرة. تعيش في نصف الكرة الجنوبي، وتحميها طبقة دهن سميكة وريش كثيف."},
  {x:9.5,z:-14.5,h:1.8,r:5,icon:"🦭",name:"الفقمة",desc:"تصطاد السمك تحت الجليد وتتنفّس من فتحات فيه. طبقة الدهن تحتها تحفظ حرارتها."}],
 mount:[
  {x:-2.6,z:20,h:2.4,r:5,icon:"🌡️",name:"مقياس الحرارة",desc:"كلما ارتفعنا انخفضت الحرارة نحو ست درجات ونصف لكل ألف متر؛ لذلك القمم باردة رغم سطوع الشمس."},
  {x:-.6,z:-3,h:2,r:6,icon:"💧",name:"جدول جبلي",desc:"ماء بارد يأتي من ذوبان الثلج في القمم. هكذا تبدأ الأنهار الكبيرة من الجبال."},
  {x:-5,z:-27,h:3,r:7,icon:"❄️",name:"خط الثلج الدائم",desc:"فوق ارتفاع معيّن يبقى الثلج طوال السنة ولا يذوب. تحته تنمو النباتات وفوقه صخور وثلج فقط."},
  {x:-5.5,z:-30,h:3.6,r:6,icon:"🎏",name:"أعلام الصلاة",desc:"أعلام ملوّنة يعلّقها سكان الهيمالايا في الممرات العالية، وتهتزّ بالرياح القوية في الأعالي."},
  {xf:()=>pxM(-9)-7.4,z:-9,h:2.2,r:6,icon:"🐐",name:"الماعز الجبلي",desc:"يتسلّق الصخور شديدة الانحدار بحوافر قوية، ويعيش على النباتات القليلة في المرتفعات."}],
};
function poiRefresh(){POI.world=G.world;const W=CUR;if(!W||!GEO_POI[W.id]){poiSet([]);return}
  const L=GEO_POI[W.id].map(p=>{const q=Object.assign({},p);if(q.xf){q.x=q.xf()}q.yf=()=>W.h(q.x,q.z);return q});
  L.push({x:W.pod.x,z:W.pod.z,yf:()=>W.h(W.pod.x,W.pod.z),h:3.2,r:6,icon:"🚀",name:"مركبتنا",desc:"بها نعود إلى الفضاء لنختار عالمًا آخر. رفيق يسألك عن هذا العالم قبل الإقلاع."});
  poiSet(L)}
'''

def patch(path,data,frame_anchor,world_check):
    p=pathlib.Path(path);s=p.read_text()
    if 'poiFrame' in s: print(path,'already patched');return
    s=s.replace('</style>',POI_CSS+'</style>',1)
    # inject module + data before window.__G
    i=s.rfind('window.__G=')
    s=s[:i]+POI_JS+data+'\n'+s[i:]
    # frame hook: before final render in main frame
    assert frame_anchor in s
    s=s.replace(frame_anchor,f'if({"POI.key" if "exhibits" in world_check else "POI.world"}!=={world_check})poiRefresh();poiFrame();\n  {frame_anchor}',1)
    p.write_text(s);print(path,'patched')

# history: hykSpawn kind tag
h=pathlib.Path('/home/claude/rafiq-history/index.html');s=h.read_text()
if 'userData.kind=asset.name' not in s:
    s=s.replace('function hykSpawn(asset,clipRe){const o=THREE.SkeletonUtils.clone(asset.scene);','function hykSpawn(asset,clipRe){const o=THREE.SkeletonUtils.clone(asset.scene);o.userData.kind=asset.name;',1)
    assert 'userData.kind=asset.name' in s
    h.write_text(s)
patch('/home/claude/rafiq-history/index.html',HIST_DATA,'  renderer.render(scene,camera)}',"G.world+':'+exhibits.length+':'+HYK.ents.length")
patch('/home/claude/geo/index.html',GEO_DATA,'  renderer.render(scene,camera)}','(CUR&&CUR.id)')
