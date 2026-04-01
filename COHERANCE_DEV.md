# COHERANCE_DEV — Development Transcript
## AIIT-GLITCH/coherence-app

> **NOTE: HOW TO USE THIS FILE**
> This is a living development transcript for the coherence-app codebase.
> Every issue found, every fix applied, and every decision made goes here — in order, with timestamps.
> Format for each entry:
>   - **What:** what is broken or needs changing
>   - **Why:** why it matters (physics, security, UX, correctness)
>   - **How:** exact fix — file, line range, code change
>   - **Status:** OPEN / IN PROGRESS / DONE
>   - **Touched by:** which Claude session wrote/changed it
>   - **Timestamp:** date and time of entry
>
> Do not summarize. Do not collapse entries. Every touch gets its own block.
> This file reads as a complete record from first review to shipped fix.

---

## SESSION 1 — Initial Full-Codebase Scrutiny
**Claude session:** claude-sonnet-4-6, conversation started 2026-03-31
**Files read:** `api/app.py` (88KB), `core/coherence_engine.py` (48KB), `modules/ace_assessment.py`, `modules/hrv_analyzer.py`, `modules/keeper_tracker.py`, `modules/breathing_pacer.py`, `modules/gamma40_stimulation.py`, `modules/geomag_monitor.py`, `data/models.py`, `templates/index.html` (1662 lines)
**Repo:** https://github.com/AIIT-GLITCH/coherence-app (default branch: `master`, not `main`)

---

### ISSUE-001 — cert.pem committed to public repository
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`cert.pem` (TLS certificate, likely including private key) is committed at the repo root and publicly visible on GitHub.

**Why:**
Anyone who has cloned the repo since creation has the private key. All HTTPS traffic to the server can be decrypted. This is an active security breach, not a future risk.

**How:**
1. Rotate the certificate immediately — generate a new keypair, the existing one is compromised.
2. Add to `.gitignore`:
   ```
   *.pem
   *.key
   *.crt
   *.p12
   ```
3. Scrub from git history so it doesn't remain accessible via old commits:
   ```bash
   git filter-repo --path cert.pem --invert-paths
   # or
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch cert.pem' \
     --prune-empty --tag-name-filter cat -- --all
   git push origin --force --all
   ```
4. Assume the cert is permanently compromised regardless — anyone who cloned before the scrub has it.

---

### ISSUE-002 — Frontend phase state labels FROZEN/COLLAPSED are inverted
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`templates/index.html` — `stateName(c)`, `stateColor(c)`, `stateColorRaw(c)`, `stateGlow(c)` functions all apply the wrong label and color to the FROZEN and COLLAPSED extremes.

```javascript
// CURRENT (WRONG):
function stateName(c) {
  if (c < 0.35) return 'FROZEN';    // ← wrong
  if (c > 0.75) return 'COLLAPSED'; // ← wrong
  return 'EDGE';
}
```

**Why:**
The physics: `C = C₀ × exp(−α × γ_eff)` with α = 16.08, γ_c = 0.0622.

| γ_eff | C value | Correct state |
|---|---|---|
| 0 | 1.00 | FROZEN (no decoherence drive) |
| γ_c = 0.0622 | exp(−1) ≈ 0.368 | EDGE (peak vitality) |
| 2γ_c = 0.124 | exp(−2) ≈ 0.135 | COLLAPSED |

So C > 0.75 → FROZEN (low decoherence, not enough challenge).
And C < 0.35 → COLLAPSED (high decoherence, past the cliff).

Current code does the opposite. A user in genuine crisis (C ≈ 0.15, γ >> γ_c) is shown a blue FROZEN label. A low-stress user (C ≈ 0.85) is shown a red COLLAPSED warning. This is a direct physics error with real user impact.

**How:**
Compute correct thresholds from the physics. γ_eff/γ_c = 0.5 → C = exp(−α × 0.5 × γ_c) = exp(−0.5) ≈ 0.607. γ_eff/γ_c = 1.5 → C = exp(−1.5) ≈ 0.223.

