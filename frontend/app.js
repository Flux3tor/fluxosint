async function scan() {
  const value = document.getElementById("targetInput").value;
  const type = document.getElementById("typeSelect").value;

  document.getElementById("result").textContent = "Scanning…";

  const res = await fetch(
    "https://api.fluxosint.flux3tor.xyz/targets/",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: type,
        value: value
      })
    }
  );

  const data = await res.json();
  document.getElementById("result").textContent =
    JSON.stringify(data, null, 2);
}
