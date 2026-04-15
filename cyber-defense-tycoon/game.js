// =====================================================
// CYBER DEFENSE TYCOON - Game Engine
// Professional idle/strategy cybersecurity game
// =====================================================

'use strict';

// ===== GAME CONFIG =====
const CONFIG = {
  TICK_MS: 100,
  CREDITS_PER_SEC_BASE: 5,
  TRAFFIC_BUILD_RATE: 0.8,
  ATTACK_INTERVAL_BASE: 12000,
  ATTACK_INTERVAL_MIN: 4000,
  NEXT_WAVE_ATTACKS: 5,
};

// ===== ATTACK TYPES =====
const ATTACKS = {
  DDoS: {
    name: 'DDoS Flood',
    icon: '🌊',
    color: '#ff2d55',
    damage: 15,
    hp: 100,
    counter: 'CDN',
    description: 'Inundação massiva de tráfego',
    button: { label: 'MITIGAR', bg: '#ff2d5520', border: '#ff2d55', color: '#ff2d55' },
  },
  SQL: {
    name: 'SQL Injection',
    icon: '💉',
    color: '#ff8c00',
    damage: 20,
    hp: 80,
    counter: 'WAF',
    description: 'Injeção maliciosa no banco de dados',
    button: { label: 'SANITIZAR', bg: '#ff8c0020', border: '#ff8c00', color: '#ff8c00' },
  },
  Phishing: {
    name: 'Phishing',
    icon: '🎣',
    color: '#bf5fff',
    damage: 12,
    hp: 60,
    counter: 'DMARC',
    description: 'Engenharia social via email falso',
    button: { label: 'IDENTIFICAR', bg: '#bf5fff20', border: '#bf5fff', color: '#bf5fff' },
  },
  Brute: {
    name: 'Brute Force',
    icon: '🔨',
    color: '#ffe000',
    damage: 10,
    hp: 120,
    counter: 'RateLimit',
    description: 'Tentativas massivas de login',
    button: { label: 'BLOQUEAR', bg: '#ffe00020', border: '#ffe000', color: '#ffe000' },
  },
  Buffer: {
    name: 'Buffer Overflow',
    icon: '💾',
    color: '#ff6b35',
    damage: 25,
    hp: 70,
    counter: 'ASLR',
    description: 'Sobrescrita maliciosa de memória',
    button: { label: 'ISOLAR', bg: '#ff6b3520', border: '#ff6b35', color: '#ff6b35' },
  },
  MITM: {
    name: 'Man-in-Middle',
    icon: '👃',
    color: '#00ccff',
    damage: 18,
    hp: 90,
    counter: 'TLS',
    description: 'Interceptação de comunicação',
    button: { label: 'CRIPTOGRAFAR', bg: '#00ccff20', border: '#00ccff', color: '#00ccff' },
  },
  Ransomware: {
    name: 'Ransomware',
    icon: '🔒',
    color: '#ff2d8c',
    damage: 30,
    hp: 150,
    counter: 'Backup',
    description: 'Criptografia maliciosa de arquivos',
    button: { label: 'RESTAURAR', bg: '#ff2d8c20', border: '#ff2d8c', color: '#ff2d8c' },
  },
  XSS: {
    name: 'XSS Attack',
    icon: '📜',
    color: '#a0ff00',
    damage: 14,
    hp: 65,
    counter: 'CSP',
    description: 'Injeção de script malicioso',
    button: { label: 'SANITIZAR', bg: '#a0ff0020', border: '#a0ff00', color: '#a0ff00' },
  },
};