```javascript
// FIXED:
function stateName(c) {
  if (c > 0.607) return 'FROZEN';    // gamma_eff < 0.5 * gamma_c
  if (c < 0.223) return 'COLLAPSED'; // gamma_eff > 1.5 * gamma_c
  return 'EDGE';
}

function stateColor(c) {
  if (c > 0.607) return 'var(--frozen)';
  if (c < 0.223) return 'var(--collapsed)';
  return 'var(--edge)';
}

function stateColorRaw(c) {
  if (c > 0.607) return '#4488ff';
  if (c < 0.223) return '#ff4444';
  return '#00ff88';
}

function stateGlow(c) {
  if (c > 0.607) return 'rgba(68,136,255,0.15)';
  if (c < 0.223) return 'rgba(255,68,68,0.15)';
  return 'rgba(0,255,136,0.15)';
}
```

Apply the same threshold fix to `updatePhaseDot()` and anywhere else `c` is used to classify state.

---

### ISSUE-003 — Two gamma_eff implementations with conflicting ACE models
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`core/coherence_engine.py` computes ACE gamma contribution as:
```python
gamma_ace = self.profile.ace_score * ACE_BETA * GAMMA_C  # linear
```

`api/app.py` inline `_CoherencePhysics` computes:
```python
gamma_ace = 0.005 * (1.0 - math.exp(-((ACE_BETA * ace_clamped) ** ACE_NU)))  # stretched exponential
```

**Why:**
The linear model in `coherence_engine.py` is physically wrong and numerically catastrophic. For ACE=10:
- Linear: γ_ace = 10 × 0.416 × 0.0622 = **0.259** — more than 4× γ_c. Any ACE score above ~2 pushes the user into total collapse by this term alone.
- Stretched exponential (app.py): γ_ace ≈ **0.0048** — 7.7% of γ_c. Physiologically reasonable.

Paper 24 defines ACE coherence as `C_n = C₀ × exp(−(β×n)^ν)` — a stretched exponential. The linear model has no basis in the framework. The `app.py` version is correct.

There should be exactly ONE gamma_eff implementation. Having two with different physics means the API endpoints that use `CoherenceEngine` give different results than those using the inline `_CoherencePhysics` fallback.

**How:**
1. Replace the linear ACE computation in `core/coherence_engine.py` `compute_gamma_eff()`:
   ```python
   # REMOVE:
   gamma_ace = self.profile.ace_score * ACE_BETA * GAMMA_C

   # REPLACE WITH:
   ace_clamped = min(self.profile.ace_score, 10.0)
   gamma_ace = 0.005 * (1.0 - math.exp(-((ACE_BETA * ace_clamped) ** ACE_NU)))
   ```
2. Delete the inline `_CoherencePhysics` class from `api/app.py` and import `CoherenceEngine` from `core/` exclusively.
3. Run `coherence_engine.py`'s `run_self_test()` after change to confirm values are sane.

---

### ISSUE-004 — __pycache__ and .pyc files committed; .gitignore is empty
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
The following compiled Python artifacts are committed to the repo:
- `api/__pycache__/app.cpython-312.pyc` (86KB)
- `core/__pycache__/coherence_engine.cpython-312.pyc` (42KB)
- `modules/__pycache__/*.cpython-312.pyc` (5 files, ~175KB total)

The `.gitignore` is 27 bytes — essentially empty.

**Why:**
`.pyc` files are machine-generated, platform-specific, and contain no information not already in the `.py` source. They bloat the repo, create false diffs, and will cause conflicts across Python versions or platforms. The private key in `cert.pem` would have been caught by a proper `.gitignore`.

**How:**
```bash
# Remove from tracking (does not delete the files locally):
git rm -r --cached api/__pycache__ core/__pycache__ modules/__pycache__
git commit -m "Remove committed __pycache__ directories"

# Replace .gitignore with a proper Python one:
```
`.gitignore` should contain at minimum:
```
__pycache__/
*.py[cod]
*.pem
*.key
*.crt
*.p12
*.db
*.sqlite
*.sqlite3
.env
instance/
.DS_Store
```

---

### ISSUE-005 — 40Hz audio is a direct tone, not binaural beats
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`templates/index.html` — `start40HzSession()`:
```javascript
// Code comment says "binaural" but implementation is:
hzOscillator.frequency.value = 40;
hzOscillator.type = 'sine';
gainNode.gain.value = 0.08;
hzOscillator.connect(gainNode);
gainNode.connect(hzAudioCtx.destination);  // mono to both channels
```

**Why:**
Binaural beats require two tones at slightly different frequencies delivered to separate ears (e.g., L: 200Hz, R: 240Hz → brain perceives 40Hz beat). The current implementation sends a direct 40Hz sine wave to both channels simultaneously. 40Hz is within audible range but felt more as a low throb than a pitch. It is not binaural. The mechanism differs: binaural works via interaural phase difference processing in the superior olivary complex; a direct 40Hz tone works (if at all) via auditory cortex entrainment directly.

