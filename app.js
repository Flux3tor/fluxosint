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

  const modules = data.results;

  modules.forEach(mod=>{
    const card = document.createElement("div");
    card.className="resultCard";

    let html = `<div class="resultTitle">${mod.module}</div>`;
    const d = mod.result.data || {};

    if(mod.module === "Email Intel"){
      html += row("Disposable", d.disposable ? "Yes":"No", d.disposable?"bad":"good");
      html += row("Gravatar", d.gravatar_found ? "Found":"None", d.gravatar_found?"good":"neutral");
      html += row("Domain Created", d.domain_created);
      html += row("Paste Mentions", d.paste_mentions?"Yes":"No", d.paste_mentions?"bad":"good");
      html += row("Risk Score", mod.result.risk, mod.result.risk>50?"bad":"good");
    }

    if(mod.module === "Username Intel"){
      Object.entries(d).forEach(([site,found])=>{
        html += row(site, found?"Found":"Not Found", found?"good":"neutral");
      });
    }

    if(mod.module === "Domain Intel"){
      html += row("IP Address", d.ip);
      html += row("Created", d.created);
      html += row("Registrar", d.registrar);
    }

    if(mod.module === "IP Intel"){
      html += row("Country", d.country);
      html += row("City", d.city);
      html += row("ISP", d.isp);
      html += row("Org", d.org);
    }

    card.innerHTML = html;
    resultsDiv.appendChild(card);
  });
}