// ===== SHOP ITEMS =====
const DEFENSES = [
  {
    id: 'Firewall',
    name: 'Firewall Básico',
    icon: '🧱',
    price: 50,
    color: '#00d4ff',
    desc: '+20% resistência geral. Filtra IPs maliciosos.',
    bonus: { globalArmor: 20 },
    counters: [],
  },
  {
    id: 'CDN',
    name: 'CDN Anti-DDoS',
    icon: '☁️',
    price: 120,
    color: '#ff2d55',
    desc: 'Neutraliza ataques DDoS automaticamente.',
    bonus: { creditsRate: 8 },
    counters: ['DDoS'],
  },
  {
    id: 'WAF',
    name: 'Web App Firewall',
    icon: '🛡️',
    price: 180,
    color: '#ff8c00',
    desc: 'Bloqueia SQL Injection e XSS na borda.',
    bonus: { creditsRate: 5 },
    counters: ['SQL', 'XSS'],
  },
  {
    id: 'DMARC',
    name: 'DMARC + SPF',
    icon: '📧',
    price: 90,
    color: '#bf5fff',
    desc: 'Aniquila ataques de phishing por email.',
    bonus: { creditsRate: 3 },
    counters: ['Phishing'],
  },
  {
    id: 'RateLimit',
    name: 'Rate Limiter',
    icon: '⏱️',
    price: 100,
    color: '#ffe000',
    desc: 'Throttle inteligente contra brute force.',
    bonus: { creditsRate: 4 },
    counters: ['Brute'],
  },
  {
    id: 'ASLR',
    name: 'ASLR + DEP',
    icon: '🧠',
    price: 250,
    color: '#ff6b35',
    desc: 'Randomização de memória. Defensável contra Buffer Overflow.',
    bonus: { globalArmor: 10 },
    counters: ['Buffer'],
  },
  {
    id: 'TLS',
    name: 'TLS 1.3 Encryption',
    icon: '🔐',
    price: 200,
    color: '#00ccff',
    desc: 'Criptografia total em trânsito. Bloqueia MITM.',
    bonus: { creditsRate: 6 },
    counters: ['MITM'],
  },
  {
    id: 'Backup',
    name: 'Backup Imutável',
    icon: '💿',
    price: 350,
    color: '#ff2d8c',
    desc: 'Recuperação instantânea contra Ransomware.',
    bonus: { healOnPurchase: 20 },
    counters: ['Ransomware'],
  },
  {
    id: 'CSP',
    name: 'Content Security Policy',
    icon: '📋',
    price: 140,
    color: '#a0ff00',
    desc: 'Política de segurança que bloqueia XSS.',
    bonus: { creditsRate: 3 },
    counters: ['XSS'],
  },
  {
    id: 'SIEM',
    name: 'SIEM Monitor',
    icon: '📊',
    price: 500,
    color: '#00ff88',
    desc: 'Dobra a geração de créditos e revela próxima wave.',
    bonus: { creditsRate: 20 },
    counters: [],
  },
];

// ===== GAME STATE =====
let state = {
  credits: 100,
  creditsPerSec: CONFIG.CREDITS_PER_SEC_BASE,
  health: 100,
  traffic: 0,
  wave: 1,
  score: 0,
  time: 0,
  paused: false,
  gameOver: false,
  ownedDefenses: new Set(),
  activeAttacks: [],
  attacksDefeated: 0,
  attacksForWave: CONFIG.NEXT_WAVE_ATTACKS,
  attacksInWave: 0,
  nextAttackIn: CONFIG.ATTACK_INTERVAL_BASE / 1000,
  lastAttackTime: Date.now(),
  globalArmor: 0,
  logs: [],
};

// ===== UTILITY =====
const fmt = n => n >= 1000000 ? (n/1000000).toFixed(1)+'M'
            : n >= 1000 ? (n/1000).toFixed(1)+'K'
            : Math.floor(n).toString();

const fmtTime = s => `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`;

function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

function weightedRandom(items, weights) {
  const total = weights.reduce((a, b) => a + b, 0);
  let r = Math.random() * total;
  for (let i = 0; i < items.length; i++) { r -= weights[i]; if (r <= 0) return items[i]; }
  return items[items.length - 1];
}

