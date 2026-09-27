(function(root,factory){
  const api=factory(root);
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root)root.SIIAOSRegistryAdapter=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(root){
'use strict';

let registryState={records:[],byLegacyId:new Map(),source:'uninitialized',error:null};

function slug(value){
  return String(value||'unknown').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'.').replace(/^\.+|\.+$/g,'')||'unknown';
}

function zeroMaturity(){
  const dims=['governance','delivery','operations','observability','security','data','ai_usage','automation','open_source','human_control'];
  return Object.fromEntries(dims.map(k=>[k,0]));
}

function fromLegacySource(source){
  return {
    record_id:'source.'+source.id,
    object_type:'source',
    name:source.name,
    description:source.role||null,
    legacy:{
      source_id:source.id,
      kind:source.kind||null,
      domain:source.domain||null,
      authority:source.authority||null,
      volume:Number.isFinite(source.volume)?source.volume:null,
      owner:source.owner||null,
      depends:source.depends||null,
      local:source.local||null,
      risk_text:source.risk||null
    },
    capabilities:[{capability_id:'discovery.'+slug(source.domain),relation:'EXPERIMENT'}],
    admission_state:'DISCOVERED',
    risk_class:'R0',
    maturity_min:zeroMaturity(),
    upstream_maturity:{stage:'unknown'},
    permissions:{},
    network:{},
    data_scope:{},
    local_feasibility:{
      cpu:null,ram:null,gpu:null,vram:null,disk:null,persistent_service:null,
      external_api_dependency:null,subscription_cost:null,offline_capable:null,degraded_mode:null
    },
    provenance:{
      source:source.url,source_repo:null,source_commit:null,version:null,
      artifact_hash:null,license:null,verified_at:null
    },
    evidence:[],
    migration:{
      source_file:'public-resource-hub/sources.js',
      source_file_sha:null,
      mapping_status:'BROWSER_FALLBACK_UNQUALIFIED',
      note:'Fallback projection only. Missing qualification fields remain unknown/null.'
    }
  };
}

function index(records){
  const byLegacyId=new Map();
  for(const record of records){
    const id=record&&record.legacy&&record.legacy.source_id;
    if(id)byLegacyId.set(id,record);
  }
  registryState.byLegacyId=byLegacyId;
}

async function init(options){
  const opts=options||{};
  const url=opts.url||'./data/registry.bootstrap.json';
  const fallbackSources=opts.sources||(root&&root.SOURCES)||[];
  try{
    if(typeof fetch!=='function')throw new Error('fetch unavailable');
    const response=await fetch(url,{cache:'no-store'});
    if(!response.ok)throw new Error('registry HTTP '+response.status);
    const payload=await response.json();
    if(!payload||!Array.isArray(payload.records))throw new Error('invalid registry payload');
    registryState={records:payload.records,byLegacyId:new Map(),source:url,error:null};
    index(registryState.records);
    return snapshot();
  }catch(error){
    const records=Array.isArray(fallbackSources)?fallbackSources.map(fromLegacySource):[];
    registryState={records,byLegacyId:new Map(),source:'legacy-fallback',error:String(error&&error.message||error)};
    index(records);
    return snapshot();
  }
}

function snapshot(){
  return {
    source:registryState.source,
    error:registryState.error,
    record_count:registryState.records.length
  };
}

function recordForLegacyId(id){
  return registryState.byLegacyId.get(id)||null;
}

function completeness(record){
  if(!record)return {known:0,total:4,ratio:0,missing:['license','upstream_stage','verified_at','local_feasibility']};
  const checks=[
    ['license',record.provenance&&record.provenance.license],
    ['upstream_stage',record.upstream_maturity&&record.upstream_maturity.stage&&record.upstream_maturity.stage!=='unknown'],
    ['verified_at',record.provenance&&record.provenance.verified_at],
    ['local_feasibility',record.local_feasibility&&(
      record.local_feasibility.offline_capable!==null||
      record.local_feasibility.external_api_dependency!==null||
      record.local_feasibility.subscription_cost!==null
    )]
  ];
  const missing=checks.filter(([,v])=>!v).map(([k])=>k);
  const known=checks.length-missing.length;
  return {known,total:checks.length,ratio:known/checks.length,missing};
}

function summary(){
  const states={},risks={};
  let unknownLicense=0,unknownUpstream=0,unverified=0;
  for(const record of registryState.records){
    states[record.admission_state||'UNKNOWN']=(states[record.admission_state||'UNKNOWN']||0)+1;
    risks[record.risk_class||'UNKNOWN']=(risks[record.risk_class||'UNKNOWN']||0)+1;
    if(!(record.provenance&&record.provenance.license))unknownLicense++;
    if(!(record.upstream_maturity&&record.upstream_maturity.stage&&record.upstream_maturity.stage!=='unknown'))unknownUpstream++;
    if(!(record.provenance&&record.provenance.verified_at))unverified++;
  }
  return {
    total:registryState.records.length,
    source:registryState.source,
    error:registryState.error,
    states,risks,unknown_license:unknownLicense,unknown_upstream:unknownUpstream,unverified
  };
}

function assessRecord(record,context){
  if(!record)return {verdict:'UNKNOWN',eligible:false,reasons:['RECORD_NOT_FOUND']};
  if(record.object_type==='source'&&record.admission_state==='DISCOVERED'){
    return {
      record,
      verdict:'DISCOVERY_ONLY',
      eligible:false,
      reasons:['NOT_QUALIFIED_AS_CANDIDATE'],
      completeness:completeness(record)
    };
  }
  const core=root&&root.SIIAOSCapabilityCore;
  if(!core||typeof core.assess!=='function'){
    return {record,verdict:'CORE_UNAVAILABLE',eligible:false,reasons:['CAPABILITY_CORE_UNAVAILABLE']};
  }
  return core.assess(record,context||{});
}

function assessLegacyId(id,context){
  return assessRecord(recordForLegacyId(id),context);
}

return {
  init,snapshot,summary,fromLegacySource,recordForLegacyId,completeness,assessRecord,assessLegacyId
};
});
