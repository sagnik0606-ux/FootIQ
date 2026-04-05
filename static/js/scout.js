let targetPlayer = null;
const primaryLeague = "Premier League";
const primarySeason = "2024-25";

// Elements
const searchInp = document.getElementById("scout-search");
const resultsEl = document.getElementById("scout-results");
const targetCard = document.getElementById("target-player-card");
const goBtn = document.getElementById("scout-go-btn");
const matchesList = document.getElementById("scout-matches-list");
const resultsSection = document.getElementById("scout-results-section");

// Debounce util
function debounce(func, timeout = 300){
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => { func.apply(this, args); }, timeout);
  };
}

// 1. Search Target Player
const doSearch = debounce(async (isGlobal = false) => {
  const q = searchInp.value.trim();
  if (q.length < 3) { resultsEl.innerHTML = ""; resultsEl.classList.remove("active"); return; }
  try {
    const url = `/api/search?name=${encodeURIComponent(q)}&league=${primaryLeague}&season=${primarySeason}${isGlobal === true ? '&all_leagues=1' : ''}`;
    const res  = await fetch(url);
    const data = await res.json();
    if (data.error) { return; }
    if (!data.length && !isGlobal) {
      return doSearch(true);
    } else if (!data.length) {
      resultsEl.innerHTML = `<div class="result-item" style="color:var(--muted);justify-content:center">No players found</div>`;
      resultsEl.classList.add("active"); return;
    }
    resultsEl.innerHTML = data.map(p => `
      <div class="result-item" data-id="${p.id}" data-player='${JSON.stringify(p).replace(/'/g,"&#39;")}'>
        <img src="${p.photo||_scoutInitials(p.name)}" onerror="this.src='${_scoutInitials(p.name)}'" />
        <div>
          <div class="result-name">${p.name}</div>
          <div class="result-meta">${p.league ? p.league + ' · ' : ''}${p.team} · ${p.position}</div>
        </div>
      </div>
    `).join("");
    resultsEl.classList.add("active");
  } catch {}
}, 380);

searchInp.addEventListener("input", doSearch);

resultsEl.addEventListener("click", e => {
  const item = e.target.closest(".result-item[data-id]");
  if (!item) return;
  targetPlayer = JSON.parse(item.dataset.player);
  
  targetCard.innerHTML = `
    <div style="display:flex;align-items:center;gap:12px;">
      <img src="${targetPlayer.photo || _scoutInitials(targetPlayer.name)}" 
           style="width:60px;height:60px;border-radius:50%;object-fit:cover;border:2px solid var(--c0)" 
           onerror="this.src='${_scoutInitials(targetPlayer.name)}'" />
      <div>
        <div style="font-size:20px;font-weight:700;color:var(--text)">${targetPlayer.name}</div>
        <div style="font-size:13px;color:var(--muted)">${targetPlayer.team} · ${targetPlayer.position}</div>
      </div>
    </div>
  `;
  targetCard.style.display = "block";
  resultsEl.classList.remove("active");
  searchInp.value = "";
  
  goBtn.disabled = false;
});

document.addEventListener("click", () => {
    document.querySelectorAll(".search-results.active").forEach(r => r.classList.remove("active"));
});

// 2. Fetch Matches
goBtn.addEventListener("click", async () => {
    if(!targetPlayer) return;
    
    goBtn.disabled = true;
    goBtn.textContent = "Crunching algos...";
    
    const body = {
        target_id: targetPlayer.id,
        target_league: primaryLeague,
        target_season: primarySeason,
        max_age: document.getElementById("scout-max-age").value,
        league_pool: document.getElementById("scout-league-pool").value
    }
    
    try {
        const res = await fetch("/api/scout", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        });
        const data = await res.json();
        
        if (!res.ok || data.error) {
            alert(data.error || "Scouting failed");
            goBtn.disabled = false;
            goBtn.textContent = "Run Scouting Algorithm →";
            return;
        }
        
        renderMatches(data.matches, data.widened);
        
    } catch(err) {
        alert("Network error");
    } finally {
        goBtn.disabled = false;
        goBtn.textContent = "Run Scouting Algorithm →";
    }
});