// ===== MATRIX BACKGROUND =====
function initMatrix() {
  const canvas = document.getElementById('matrixCanvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const cols = Math.floor(canvas.width / 16);
  const drops = Array(cols).fill(1);
  const chars = '01アイウエオカキクケコ<>{}[]|/\\@#$%^&*';

  setInterval(() => {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#00d4ff';
    ctx.font = '13px Share Tech Mono';

    drops.forEach((y, i) => {
      const char = chars[randInt(0, chars.length - 1)];
      ctx.fillText(char, i * 16, y * 16);
      if (y * 16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
      drops[i]++;
    });
  }, 50);
}

// ===== LOG SYSTEM =====
function addLog(msg, type = 'info') {
  const now = new Date();
  const time = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;
  state.logs.unshift({ time, msg, type });
  if (state.logs.length > 50) state.logs.pop();
  renderLog();
}

function renderLog() {
  const container = document.getElementById('log-container');
  const entries = state.logs.slice(0, 20);
  container.innerHTML = entries.map(e =>
    `<div class="log-entry">
      <span class="log-time">[${e.time}]</span>
      <span class="log-${e.type}">${e.msg}</span>
    </div>`
  ).join('');
}

// ===== TOAST =====
function showToast(msg, type = 'info', icon = '💬') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3100);
}

// ===== SHOP RENDER =====
function renderShop() {
  const grid = document.getElementById('shop-grid');
  grid.innerHTML = DEFENSES.map(item => {
    const owned = state.ownedDefenses.has(item.id);
    const affordable = state.credits >= item.price;
    const cls = owned ? 'owned' : (!affordable ? 'cant-afford' : '');

    return `<div class="shop-item ${cls}" 
                 id="shop-${item.id}"
                 style="--item-color: ${item.color}"
                 onclick="buyDefense('${item.id}')">
      <div class="shop-item-header">
        <span class="shop-item-icon">${item.icon}</span>
        <span class="shop-item-name">${item.name}</span>
        ${owned
          ? '<span class="shop-item-owned-badge">✅ ATIVO</span>'
          : `<span class="shop-item-price">💰 ${item.price}</span>`
        }
      </div>
      <div class="shop-item-desc">${item.desc}</div>
      ${item.counters.length > 0
        ? `<div class="shop-item-counter" style="background:${item.color}20; color:${item.color}; border: 1px solid ${item.color}66">
            🎯 Neutraliza: ${item.counters.join(', ')}
           </div>`
        : ''
      }
    </div>`;
  }).join('');
}

// ===== BUY DEFENSE =====
function buyDefense(id) {
  if (state.gameOver || state.paused) return;
  if (state.ownedDefenses.has(id)) return;

  const item = DEFENSES.find(d => d.id === id);
  if (!item) return;

  if (state.credits < item.price) {
    showToast(`Créditos insuficientes! Precisa de ${item.price}`, 'error', '⛔');
    return;
  }

  state.credits -= item.price;
  state.ownedDefenses.add(id);

  // Apply bonuses
  if (item.bonus.creditsRate) state.creditsPerSec += item.bonus.creditsRate;
  if (item.bonus.globalArmor) state.globalArmor += item.bonus.globalArmor;
  if (item.bonus.healOnPurchase) {
    state.health = Math.min(100, state.health + item.bonus.healOnPurchase);
    addLog(`Sistema recuperado em ${item.bonus.healOnPurchase}% via backup!`, 'ok');
  }

  // Auto-defeat matching attacks
  state.activeAttacks.forEach(atk => {
    if (item.counters.includes(atk.type)) {
      setTimeout(() => autoDefeatAttack(atk.id), 300);
    }
  });

  addLog(`[INSTALADO] ${item.name} - defesa ativada!`, 'ok');
  showToast(`${item.icon} ${item.name} instalado!`, 'success', '✅');
  renderShop();
  updateActiveDefenses();
}