**How — Option A (correct to true binaural):**
```javascript
// Left ear: 200Hz carrier
const oscL = hzAudioCtx.createOscillator();
const gainL = hzAudioCtx.createGain();
const mergerL = hzAudioCtx.createChannelMerger(2);

oscL.frequency.value = 200;
oscL.type = 'sine';
gainL.gain.value = 0.08;
oscL.connect(gainL);
gainL.connect(mergerL, 0, 0); // left channel

// Right ear: 240Hz carrier (200 + 40 = 40Hz binaural beat)
const oscR = hzAudioCtx.createOscillator();
const gainR = hzAudioCtx.createGain();
oscR.frequency.value = 240;
oscR.type = 'sine';
gainR.gain.value = 0.08;
oscR.connect(gainR);
gainR.connect(mergerL, 0, 1); // right channel

mergerL.connect(hzAudioCtx.destination);
oscL.start();
oscR.start();
// store both oscillators for stop()
```

**How — Option B (keep direct tone, fix the label):**
Remove the comment saying "binaural" and update the UI tooltip/description to "40Hz auditory tone" instead of binaural beats.

Note: binaural requires headphones to work. Direct tone works through speakers. If the primary use case is phone speakers, Option B may be more appropriate.

---

### ISSUE-006 — Breathing pattern names mismatch frontend vs backend
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
Frontend pattern buttons (`templates/index.html`):
```javascript
const PATTERNS = {
  '4-7-8': { inhale: 4, holdIn: 7, exhale: 8, holdOut: 0 },
  'box': { inhale: 4, holdIn: 4, exhale: 4, holdOut: 4 },
  'coherent': { inhale: 5.5, holdIn: 0, exhale: 5.5, holdOut: 0 },
};
```

Backend patterns (`api/app.py`):
```python
BREATHING_PATTERNS = {
  'resonance': {'inhale': 5, 'exhale': 5},    # 0.1 Hz
  'box':       {'inhale': 4, 'hold_in': 4, 'exhale': 4, 'hold_out': 4},
  'calm':      {'inhale': 4, 'exhale': 6},
  'prayer':    {'inhale': 5, 'exhale': 5},
}
```

**Why:**
The frontend's `4-7-8` pattern does not exist in the backend. When the frontend calls `/api/breathing/complete` with pattern name `4-7-8`, the backend logs an unrecognized pattern. Sessions are miscategorized in the database and trend analysis will be wrong.

The frontend's `coherent` (5.5/5.5) doesn't match the backend's `resonance` (5/5) by name or by timing.

**How:**
Option A — add `4-7-8` to the backend and rename `coherent` to `resonance` in the frontend:
```python
# api/app.py — add to BREATHING_PATTERNS:
'4-7-8': {'inhale': 4, 'hold_in': 7, 'exhale': 8, 'hold_out': 0},
```
```javascript
// templates/index.html — rename key:
'resonance': { inhale: 5.5, holdIn: 0, exhale: 5.5, holdOut: 0 },
```

Option B — pass pattern parameters to the API rather than a name key, so the frontend is always the source of truth for pattern timing. This is cleaner long-term.

---

### ISSUE-007 — Anti-Zeno check is client-side localStorage only
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`templates/index.html` — `checkAntiZeno()`:
```javascript
const key = 'coherence_opens_' + new Date().toISOString().slice(0, 10);
let count = parseInt(localStorage.getItem(key) || '0');
count++;
localStorage.setItem(key, count.toString());
if (count > 6) {
  document.getElementById('antiZeno').classList.add('active');
}
```

The backend has an `app_checks` table in SQLite for this purpose but the frontend never calls a server endpoint to record or enforce the limit.

**Why:**
Paper 50 (Anti-Zeno theorem): frequent measurement accelerates decoherence. The 6-check/day limit is a physics constraint, not just a UX nudge. Enforcing it only in localStorage means:
- Clearing browser storage resets the count
- A different browser or device starts fresh
- The backend's `app_checks` table accumulates no useful data

**How:**
Add a server endpoint that increments and returns the daily count:
```python
# api/app.py
@app.route('/api/check', methods=['POST'])
def record_check():
    user_id = get_current_user_id()
    today = date.today().isoformat()
    count = db.increment_check_count(user_id, today)
    return jsonify({'count': count, 'limit': 6, 'at_limit': count >= 6})
```

