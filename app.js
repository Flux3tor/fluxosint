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
  const btn = document.getElementById("scanBtn");
  const resultsDiv = document.getElementById("results");

  const value = document.getElementById("targetInput").value.trim();
  const type = document.getElementById("typeSelect").value;

  const error = validateInput(type,value);
  if(error){
    resultsDiv.innerHTML = `<div class="resultCard bad">${error}</div>`;
    return;
  }

  btn.disabled = true;
  btn.innerText = "Scanning...";
  resultsDiv.innerHTML = `<div class="resultCard neutral">Running OSINT modules...</div>`;

  try{
    const res = await fetch("https://api.fluxosint.flux3tor.xyz/targets/",{
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body:JSON.stringify({type,value})
    });

    const data = await res.json();
    renderResults(data);

  }catch(e){
    resultsDiv.innerHTML = `<div class="resultCard bad">Server error</div>`;
  }

  btn.disabled = false;
  btn.innerText = "Run Scan";
}

function row(label,value,status="neutral"){
  return `<div class="row">
    <span>${label}</span>
    <span class="${status}">${value ?? "Unknown"}</span>
  </div>`;
}

function renderResults(data){
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML="";

  const overall = data.overall_risk || 0;

  const riskCard = document.createElement("div");
  riskCard.className="resultCard";

  let label="Low";
  let cls="good";

  if(overall > 60){
    label="High";
    cls="bad";
  }else if(overall > 25){
    label="Medium";
    cls="neutral";
  }

  riskCard.innerHTML = `
    <div class="resultTitle">Overall Risk</div>
    <div class="${cls}">${overall} (${label})</div>
  `;

  resultsDiv.appendChild(riskCard);

  const modules = data.results;

  modules.forEach(mod=>{
    const card = document.createElement("div");
    card.className="resultCard";

    let html = `<div class="resultTitle">${mod.module}</div>`;
    const d = mod.result.data || {};

    if(mod.module === "Email Intel"){

      if(Array.isArray(d.mx_records)){
        d.mx_records.forEach(mx=>{
          html += row("MX", mx);
        });
      }

      html += row("Disposable", d.disposable ? "Yes":"No", d.disposable?"bad":"good");
      html += row("Gravatar", d.gravatar_found ? "Found":"None", d.gravatar_found?"good":"neutral");
      html += row("Domain Created", d.domain_created,"neutral");
      html += row("Paste Mentions", d.paste_mentions?"Yes":"No", d.paste_mentions?"bad":"good");
      html += row("Risk Score", mod.result.risk, mod.result.risk>50?"bad":"good");
    }

    if(mod.module === "Username Intel"){
      Object.entries(d).forEach(([site,found])=>{
        html += row(site, found?"Found":"Not Found", found?"good":"neutral");
      });
    }

    if(mod.module === "Domain Intel"){
      html += row("IP Address", d.ip,"neutral");
      html += row("Created", d.created,"neutral");
      html += row("Registrar", d.registrar,"neutral");
    }

    if(mod.module === "IP Intel"){
      html += row("Country", d.country,"neutral");
      html += row("City", d.city,"neutral");
      html += row("ISP", d.isp,"neutral");
      html += row("Org", d.org,"neutral");
    }

    card.innerHTML = html;
    resultsDiv.appendChild(card);
  });

  if(data.history && data.history.length){
    const historyCard = document.createElement("div");
    historyCard.className="resultCard";

    let html = `<div class="resultTitle">Previous Scan</div>`;

    data.history.forEach(scan=>{
      const date = new Date(scan.created_at).toLocaleString();
      html += `<div class="row">
        <span>Risk</span>
        <span class="${scan.overall_risk > 60 ? "bad" : scan.overall_risk > 25 ? "neutral" : "good"}">${scan.overall_risk}</span>
      </div>`;
      html += `<div class="row">
        <span>Date</span>
        <span class="neutral">${date}</span>
      </div>`;
    });

    historyCard.innerHTML = html;
    resultsDiv.appendChild(historyCard);
  }
}