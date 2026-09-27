const fs=require('fs');
const path=require('path');
const assert=require('assert');
const core=require('../engine.js');

const cases=JSON.parse(fs.readFileSync(path.join(__dirname,'..','conformance','cases.json'),'utf8'));

for(const c of cases){
  assert.equal(core.assess(c.record,c.context||{}).verdict,c.expected,c.name);
}

const candidate={
  record_id:'new',
  name:'New',
  admission_state:'CANDIDATE',
  risk_class:'R1',
  maturity_min:{},
  capabilities:[{capability_id:'same',relation:'NEW'}],
  local_feasibility:{}
};

const admitted={
  record_id:'existing',
  name:'Existing',
  admission_state:'ADMITTED',
  risk_class:'R0',
  maturity_min:{},
  capabilities:[{capability_id:'same',relation:'NEW'}],
  local_feasibility:{}
};

assert.equal(core.assess(candidate,{admittedRecords:[admitted]}).verdict,'DUPLICATE');
console.log('ok',cases.length+1,'cases');