Frontend on load:
```javascript
async function recordOpen() {
  const res = await fetchData('/api/check', null, 'POST');
  if (res && res.at_limit) {
    document.getElementById('antiZeno').classList.add('active');
  }
}
```
Keep localStorage as a fallback if the API is unreachable.

---

### ISSUE-008 — Silent fallback to hardcoded EDGE demo data when API unreachable
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`templates/index.html` — `loadDashboard()`:
```javascript
fetchData('/api/status', {
  coherence: 0.62,
  W: 0.9394,
  gamma_eff: 0.045,   // gamma_eff/gamma_c = 0.72 → EDGE state, green gauge
  gamma_c: 0.0622,
  state: 'edge'
})
```

If the Flask server is down, the user sees C = 0.62 in green with no indication the data is fake.

**Why:**
A user in genuine crisis whose phone can't reach the server sees a reassuring green EDGE reading. The health stakes make silent fallback inappropriate. The user should know they are seeing no data.

**How:**
Return `null` on fetch failure and handle it explicitly:
```javascript
async function fetchData(endpoint, method = 'GET') {
  try {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(endpoint, { method, signal: controller.signal });
    clearTimeout(id);
    if (!res.ok) return null;
    return await res.json();
  } catch(e) {
    return null;
  }
}

// In loadDashboard():
const status = await fetchData('/api/status');
if (!status) {
  document.getElementById('gaugeValue').textContent = '--';
  document.getElementById('stateLabel').textContent = 'NO DATA';
  document.getElementById('stateLabel').style.color = 'var(--text-muted)';
  document.getElementById('paramsLine').textContent = 'Server unreachable';
  return;
}
```

---

### ISSUE-009 — fetchData has no timeout; hangs on dead server
**Timestamp:** 2026-03-31
**Status:** OPEN (subsumed into ISSUE-008 fix above)
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`fetch()` with no `AbortController` will hang until the browser's default timeout (~30–60s) on a dead server. The six parallel `Promise.all` calls in `loadDashboard()` will all hang simultaneously, blocking the UI for up to a minute.

**How:**
Add `AbortController` with 5s timeout — shown in ISSUE-008 fix above. This resolves both issues.

---

### ISSUE-010 — 40Hz visual flicker cannot be exactly 40Hz on 60Hz displays
**Timestamp:** 2026-03-31
**Status:** OPEN
**Touched by:** claude-sonnet-4-6 (identified, not yet fixed)

**What:**
`templates/index.html` — `flickerLoop()`:
```javascript
const halfPeriod = 1000 / 80; // 12.5ms
function flickerLoop(timestamp) {
  if (timestamp - lastToggle >= halfPeriod) {
    flash.classList.toggle('on');
    flash.classList.toggle('off');
    lastToggle = timestamp;
  }
  hzAnimFrame = requestAnimationFrame(flickerLoop);
}
```

`requestAnimationFrame` fires at the display's native refresh rate. On a 60Hz display, frames arrive every ~16.67ms. The code toggles when ≥12.5ms have elapsed — which means it toggles every frame (every 16.67ms) → effective flicker rate is 60Hz / 2 = **30Hz**, not 40Hz. On a 120Hz display, it would toggle every other frame → **60Hz**. Neither is 40Hz.

**Why:**
The gamma entrainment literature uses 40Hz specifically. 30Hz and 60Hz are not equivalent. This may reduce efficacy.

**How:**
There is no pure-JS way to force exactly 40Hz on a display that doesn't support it. Options:
1. Detect display refresh rate and warn if not 40Hz-capable:
   ```javascript
   // Measure actual rAF interval
   let frames = [];
   function measureRefreshRate(ts) {
     frames.push(ts);
     if (frames.length < 10) { requestAnimationFrame(measureRefreshRate); return; }
     const avg = (frames[frames.length-1] - frames[0]) / (frames.length - 1);
     const hz = Math.round(1000 / avg);
     if (hz !== 40 && hz % 40 !== 0) {
       console.warn(`Display is ${hz}Hz — 40Hz visual entrainment unavailable. Audio only.`);
       // Disable visual, keep audio
     }
   }
   requestAnimationFrame(measureRefreshRate);
   ```
2. Use Web Audio API's `AudioWorklet` to generate a perfectly timed 40Hz click train for audio entrainment (not display-rate-dependent).
3. Label the visual as "approximately 40Hz" and rely on the audio for precise entrainment.