// ===== ACTIVE DEFENSES DISPLAY =====
function updateActiveDefenses() {
  const container = document.getElementById('active-defenses-list');
  if (state.ownedDefenses.size === 0) {
    container.innerHTML = '<span class="tag tag-empty">Nenhuma defesa instalada</span>';
    return;
  }
  container.innerHTML = Array.from(state.ownedDefenses).map(id => {
    const item = DEFENSES.find(d => d.id === id);
    return `<span class="tag tag-defense">${item.icon} ${item.id}</span>`;
  }).join('');
}

// ===== ATTACK GENERATION =====
function getAttackTypes() {
  const wave = state.wave;
  const pool = Object.keys(ATTACKS);
  if (wave <= 1) return pool.slice(0, 4);
  if (wave <= 3) return pool.slice(0, 6);
  return pool;
}

function spawnAttack() {
  if (state.gameOver || state.paused) return;
  if (state.activeAttacks.length >= 6) return;

  const pool = getAttackTypes();
  const weights = pool.map(t => state.ownedDefenses.has(ATTACKS[t].counter) ? 0.3 : 1.5);
  const type = weightedRandom(pool, weights);
  const def = ATTACKS[type];

  const wave = state.wave;
  const hpMult = 1 + (wave - 1) * 0.3;
  const dmgMult = 1 + (wave - 1) * 0.15;

  const id = `atk-${Date.now()}-${Math.random().toString(36).slice(2)}`;
  const attack = {
    id,
    type,
    name: def.name,
    icon: def.icon,
    color: def.color,
    counter: def.counter,
    hp: Math.floor(def.hp * hpMult),
    maxHp: Math.floor(def.hp * hpMult),
    damage: Math.floor((def.damage * dmgMult) * (1 - state.globalArmor / 200)),
    button: def.button,
  };

  state.activeAttacks.push(attack);
  state.attacksInWave++;

  document.getElementById('arena-idle').style.display = 'none';
  document.getElementById('wave-status').textContent = '🔴 SOB ATAQUE!';
  document.getElementById('wave-status').classList.add('under-attack');

  addLog(`[ALERTA] ${def.name} detectado! Power: ${attack.damage}HP/s`, 'err');
  showToast(`⚠️ ${def.name} ingressou!`, 'error', def.icon);

  renderArena();
}

// ===== RENDER ARENA =====
function renderArena() {
  const arena = document.getElementById('attacks-arena');
  const idle = document.getElementById('arena-idle');

  // Clear old cards (keep idle)
  Array.from(arena.querySelectorAll('.attack-card')).forEach(el => el.remove());

  if (state.activeAttacks.length === 0) {
    idle.style.display = 'block';
    document.getElementById('wave-status').textContent = '🟢 SISTEMA ESTÁVEL';
    document.getElementById('wave-status').classList.remove('under-attack');
    return;
  }
  idle.style.display = 'none';

  state.activeAttacks.forEach(atk => {
    const pct = (atk.hp / atk.maxHp) * 100;
    const autoDefended = state.ownedDefenses.has(atk.counter);

    const card = document.createElement('div');
    card.className = `attack-card attack-card-type-${atk.type}`;
    card.id = `card-${atk.id}`;
    card.style.borderColor = atk.color;
    card.innerHTML = `
      <div class="attack-icon">${atk.icon}</div>
      <div class="attack-name" style="color:${atk.color}">${atk.name}</div>
      <div class="attack-power">⚡ ${atk.damage} DMG/s · HP: ${atk.hp}/${atk.maxHp}</div>
      <div class="attack-hp-track">
        <div class="attack-hp-fill" id="hp-${atk.id}" style="width:${pct}%; background:${atk.color}; box-shadow: 0 0 8px ${atk.color}88"></div>
      </div>
      ${autoDefended
        ? `<div style="margin-top:8px; color: #00ff88; font-family: var(--font-mono); font-size:10px">⚡ AUTO-NEUTRALIZADO (${atk.counter})</div>`
        : `<button class="attack-btn" 
                  onclick="manualBlock('${atk.id}')" 
                  style="background:${atk.button.bg}; border-color:${atk.button.border}; color:${atk.button.color}">
              ${atk.button.label}
           </button>
           <div class="attack-counter-hint">🏪 Instale <strong style="color:${atk.color}">${atk.counter}</strong> para auto-neutralizar</div>`
      }
    `;
    arena.appendChild(card);
  });
}