function _scoutInitials(name, size=50) {
    const initials = name.split(" ").map(w => w[0]).slice(0,2).join("").toUpperCase();
    const colors = ["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4"];
    const color = colors[name.charCodeAt(0) % colors.length];
    const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='${size}' height='${size}' viewBox='0 0 ${size} ${size}'><circle cx='${size/2}' cy='${size/2}' r='${size/2}' fill='${color}22'/><circle cx='${size/2}' cy='${size/2}' r='${size/2-1}' fill='none' stroke='${color}' stroke-width='1.5'/><text x='${size/2}' y='${size/2+size*0.15}' text-anchor='middle' font-family='system-ui,sans-serif' font-size='${size*0.3}' font-weight='700' fill='${color}'>${initials}</text></svg>`;
    return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}

async function _loadScoutImage(name, team, imgEl) {
    try {
        const url = `/api/player-image?name=${encodeURIComponent(name)}${team ? `&team=${encodeURIComponent(team)}` : ""}`;
        const r = await fetch(url);
        if (r.ok) {
            const d = await r.json();
            if (d.url) { imgEl.src = d.url; return; }
        }
    } catch {}
    imgEl.src = _scoutInitials(name);
}

function renderMatches(matches, widened) {
    const notice = widened
        ? `<div style="text-align:center;color:var(--muted);font-size:13px;padding:8px 0 16px">Age filter relaxed to show best available matches</div>`
        : "";

    if (!matches || matches.length === 0) {
        matchesList.innerHTML = notice + `<div style="text-align:center;color:var(--muted);padding:40px">No matching players found in the database.</div>`;
        resultsSection.style.display = "block";
        resultsSection.querySelectorAll('.scroll-animate').forEach(el => el.classList.add('scroll-animate-visible'));
        return;
    }

    matchesList.innerHTML = notice + matches.map((m, i) => `
        <div class="glass-card" style="display:flex;align-items:center;padding:20px;gap:20px;border-color: ${i===0 ? 'var(--c0)' : 'var(--border)'}; transform:none; cursor:default">
            <div style="font-size:24px;font-weight:900;color:var(--dim);width:30px">#${i+1}</div>
            <img data-name="${m.name}" src="${_scoutInitials(m.name)}" 
                 onerror="this.src='${_scoutInitials(m.name)}'"
                 style="width:50px;height:50px;border-radius:50%;object-fit:cover" />
            <div style="flex:1">
                <div style="font-size:18px;font-weight:700;color:var(--text)">${m.name} <span style="font-size:12px;color:var(--muted);font-weight:500;margin-left:6px">(Age ${m.age})</span></div>
                <div style="font-size:13px;color:var(--dim)">${m.league} · ${m.team}</div>
            </div>
            <div style="display:flex;gap:24px;align-items:center;">
                <div style="text-align:right">
                    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--muted)">Composite Score</div>
                    <div style="font-size:22px;font-weight:800;color:var(--text)">${m.score}</div>
                </div>
                <div style="width:1px;height:40px;background:var(--border)"></div>
                <div style="text-align:right; width: 100px;">
                    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--c0)">Similarity Match</div>
                    <div style="font-size:22px;font-weight:800;color:var(--c0)">${m.sim_score}%</div>
                </div>
            </div>
        </div>
    `).join("");

    // Show results immediately, then load images async
    resultsSection.style.display = "block";
    resultsSection.querySelectorAll('.scroll-animate').forEach(el => el.classList.add('scroll-animate-visible'));
    setTimeout(() => resultsSection.scrollIntoView({ behavior:"smooth", block:"start" }), 100);

    // Load images in background — non-blocking
    matchesList.querySelectorAll("img[data-name]").forEach(img => {
        const team = img.closest(".glass-card").querySelector("div[style*='color:var(--dim)']").textContent.split(" · ")[1];
        _loadScoutImage(img.dataset.name, team, img);
    });
}