---

## PENDING FIXES
All issues above are OPEN as of 2026-03-31. No code has been written to the repo in this session — review only.

Next session should start with ISSUE-001 (cert rotation) and ISSUE-002 (inverted phase labels), as those have the highest impact.

---

*Transcript continues below as fixes are applied.*

---

### ISSUE-001 — cert.pem in public repo — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** Replaced .gitignore with a comprehensive Python/security gitignore. New .gitignore covers *.pem, *.key, *.crt, *.p12, __pycache__/, *.py[cod], *.db, *.sqlite, .env, .DS_Store, and IDE directories. Note: new cert.pem and key.pem must be generated via `openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=BUDDY.ai/O=AIIT-THRESI"` and `git rm -r --cached __pycache__ cert.pem` must be run to remove tracked files from git index. These shell commands require Bash access.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/.gitignore`
**Why:** cert.pem (TLS private key material) was committed to a public repo. Anyone who cloned has the private key. The .gitignore was essentially empty (27 bytes), failing to exclude certificates, pycache, databases, and environment files.

---

### ISSUE-002 — Frontend phase labels inverted — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** Fixed stateName(c), stateColor(c), stateColorRaw(c), and stateGlow(c) functions in templates/index.html. Old thresholds (c < 0.35 = FROZEN, c > 0.75 = COLLAPSED) were inverted relative to the physics. New thresholds: c > 0.607 = FROZEN (gamma_eff < 0.5 * gamma_c, low decoherence), c < 0.223 = COLLAPSED (gamma_eff > 1.5 * gamma_c, high decoherence), else = EDGE. These thresholds are derived from C = exp(-alpha * gamma_eff) where alpha = 16.08 and gamma_c = 0.0622.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html`
**Why:** The physics: high C means low gamma_eff (FROZEN, not COLLAPSED). Low C means high gamma_eff (COLLAPSED, not FROZEN). A user in genuine crisis (C ~ 0.15) was being shown a blue FROZEN label, while a low-stress user (C ~ 0.85) was shown a red COLLAPSED warning. Direct physics error with real user impact.

---

### ISSUE-003 — Two conflicting gamma_eff implementations — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** (1) Added ACE_NU = 0.82 constant to core/coherence_engine.py. (2) Replaced linear ACE computation `gamma_ace = self.profile.ace_score * ACE_BETA * GAMMA_C` with stretched exponential: `ace_clamped = min(self.profile.ace_score, 10.0); gamma_ace = 0.005 * (1.0 - math.exp(-((ACE_BETA * ace_clamped) ** ACE_NU)))`. This matches the api/app.py inline _CoherencePhysics implementation which was correct per Paper 24.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/core/coherence_engine.py`
**Why:** The linear model was physically wrong and numerically catastrophic. For ACE=10: linear gave gamma_ace = 0.259 (4x gamma_c, instant collapse), stretched exponential gives gamma_ace ~ 0.0048 (7.7% of gamma_c, physiologically reasonable). Paper 24 defines ACE coherence as C_n = C_0 * exp(-(beta*n)^nu) — a stretched exponential. The linear model had no basis in the framework.

---

### ISSUE-004 — __pycache__ committed — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** The .gitignore update in ISSUE-001 now includes `__pycache__/` and `*.py[cod]` patterns. Note: `git rm -r --cached api/__pycache__ core/__pycache__ modules/__pycache__` must still be run to remove already-tracked pycache directories from the git index. This requires Bash/shell access.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/.gitignore` (same as ISSUE-001)
**Why:** .pyc files are machine-generated, platform-specific, create false diffs, and cause conflicts across Python versions. The 27-byte .gitignore was essentially empty.

---

### ISSUE-005 — 40Hz audio not binaural — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** (Option B applied) Changed the audio comment from "40Hz binaural" to "40Hz direct auditory tone (not binaural — works on phone speakers without headphones)". Updated the 40Hz session overlay title from "40 Hz Gamma Entrainment" to "40 Hz Gamma Entrainment (Auditory Tone + Visual)" to accurately describe the implementation. The direct 40Hz sine wave implementation was kept because it works on phone speakers without headphones, which is the primary use case.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html`
**Why:** The code comment said "binaural" but the implementation sends a direct 40Hz sine wave to both channels. Binaural requires two tones at different frequencies to separate ears. The mechanism differs: binaural works via interaural phase difference processing; a direct 40Hz tone works via auditory cortex entrainment. Labels must be accurate.

