document.getElementById("year").textContent = new Date().getFullYear();

function validateInput(type,value){

  if(!value || value.trim()==="") return "Enter a target first";

  if(type==="email" && !/^\S+@\S+\.\S+$/.test(value))
    return "Enter a valid email";

  if(type==="domain" && !/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value))
    return "Enter a valid domain";

  if(type==="ip" && !/^(\d{1,3}\.){3}\d{1,3}$/.test(value))
    return "Enter a valid IP address";

  return null;
}

async function scan(){

  const btn=document.getElementById("scanBtn");
  const resultsDiv=document.getElementById("results");

  const value=document.getElementById("targetInput").value.trim();
  const type=document.getElementById("typeSelect").value;

  const error=validateInput(type,value);

  if(error){
    resultsDiv.innerHTML=`<div class="resultCard bad">${error}</div>`;
    return;
  }

  btn.disabled=true;
  btn.innerText="Scanning...";

  resultsDiv.innerHTML=
  `<div class="resultCard neutral">Running OSINT modules...</div>`;

  try{

    const res=await fetch("https://api.fluxosint.flux3tor.xyz/targets/",{
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body:JSON.stringify({type,value})
    });

    const data=await res.json();

    window.lastTargetId=data.target_id;

    renderResults(data);
    loadHistory();

  }catch(e){

    resultsDiv.innerHTML=
    `<div class="resultCard bad">Server error</div>`;

  }

  btn.disabled=false;
  btn.innerText="Run Scan";
}

function row(label,value,status="neutral"){
  return `<div class="row">
  <span>${label}</span>
  <span class="${status}">${value ?? "Unknown"}</span>
  </div>`;
}

function renderResults(data){

  const resultsDiv=document.getElementById("results");
  resultsDiv.innerHTML="";

  const overall=data.overall_risk;

  const riskCard=document.createElement("div");
  riskCard.className="resultCard";

  let label="Low";
  let cls="good";

  if(overall>60){
    label="High";
    cls="bad";
  }
  else if(overall>25){
    label="Medium";
    cls="neutral";
  }

  riskCard.innerHTML=`
  <div class="resultTitle">Overall Risk</div>
  <div class="${cls}">${overall} (${label})</div>
  `;

  resultsDiv.appendChild(riskCard);

  const modules=data.results;

  modules.forEach(mod=>{

    const card=document.createElement("div");
    card.className="resultCard";

    let html=`<div class="resultTitle">${mod.module}</div>`;
    const d=mod.result.data||{};

    Object.entries(d).forEach(([k,v])=>{
      html+=row(k,v);
    });

    card.innerHTML=html;
    resultsDiv.appendChild(card);

  });

}

async function loadHistory(){

  if(!window.lastTargetId) return;

  const res=await fetch(
  `https://api.fluxosint.flux3tor.xyz/targets/${window.lastTargetId}/scans`
  );

  const scans=await res.json();

  const history=document.getElementById("history");

  history.innerHTML="";

  scans.slice(1).forEach(s=>{

    const card=document.createElement("div");
    card.className="resultCard";

    card.innerHTML=`
    <div class="resultTitle">Previous Scan</div>
    <div>Risk: ${s.risk}</div>
    <div>${s.created_at}</div>
    `;

    history.appendChild(card);

  });

}