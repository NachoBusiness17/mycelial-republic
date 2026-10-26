// diff_steer_probe.mjs — agenda#2 model-differential steering, $0 free-lane (cerebras gpt-oss-120b Tail).
// Isolates the differential variable: steering hint PRECISION (strong-Brain vs weak-Brain) -> hints-to-converge
// on a fixed falsifiable Tail predicate. Never prints keys. Appends rows to /board/diff_steer_receipts.jsonl.
import { readFileSync, existsSync, appendFileSync } from 'node:fs';
import { performance } from 'node:perf_hooks';

function loadKey(name){
  if (process.env[name]) return process.env[name];
  if (!existsSync('/mag/.env')) return null;
  const line = readFileSync('/mag/.env','utf8').split(/\r?\n/).find(l=>l.startsWith(name+'='));
  return line ? line.slice(name.length+1).replace(/^"|"$/g,'').trim() : null;
}
const KEY = loadKey('CEREBRAS_API_KEY')||loadKey('CEREBRA_API_KEY');
const BASE='https://api.cerebras.ai/v1/chat/completions', MODEL='gpt-oss-120b';
if(!KEY){console.error('NO_KEY');process.exit(1);}

const PRED = (o)=>{ try{ const j=JSON.parse(o); return j&&j.ok===true; }catch{ return false; } }; // bytes: {"ok":true}
const SYS='You are a terse probe. Obey the latest user instruction exactly. Do not explain.';
const n = (a,kt)=>JSON.stringify({model:MODEL,messages:[{role:'system',content:SYS},{role:'user',content:a}],max_tokens:kt,temperature:0});

async function hint(inst,kt=200){
  const t0=performance.now();
  const r=await fetch(BASE,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+KEY},body:n(inst,kt)});
  const ms=Math.round(performance.now()-t0); const j=await r.json();
  const c=j.choices&&j.choices[0];
  return {http:r.status, ms, content:((c&&c.message&&c.message.content)||'').trim(), finish:c&&c.finish_reason,
          promptTok:(j.usage&&j.usage.prompt_tokens)??null, outTok:(j.usage&&j.usage.completion_tokens)??null};
}

// ARM A — strong-Brain ladder: precise corrective hints, converge fast.
const ARM_A = [
  'Reply with EXACTLY this JSON and nothing else: {"ok":true}',
  'Remove all other text. Output ONLY the raw JSON: {"ok":true}',
  'Your output must be parseable JSON with ok exactly true. Output: {"ok":true}',
];
// ARM B — weak-Brain ladder: vague hints, slow/drifts.
const ARM_B = [
  'reply ok true',
  'make it a real json object',
  'output a json where a field ok has value true',
  'exactly {"ok":true} and nothing else',
];

const rows=[];
async function run(label, ladder){
  let content='';
  for(let i=0;i<ladder.length;i++){
    const r=await hint(ladder[i]);
    content=r.content;
    const row={ts:new Date().toISOString(),model:MODEL,arm:label,step:i+1,http:r.http,ms:r.ms,
      obey:r.http===200?PRED(content):false,out:content.slice(0,80),
      promptTok:r.promptTok,outTok:r.outTok,finish:r.finish};
    rows.push(row); appendFileSync('/board/diff_steer_receipts.jsonl',JSON.stringify(row)+'\n');
    console.log(label,'step',i+1,JSON.stringify(row));
    if(row.obey) break; // converged
    await new Promise(s=>setTimeout(s,900));
  }
  return rows.filter(x=>x.arm===label);
}

await run('A_strong', ARM_A);
await new Promise(s=>setTimeout(s,1200));
await run('B_weak', ARM_B);

// summary: hints-to-converge per arm
const sum=(lbl)=>{const s=rows.filter(x=>x.arm===lbl);const conv=s.findIndex(x=>x.obey);return {arm:lbl,steps:s.length,convergedAt:conv===-1?null:conv+1};};
console.log('SUMMARY',JSON.stringify({A:sum('A_strong'),B:sum('B_weak')}));