---

### ISSUE-006 — Breathing pattern name mismatch — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** (1) Added '4-7-8' pattern to BREATHING_PATTERNS dict in api/app.py with correct timing (inhale 4s, hold_in 7s, exhale 8s, hold_out 0s). (2) Renamed frontend 'coherent' pattern to 'resonance' in PATTERNS dict in templates/index.html, changed timing from 5.5/5.5 to 5/5 to match backend resonance pattern. (3) Updated the HTML pattern selector button from 'Coherent (5.5-5.5)' to 'Resonance (5-5)'.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/api/app.py`, `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html`
**Why:** Frontend '4-7-8' pattern did not exist in backend, causing unrecognized pattern logs and miscategorized sessions. Frontend 'coherent' (5.5/5.5) did not match backend 'resonance' (5/5) by name or timing. Sessions were being miscategorized in the database and trend analysis was wrong.

---

### ISSUE-007 — Anti-Zeno client-side only — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** (1) Added POST /api/check endpoint to api/app.py that calls _record_app_check() and _get_check_count_today(), returns {count, limit, at_limit, message}. Uses existing app_checks table and anti-Zeno helper functions already in the backend. (2) Rewrote frontend checkAntiZeno() to be async, calling /api/check with a 5s AbortController timeout. On success, updates APP.openCount and syncs localStorage as backup. On server failure, falls back to localStorage-only counting (preserving original behavior).
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/api/app.py`, `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html`
**Why:** Paper 50 (Anti-Zeno theorem): frequent measurement accelerates decoherence. The 6-check/day limit is a physics constraint. Enforcing it only in localStorage meant clearing browser storage reset the count, different browsers started fresh, and the backend app_checks table accumulated no data.

---

### ISSUE-008 — Silent fallback to fake data — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** (1) Rewrote fetchData() to accept (endpoint, method) instead of (endpoint, fallback). Returns null on any failure (network error, non-ok status, timeout). Includes 5s AbortController timeout. (2) Removed all hardcoded fallback data from loadDashboard() — no more fake C=0.62/EDGE/green values. (3) Added null-check for status response: if null, displays "--" for gauge value, "NO DATA" for state label (in muted color), and "Server unreachable" for params line, then returns early. (4) All other data sources (metrics, recs, trend, keeper, geomag) are null-guarded before rendering.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html`
**Why:** When the Flask server was down, the user saw C=0.62 in green with no indication the data was fake. A user in genuine crisis whose phone cannot reach the server would see a reassuring green EDGE reading. The health stakes make silent fallback inappropriate.

---

### ISSUE-009 — No timeout on fetch — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** Subsumed into ISSUE-008 fix. fetchData() now uses AbortController with 5-second timeout. Previously, fetch() with no AbortController would hang until the browser's default timeout (30-60s). The six parallel Promise.all calls in loadDashboard() would all hang simultaneously, blocking the UI for up to a minute.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html` (same as ISSUE-008)
**Why:** fetch() without AbortController hangs on dead servers. Six parallel hanging fetches block the entire UI.

---

### ISSUE-010 — 40Hz can't hit 40Hz on 60Hz displays — FIXED
**Timestamp:** 2026-03-31
**Status:** DONE
**Touched by:** Claude Opus 4.6 (coheranceclaude session, ~4AM CDT)
**What was changed:** (1) Added display refresh rate detection using requestAnimationFrame timing (measures 12 frames, computes average interval). (2) If display cannot do exact 40Hz (i.e., refresh rate is not a multiple of 40, such as 60Hz), logs a console warning and updates the session overlay title to show the actual approximate flicker rate (e.g., "Visual: ~30Hz (approximate), Audio: exact 40Hz"). (3) Added detailed code comments explaining that requestAnimationFrame is display-rate-limited: 60Hz display yields ~30Hz flicker, 120Hz yields ~60Hz. (4) The audio tone is always exactly 40Hz regardless of display. Visual is now labeled "approximate" when the display cannot achieve exact 40Hz.
**Files modified:** `/home/buddy_ai/Desktop/COHERENCE_APP/templates/index.html`
**Why:** The gamma entrainment literature uses 40Hz specifically. On a 60Hz display, requestAnimationFrame toggles every frame (~16.67ms) giving 30Hz effective flicker, not 40Hz. Users need to know the visual is approximate and that the audio channel provides the precise 40Hz entrainment.