// ===== MANUAL BLOCK =====
function manualBlock(id) {
  if (state.gameOver || state.paused) return;
  const atk = state.activeAttacks.find(a => a.id === id);
  if (!atk) return;

  // Manual block reduces HP by a portion
  const reduction = Math.floor(atk.maxHp * 0.4);
  atk.hp = Math.max(0, atk.hp - reduction);

  if (atk.hp <= 0) {
    defeatAttack(id, true);
  } else {
    // Update HP bar
    const bar = document.getElementById(`hp-${id}`);
    if (bar) bar.style.width = `${(atk.hp / atk.maxHp) * 100}%`;
    addLog(`Contra-atacando ${atk.name}... HP restante: ${atk.hp}`, 'warn');
  }
}

// ===== AUTO DEFEAT =====
function autoDefeatAttack(id) {
  defeatAttack(id, false);
}

function defeatAttack(id, manual) {
  const idx = state.activeAttacks.findIndex(a => a.id === id);
  if (idx === -1) return;
  const atk = state.activeAttacks[idx];

  state.activeAttacks.splice(idx, 1);
  state.attacksDefeated++;
  state.score += manual ? 150 : 80;

  const card = document.getElementById(`card-${id}`);
  if (card) {
    card.classList.add('defeated');
    setTimeout(() => card.remove(), 500);
  }

  const bonus = manual ? randInt(20, 50) : randInt(8, 20);
  state.credits += bonus;
  addLog(`[NEUTRALIZADO] ${atk.name}! +${bonus} créditos`, 'ok');
  if (manual) showToast(`+${bonus} créditos por neutralização manual!`, 'success', '💰');

  checkWaveProgress();
  setTimeout(renderArena, 600);
}

// ===== WAVE PROGRESS =====
function checkWaveProgress() {
  const progress = Math.min(state.attacksDefeated / (state.attacksForWave * state.wave), 1);
  document.getElementById('wave-progress-bar').style.width = `${progress * 100}%`;
  document.getElementById('attacks-defeated').textContent = `${state.attacksDefeated} ataques neutralizados`;

  if (state.attacksDefeated >= state.attacksForWave * state.wave) {
    advanceWave();
  }
}

// ===== ADVANCE WAVE =====
function advanceWave() {
  state.wave++;
  const bonus = state.wave * 100;
  state.credits += bonus;
  state.score += state.wave * 500;
  state.attacksInWave = 0;

  document.getElementById('wave-display').textContent = state.wave;
  document.getElementById('wave-progress-label').textContent = state.wave;

  addLog(`[ONDA ${state.wave}] Novo ciclo de ataques iniciado! +${bonus} créditos`, 'info');
  showToast(`🌊 ONDA ${state.wave} INICIADA! +${bonus} créditos`, 'info', '🌊');
  updateWavePreview();
}

// ===== WAVE PREVIEW =====
function updateWavePreview() {
  const pool = getAttackTypes();
  const preview = document.getElementById('wave-preview-content');
  const hasSIEM = state.ownedDefenses.has('SIEM');

  if (hasSIEM) {
    // SIEM reveals next 3 actual attacks
    const sample = pool.slice(0, 3).map(t => ATTACKS[t]);
    preview.innerHTML = sample.map(a =>
      `<span class="preview-tag" style="border-color:${a.color}; color:${a.color}">${a.icon} ${a.name}</span>`
    ).join('');
  } else {
    preview.innerHTML = `<span class="preview-text">Instale 📊 SIEM para revelar próxima wave...</span>`;
  }
}

