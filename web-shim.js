/* Rafiq web shim: provides window.claude.use(...) outside claude.ai
   tts -> browser speechSynthesis, dictation -> Web Speech API, sample -> /api/grade (needs ANTHROPIC_API_KEY on the server) */
(function(){
  if(window.claude&&window.claude.use)return;
  const synth=window.speechSynthesis;
  function arVoice(){if(!synth)return null;const vs=synth.getVoices();return vs.find(v=>/^ar[-_]?(EG|SA)?/i.test(v.lang)&&/female|zira|hoda|salma|google/i.test(v.name))||vs.find(v=>/^ar/i.test(v.lang))||null}
  if(synth)synth.onvoiceschanged=()=>{};
  const tts=synth?{
    speak(text){return new Promise(res=>{try{synth.cancel();const u=new SpeechSynthesisUtterance(text);u.lang="ar-EG";const v=arVoice();if(v)u.voice=v;u.rate=.95;u.pitch=1.15;u.onend=u.onerror=()=>res();synth.speak(u)}catch(e){res()}})},
    stop(){try{synth.cancel()}catch(e){}}
  }:null;
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  function makeDict(){const rec=new SR();rec.lang="ar-EG";rec.continuous=true;rec.interimResults=true;const h={partial:[],final:[],state:[]};let on=false;
    const emit=(k,v)=>h[k].forEach(f=>{try{f(v)}catch(e){}});
    rec.onresult=e=>{let fin="",part="";for(let i=e.resultIndex;i<e.results.length;i++){const r=e.results[i];if(r.isFinal)fin+=r[0].transcript;else part+=r[0].transcript}if(part)emit("partial",{text:part});if(fin)emit("final",{text:fin})};
    rec.onstart=()=>{on=true;emit("state",{state:"listening"})};rec.onend=()=>{on=false;emit("state",{state:"idle"})};
    rec.onerror=e=>{on=false;emit("state",{state:"idle"});if(e.error==="not-allowed")window.__dictDenied=true};
    return{onPartial(f){h.partial.push(f)},onFinal(f){h.final.push(f)},onState(f){h.state.push(f)},
      start(){return new Promise((res,rej)=>{if(window.__dictDenied)return rej({code:"not_granted"});try{rec.start();res()}catch(e){rej(e)}})},
      stop(){return new Promise(res=>{try{rec.stop()}catch(e){}res()})}}}
  const sample=async(prompt,opts)=>{const r=await fetch("/api/grade",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({prompt})});if(!r.ok)throw new Error("grade "+r.status);return r.json()};
  window.claude={use:async name=>{if(name==="tts")return tts;if(name==="dictation")return SR&&location.protocol==="https:"?makeDict():null;if(name==="sample"){try{const r=await fetch("/api/grade",{method:"HEAD"});return r.ok?sample:null}catch(e){return null}}return null}};
})();
