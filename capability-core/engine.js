(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;if(root)root.SIIAOSCapabilityCore=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const DIMS=['governance','delivery','operations','observability','security','data','ai_usage','automation','open_source','human_control'];
const RISK=Object.freeze({R0:0,R1:1,R2:2,R3:3,R4:4});
const TERMINAL=new Set(['BLOCKED','REJECTED','RETIRED','HOLD']);
function profile(p={}){return Object.fromEntries(DIMS.map(k=>{const n=Number(p[k]??0);return [k,Number.isFinite(n)?Math.max(0,Math.min(4,Math.trunc(n))):0]}));}
function maturityFit(rec,p={}){const a=profile(p),req=profile(rec?.maturity_min);const gaps=DIMS.filter(k=>a[k]<req[k]).map(k=>({dimension:k,actual:a[k],required:req[k],gap:req[k]-a[k]}));return {meets:gaps.length===0,actual:a,required:req,gaps,total_gap:gaps.reduce((s,x)=>s+x.gap,0)};}
function riskGate(rec,policy={}){const risk=RISK[rec?.risk_class]??4,maxWo=RISK[policy.maxRiskWithoutHuman||'R2'],maxAllowed=RISK[policy.maxAllowedRisk||'R4'];if(risk>maxAllowed)return {allowed:false,human_gate:true,reason:'RISK_EXCEEDS_POLICY'};if(risk>=RISK.R3||risk>maxWo)return {allowed:true,human_gate:true,reason:'HUMAN_GATE_REQUIRED'};return {allowed:true,human_gate:false,reason:'RISK_WITHIN_POLICY'};}
function capIds(rec){return new Set((rec?.capabilities||[]).map(x=>x.capability_id).filter(Boolean));}
function overlap(candidate,admitted=[]){const ids=capIds(candidate),out=[];for(const e of admitted){if(!['ADMITTED','PINNED','OBSERVED'].includes(e.admission_state))continue;for(const cid of capIds(e))if(ids.has(cid))out.push({capability_id:cid,record_id:e.record_id,name:e.name});}return out;}
function localFit(rec,prefs={}){const l=rec?.local_feasibility||{},reasons=[];if(prefs.requireOffline===true&&l.offline_capable!==true)reasons.push('OFFLINE_NOT_PROVEN');if(prefs.avoidExternalApi===true&&l.external_api_dependency===true)reasons.push('EXTERNAL_API_DEPENDENCY');if(typeof prefs.maxSubscriptionCost==='number'&&typeof l.subscription_cost==='number'&&l.subscription_cost>prefs.maxSubscriptionCost)reasons.push('SUBSCRIPTION_COST_EXCEEDS_POLICY');return {meets:reasons.length===0,reasons};}
function assess(rec,ctx={}){const state=rec?.admission_state;if(TERMINAL.has(state))return {record:rec,verdict:state,eligible:false,reasons:['STATE_'+state],maturity:null,risk:null,overlap:[],local:null};const mat=maturityFit(rec,ctx.profile);if(!mat.meets)return {record:rec,verdict:'MATURITY_GAP',eligible:false,reasons:mat.gaps.map(g=>`MATURITY_${g.dimension.toUpperCase()}_${g.actual}_LT_${g.required}`),maturity:mat,risk:null,overlap:[],local:null};const rg=riskGate(rec,ctx.policy);if(!rg.allowed)return {record:rec,verdict:'BLOCKED',eligible:false,reasons:[rg.reason],maturity:mat,risk:rg,overlap:[],local:null};const ov=overlap(rec,ctx.admittedRecords||[]),rel=new Set((rec.capabilities||[]).map(x=>x.relation));if(ov.length&&![...rel].some(x=>['AUGMENT','REPLACE','DUPLICATE'].includes(x)))return {record:rec,verdict:'DUPLICATE',eligible:false,reasons:['CAPABILITY_ALREADY_ADMITTED'],maturity:mat,risk:rg,overlap:ov,local:null};const lf=localFit(rec,ctx.preferences);if(!lf.meets)return {record:rec,verdict:'LOCAL_POLICY_GAP',eligible:false,reasons:lf.reasons,maturity:mat,risk:rg,overlap:ov,local:lf};if(rg.human_gate)return {record:rec,verdict:'HUMAN_GATE',eligible:true,reasons:[rg.reason],maturity:mat,risk:rg,overlap:ov,local:lf};return {record:rec,verdict:'ELIGIBLE',eligible:true,reasons:['FIT'],maturity:mat,risk:rg,overlap:ov,local:lf};}
function score(a){if(!a.eligible)return -1000-(a.maturity?.total_gap||0);let s=100-(RISK[a.record.risk_class]??4)*10;if(a.verdict==='HUMAN_GATE')s-=15;const l=a.record.local_feasibility||{};if(l.offline_capable===true)s+=10;if(l.external_api_dependency===false)s+=8;if(l.subscription_cost===0)s+=4;return s;}
function route(records=[],ctx={}){return records.map(r=>{const a=assess(r,ctx);return {...a,score:score(a)}}).sort((a,b)=>b.score-a.score||String(a.record.name||'').localeCompare(String(b.record.name||'')));}
const ALLOWED_TRANSITIONS=Object.freeze({
DISCOVERED:new Set(['CANDIDATE','REJECTED']),
CANDIDATE:new Set(['SCANNED','BLOCKED','REJECTED']),
SCANNED:new Set(['REVIEWED','BLOCKED','REJECTED']),
REVIEWED:new Set(['EXPERIMENT','BLOCKED','REJECTED']),
EXPERIMENT:new Set(['ADMITTED','BLOCKED','REJECTED']),
ADMITTED:new Set(['PINNED','HOLD','RETIRED']),
PINNED:new Set(['OBSERVED','HOLD','RETIRED']),
OBSERVED:new Set(['HOLD','RETIRED']),
HOLD:new Set(['EXPERIMENT','RETIRED']),
UNKNOWN:new Set(['CANDIDATE','REJECTED'])
});
function evidenceKinds(evidence=[]){return new Set(evidence.map(e=>String(e.kind||'').toLowerCase()));}
function verifiedEvidence(evidence=[],kinds=null){return evidence.some(e=>e.status==='verified'&&(!kinds||kinds.has(String(e.kind||'').toLowerCase())));}
function transition(rec,targetState,request={}){
const current=rec.admission_state||'UNKNOWN',target=String(targetState||'').toUpperCase(),allowed=ALLOWED_TRANSITIONS[current]||new Set(),reasons=[];
if(!allowed.has(target))reasons.push('TRANSITION_NOT_ALLOWED');
const supplied=request.evidence||[],combined=[...(rec.evidence||[]),...supplied],kinds=evidenceKinds(combined),risk=RISK[rec.risk_class]??4;
if(target==='SCANNED')for(const required of ['provenance','license','security'])if(!kinds.has(required))reasons.push('MISSING_'+required.toUpperCase()+'_EVIDENCE');
if(target==='EXPERIMENT'){const exp=request.experiment||rec.experiment||{};if(!exp.hypothesis)reasons.push('MISSING_EXPERIMENT_HYPOTHESIS');if(!exp.success_metrics?.length)reasons.push('MISSING_EXPERIMENT_SUCCESS_METRICS');if(!exp.rollback)reasons.push('MISSING_EXPERIMENT_ROLLBACK');if(risk>=RISK.R3&&request.human_approved!==true)reasons.push('HUMAN_APPROVAL_REQUIRED');}
if(target==='ADMITTED'){if(!verifiedEvidence(combined,new Set(['experiment_result','admission_exception'])))reasons.push('VERIFIED_EXPERIMENT_OR_EXCEPTION_REQUIRED');if(risk>=RISK.R3&&request.human_approved!==true)reasons.push('HUMAN_APPROVAL_REQUIRED');}
if(target==='PINNED'){const provenance={...(rec.provenance||{}),...(request.provenance||{})};if(!provenance.artifact_hash)reasons.push('ARTIFACT_HASH_REQUIRED');if(!(provenance.source_commit||provenance.version))reasons.push('IMMUTABLE_VERSION_REQUIRED');}
if(target==='OBSERVED'){const observed=combined.some(e=>['observed','verified'].includes(e.status)&&e.environment);if(!observed)reasons.push('RUNTIME_EVIDENCE_REQUIRED');}
if(['HOLD','RETIRED','REJECTED','BLOCKED'].includes(target)&&!request.reason)reasons.push('REASON_REQUIRED');
if(reasons.length)return {ok:false,from_state:current,target_state:target,reasons,record:rec};
const updated={...rec,admission_state:target,evidence:combined};
if(request.experiment!==undefined)updated.experiment=request.experiment;
if(request.provenance!==undefined)updated.provenance={...(updated.provenance||{}),...request.provenance};
updated.lifecycle_history=[...(updated.lifecycle_history||[]),{from:current,to:target,timestamp:request.timestamp||null,reason:request.reason||null,human_approved:request.human_approved===true,evidence_ids:supplied.map(e=>e.evidence_id).filter(Boolean)}];
return {ok:true,from_state:current,target_state:target,reasons:[],record:updated};
}
function execute(env){if(env.operation==='assess')return {protocol_version:'0.1',result:assess(env.record,env.context)};if(env.operation==='route')return {protocol_version:'0.1',result:route(env.records||[],env.context)};if(env.operation==='transition')return {protocol_version:'0.1',result:transition(env.record,env.target_state,env.transition||{})};throw new Error('Unsupported operation');}
return {DIMS,RISK,ALLOWED_TRANSITIONS,profile,maturityFit,riskGate,capIds,overlap,localFit,assess,score,route,transition,execute};
});
if(typeof module==='object'&&module.exports&&require.main===module){let input='';process.stdin.setEncoding('utf8');process.stdin.on('data',c=>input+=c);process.stdin.on('end',()=>{try{process.stdout.write(JSON.stringify(module.exports.execute(JSON.parse(input)))+'\n')}catch(e){process.stderr.write(String(e)+'\n');process.exitCode=1}});}
