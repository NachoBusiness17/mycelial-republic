// invariant_probe_001.mjs — cross-model steering transfer (GLM-5.3-Flash vs DeepSeek-V4-Flash Tail).
// Comparative anatomy probe: same steering-line -> D-depth-response physics on a different model family.
// Model: glm-5.3-flash via https://api.z.ai/api/anthropic/v1/messages (headers x-api-key / anthropic-version).
// NOTE: thinking always-on -> keep max_tokens SMALL (<=200), runs FEW (<=6 calls). $0-marginal on plan.
// NEVER prints the key. Logs ONE JSON line per call to /board/invariant_probe_001.jsonl.
import { readFileSync, existsSync, appendFileSync } from 'node:fs';
import { performance } from 'node:perf_hooks';

function loadKey(name){
  if (process.env[name]) return process.env[name];
  if (!existsSync('/mag/.env')) return null;
  const line = readFileSync('/mag/.env','utf8').split(/\r?\n/).find(l=>l.startsWith(name+'='));
  return line ? line.slice(name.length+1).replace(/^"|"$/g,'').trim() : null;
}
const KEY = loadKey('ZAI_API_KEY_3');
const BASE='https://api.z.ai/api/anthropic/v1/messages', MODEL='glm-5.3-flash';
if(!KEY){ console.error('NO_KEY'); process.exit(1); }

// ---- DS Tail seat reconstruction (from steer_exp_001 receipts + steers.jsonl + diff_steer_probe.mjs) ----
// Receipt semantics observed on DS-V4-Flash: steering line declares [target: D=N], Tail's per-call work
// verifies N items (items_verified == D) and logs a receipt in the shape {D, items_verified, mismatches}.
// This GLM twin gets the SAME system-prompt shape (terse Tail operational seat) + SAME steering lines.
const SYS = 'You are a terse Tail seat in a fleet. You receive a steering line that sets a depth parameter D. '
 + 'You perform one unit of work at the requested depth and reply with EXACTLY one compact JSON receipt in the form '
 + '{"D":<depth>,"items_verified":<count>,"mismatches":0} where items_verified equals the D you actually applied. '
 + 'Only output that JSON. No explanation, no prose, no markdown.';

// Steering lines (verbatim-ish from /board/steers.jsonl, D values varied per probe).
const cases = [
  { id:'c1', steering:'STEER-001 [task: INDEX verification sweep] [param: depth D] [target: D=2] [rate: adjust every ~10 calls] [ttl: 30min] [scope: verify 26 INDEX items sha256 from disk vs recorded] ACTION: start sweep with D=2 per call.' },
  { id:'c2', steering:'STEER-002 [task: INDEX verification sweep] [target: D=4] [rationale: 10 receipts at D=2 all clean, raise depth to accelerate] [rate: adjust every ~10 calls] [ttl: 30min] [scope: continue remaining INDEX 26-sha256 verification] ACTION: bump to D=4 per call.' },
  { id:'c3', steering:'STEER-003 [task: INDEX verification sweep] [target: D=5] [scope: continue remaining INDEX 26-sha256 verification from disk vs recorded] ACTION: bump to D=5 per call.' },
  { id:'c4', steering:'STEER-004 [task: INDEX verification sweep] [target: D=2] [scope: fresh cold pass on all 26 INDEX items] ACTION: D=2 per call.' },
  { id:'c5', steering:'STEER-005 [task: INDEX verification sweep] [target: D=6] [scope: accelerate to finish] ACTION: D=6 per call.' },
];

async function call(steering){
  const t0=performance.now();
  let resp;
  try {
    resp = await fetch(BASE,{
      method:'POST',
      headers:{'Content-Type':'application/json','x-api-key':KEY,'anthropic-version':'2023-06-01'},
      body: JSON.stringify({ model:MODEL, max_tokens:200, system:SYS, messages:[{role:'user',content:steering}] })
    });
  } catch(e){ return {http:0, ms:Math.round(performance.now()-t0), err:String(e)}; }
  const ms=Math.round(performance.now()-t0);
  let body; try{ body=await resp.json(); }catch{ return {http:resp.status, ms, err:'bad-json'}; }
  // extract final text content + thinking tokens
  let finalText='', thinkText='';
  if(body.content && Array.isArray(body.content)){
    for(const b of body.content){
      if(b.type==='text') finalText += b.text||'';
      if(b.type==='thinking') thinkText += b.text||'';
    }
  }
  return {
    http:resp.status, ms, finalText:finalText.trim(),
    thinkChars:thinkText.length,
    usage: body.usage||null,
    err: body.error? JSON.stringify(body.error):undefined
  };
}

// classify the model's reported D vs the requested D
function parseD(text){
  try{
    const j=JSON.parse(text);
    if(j && typeof j.D==='number') return {D:j.D, items:j.items_verified, ok:true};
    return {ok:false, raw:text.slice(0,60)};
  }catch{ return {ok:false, raw:text.slice(0,60)}; }
}

// Human-read reference (what DS did per the receipts): the requested D was honored -> items_verified==D.
async function run(){
  for(const c of cases){
    const r = await call(c.steering);
    const requestedD = parseInt((c.steering.match(/target: D=(\d+)/)||[])[1],10);
    const pd = parseD(r.finalText||'');
    // transfer: GLM reported D == requested D (same direction & magnitude as DS honors-it behavior)
    let transfer='unclear';
    let observed='';
    if(r.http===200 && !r.err){
      if(pd.ok){
        if(pd.D===requestedD && pd.items===requestedD){ transfer='match'; observed='D='+pd.D+', items_verified='+pd.items; }
        else if(pd.D===requestedD || pd.items===requestedD){ transfer='partial'; observed='D='+pd.D+', items_verified='+pd.items; }
        else { transfer='mismatch'; observed='D='+pd.D+', items_verified='+(pd.items===undefined?'NA':pd.items); }
      } else { transfer='mismatch'; observed='non-json: '+r.finalText.slice(0,50); }
    } else { transfer='unclear'; observed=(r.err||('http='+r.http)); }

    const row={ ts:new Date().toISOString(), model:MODEL, steering_line:c.id,
      requested_D:requestedD, observed_D_response:observed,
      ds_reference_D_response:'D honored -> items_verified='+requestedD+' (receipt shape {D,items_verified,mismatches:0})',
      transfer, note: JSON.stringify({http:r.http, ms:r.ms, thinkChars:r.thinkChars,
        usage:r.usage?{in:r.usage.input_tokens, out:r.usage.output_tokens, thinking:r.usage.thinking_tokens}:null}) };
    appendFileSync('/board/invariant_probe_001.jsonl', JSON.stringify(row)+'\n');
    console.log(c.id, 'reqD='+requestedD, 'transfer='+transfer, 'out='+observed,
      'http='+r.http, 'ms='+r.ms, 'thinkChars='+r.thinkChars);
    if(r.http===529){ await new Promise(s=>setTimeout(s,8000)); }
    else { await new Promise(s=>setTimeout(s,1200)); }
  }
  console.log('DONE');
}
await run();