// ===== MAIN GAME TICK =====
let lastTick = Date.now();
let ticksPerSec = 0;
let secAccum = 0;

function gameTick() {
  if (state.paused || state.gameOver) return;

  const now = Date.now();
  const dt = (now - lastTick) / 1000;
  lastTick = now;

  // Time counter
  secAccum += dt;
  if (secAccum >= 1) {
    secAccum = 0;
    state.time++;
    ticksPerSec = 0;
  }

  // Credits income
  state.credits += state.creditsPerSec * dt;

  // Traffic animation
  state.traffic = Math.min(100, state.traffic + CONFIG.TRAFFIC_BUILD_RATE * dt * 10);

  // Attack timer
  const attackInterval = Math.max(
    CONFIG.ATTACK_INTERVAL_MIN,
    CONFIG.ATTACK_INTERVAL_BASE - (state.wave - 1) * 1000
  );
  state.nextAttackIn = Math.max(0, (attackInterval - (now - state.lastAttackTime)) / 1000);

  if (now - state.lastAttackTime >= attackInterval) {
    spawnAttack();
    state.lastAttackTime = now;
  }

  // Process active attacks damage
  state.activeAttacks.forEach(atk => {
    const hasCounter = state.ownedDefenses.has(atk.counter);
    if (hasCounter) {
      // Auto-reduce HP
      atk.hp -= atk.maxHp * 0.1 * dt * 5;
      if (atk.hp <= 0) {
        setTimeout(() => defeatAttack(atk.id, false), 50);
      }
    } else {
      // Deal damage to server
      const armor = state.globalArmor / 100;
      state.health -= atk.damage * dt * (1 - armor) * 0.05;
    }
  });

  state.health = Math.max(0, state.health);

  // Update UI
  updateHUD(dt);

  if (state.health <= 0) {
    triggerGameOver();
  }
}

// ===== HUD UPDATE =====
function updateHUD(dt) {
  // Credits
  const credEl = document.getElementById('credits-display');
  credEl.textContent = fmt(state.credits);
  document.getElementById('credits-rate').textContent = `+${state.creditsPerSec}/s`;

  // Update shop affordability
  DEFENSES.forEach(item => {
    const el = document.getElementById(`shop-${item.id}`);
    if (!el) return;
    if (!state.ownedDefenses.has(item.id)) {
      el.classList.toggle('cant-afford', state.credits < item.price);
    }
  });

  // Health bar
  const hPct = Math.max(0, state.health);
  document.getElementById('health-bar').style.width = `${hPct}%`;
  document.getElementById('health-pct').textContent = `${Math.floor(hPct)}%`;
  const bar = document.getElementById('health-bar');
  bar.classList.remove('warning', 'danger');
  if (hPct < 30) bar.classList.add('danger');
  else if (hPct < 60) bar.classList.add('warning');

  // Traffic bar
  document.getElementById('traffic-bar').style.width = `${state.traffic}%`;
  document.getElementById('traffic-pct').textContent = `${Math.floor(state.traffic)}%`;

  // Score + time
  document.getElementById('score-display').textContent = fmt(state.score);
  document.getElementById('time-display').textContent = fmtTime(state.time);

  // Attack HP bars
  state.activeAttacks.forEach(atk => {
    const bar = document.getElementById(`hp-${atk.id}`);
    if (bar) bar.style.width = `${(atk.hp / atk.maxHp) * 100}%`;
  });

  // Next attack timer
  document.getElementById('next-attack-timer').textContent = Math.ceil(state.nextAttackIn);
}

// ===== GAME OVER =====
function triggerGameOver() {
  state.gameOver = true;
  addLog('[CRÍTICO] Sistema comprometido! Reiniciando...', 'err');

  const overlay = document.getElementById('modal-overlay');
  document.getElementById('modal-icon').textContent = '💀';
  document.getElementById('modal-title').textContent = 'SISTEMA COMPROMETIDO';
  document.getElementById('modal-desc').textContent = `Os invasores venceram na Onda ${state.wave}. O servidor foi derrubado.`;
  document.getElementById('modal-stats').innerHTML = `
    <div class="modal-stat">
      <div class="modal-stat-label">ONDA ALCANÇADA</div>
      <div class="modal-stat-value">${state.wave}</div>
    </div>
    <div class="modal-stat">
      <div class="modal-stat-label">SCORE FINAL</div>
      <div class="modal-stat-value">${fmt(state.score)}</div>
    </div>
    <div class="modal-stat">
      <div class="modal-stat-label">ATAQUES NEUTRALIZADOS</div>
      <div class="modal-stat-value">${state.attacksDefeated}</div>
    </div>
    <div class="modal-stat">
      <div class="modal-stat-label">TEMPO TOTAL</div>
      <div class="modal-stat-value">${fmtTime(state.time)}</div>
    </div>
  `;
  overlay.classList.add('active');
}

// ===== RESET GAME =====
function resetGame() {
  state = {
    credits: 100,
    creditsPerSec: CONFIG.CREDITS_PER_SEC_BASE,
    health: 100,
    traffic: 0,
    wave: 1,
    score: 0,
    time: 0,
    paused: false,
    gameOver: false,
    ownedDefenses: new Set(),
    activeAttacks: [],
    attacksDefeated: 0,
    attacksForWave: CONFIG.NEXT_WAVE_ATTACKS,
    attacksInWave: 0,
    nextAttackIn: CONFIG.ATTACK_INTERVAL_BASE / 1000,
    lastAttackTime: Date.now(),
    globalArmor: 0,
    logs: [],
  };
  lastTick = Date.now();

  document.getElementById('modal-overlay').classList.remove('active');
  document.getElementById('wave-display').textContent = '1';
  document.getElementById('wave-progress-label').textContent = '1';
  document.getElementById('wave-progress-bar').style.width = '0%';
  document.getElementById('attacks-defeated').textContent = '0 ataques neutralizados';

  // Clear arena
  const arena = document.getElementById('attacks-arena');
  Array.from(arena.querySelectorAll('.attack-card')).forEach(el => el.remove());
  document.getElementById('arena-idle').style.display = 'block';

  renderShop();
  updateActiveDefenses();
  addLog('[SISTEMA] Servidor reiniciado. Bem-vindo ao Cyber Defense Tycoon!', 'info');
  addLog('[SISTEMA] Compre defesas na loja para neutralizar ataques automaticamente.', 'info');
  updateWavePreview();
}

// ===== INIT & CONTROLS =====
document.addEventListener('DOMContentLoaded', () => {
  initMatrix();

  // Scanline effect
  const scanline = document.createElement('div');
  scanline.className = 'scan-overlay';
  document.body.appendChild(scanline);

  resetGame();

  // Start game loop
  setInterval(gameTick, CONFIG.TICK_MS);

  // Pause button
  document.getElementById('btn-pause').addEventListener('click', () => {
    state.paused = !state.paused;
    const btn = document.getElementById('btn-pause');
    btn.textContent = state.paused ? '▶ RESUMIR' : '⏸ PAUSA';
    if (!state.paused) lastTick = Date.now();
  });

  // Restart
  document.getElementById('btn-restart').addEventListener('click', resetGame);

  // Share score
  document.getElementById('btn-share').addEventListener('click', () => {
    const text = `🛡️ Cyber Defense Tycoon\n⚡ Score: ${fmt(state.score)}\n🌊 Onda: ${state.wave}\n⏱️ Tempo: ${fmtTime(state.time)}\n\n🎮 Pode me superar?`;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text);
      showToast('Score copiado para o clipboard!', 'info', '📋');
    }
  });

  // Initial logs
  addLog('[ONLINE] Servidor ALPHA inicializado com sucesso!', 'ok');
  addLog('[ALERTA] Ameaças detectadas no perímetro. Compre defesas!', 'warn');
});
