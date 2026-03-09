#!/usr/bin/env python3
import os

OUTPUT_DIR = "/home/claude/opcg"

SETS = [
  ("op01","OP-01","ROMANCE DAWN",             121),
  ("op02","OP-02","Paramount War",            121),
  ("op03","OP-03","Pillars of Strength",      121),
  ("op04","OP-04","Kingdoms of Intrigue",     121),
  ("op05","OP-05","Awakening of the New Era", 122),
  ("op06","OP-06","Wings of the Captain",     120),
  ("op07","OP-07","500 Years in the Future",  121),
  ("op08","OP-08","Two Legends",              121),
  ("op09","OP-09","Emperors in the New World",124),
  ("op10","OP-10","Royal Blood",              121),
  ("op11","OP-11","A Fist of Divine Speed",   122),
  ("op12","OP-12","Legacy of the Master",     122),
  ("op13","OP-13","Carrying on His Will",     122),
  ("op14","OP-14","The Azure Sea's Seven",    125),
  ("op15","OP-15","Adventure on KAMI's Island",122),
]

# OP-01 price data from yuyu-tei (internal yuyu ID -> price JPY)
OP01_PRICES = {
  # P-SEC
  "OP01-120_psec_parallel": (3980, False),
  "OP01-120_psec_super_parallel": (128000, False),
  "OP01-121_psec_parallel": (3980, True),
  # SEC
  "OP01-120_sec": (220, False),
  "OP01-121_sec": (220, False),
  # P-SR
  "OP01-024_psr": (2980, False),
  "OP01-025_psr": (3980, True),
  "OP01-040_psr": (580, True),
  "OP01-047_psr": (1480, True),
  "OP01-051_psr": (1280, True),
  "OP01-067_psr": (780, False),
  "OP01-070_psr": (980, False),
  "OP01-078_psr": (4980, True),
  "OP01-094_psr": (780, False),
  "OP01-096_psr": (780, True),
  # SR
  "OP01-024_sr": (120, True),
  "OP01-025_sr": (220, True),
  "OP01-040_sr": (80, True),
  "OP01-047_sr": (120, True),
  "OP01-051_sr": (120, True),
  "OP01-067_sr": (80, True),
  "OP01-070_sr": (80, True),
  "OP01-078_sr": (120, True),
  "OP01-094_sr": (120, True),
  "OP01-096_sr": (120, True),
  # P-R
  "OP01-013_pr": (1980, True),
  "OP01-016_pr": (14800, True),
  "OP01-073_pr": (1480, True),
  "OP01-093_pr": (580, True),
  "OP01-097_pr": (580, True),
  "OP01-102_pr": (580, True),
  # R
  "OP01-004_r": (80, True),
  "OP01-005_r": (80, True),
  "OP01-013_r": (120, True),
  "OP01-016_r": (220, True),
  "OP01-017_r": (80, True),
  "OP01-026_r": (120, True),
  "OP01-035_r": (80, True),
  "OP01-041_r": (80, True),
  "OP01-046_r": (80, True),
  "OP01-049_r": (80, True),
  "OP01-054_r": (80, True),
  "OP01-058_r": (120, True),
  "OP01-068_r": (80, True),
  "OP01-069_r": (80, True),
  "OP01-071_r": (80, True),
  "OP01-073_r": (80, True),
  "OP01-074_r": (80, True),
  "OP01-079_r": (80, True),
  "OP01-086_r": (80, True),
  "OP01-093_r": (120, True),
  "OP01-097_r": (80, True),
  "OP01-102_r": (80, True),
  "OP01-111_r": (80, True),
  "OP01-112_r": (80, True),
  "OP01-114_r": (80, True),
  "OP01-119_r": (180, True),
}

# Simplified per-card price mapping: card_id -> lowest price (JPY), in_stock
OP01_CARD_PRICES = {
  "OP01-001": (None, True),
  "OP01-002": (None, True),
  "OP01-003": (None, True),
  "OP01-004": (80, True),
  "OP01-005": (80, True),
  "OP01-006": (120, True),
  "OP01-007": (30, True),
  "OP01-008": (30, True),
  "OP01-009": (30, True),
  "OP01-010": (30, True),
  "OP01-011": (80, True),
  "OP01-012": (30, True),
  "OP01-013": (120, True),
  "OP01-014": (80, True),
  "OP01-015": (80, True),
  "OP01-016": (220, True),
  "OP01-017": (80, True),
  "OP01-018": (30, True),
  "OP01-019": (80, True),
  "OP01-020": (30, True),
  "OP01-021": (80, True),
  "OP01-022": (80, True),
  "OP01-023": (30, True),
  "OP01-024": (120, True),
  "OP01-025": (220, True),
  "OP01-026": (120, True),
  "OP01-027": (80, True),
  "OP01-028": (30, True),
  "OP01-029": (80, True),
  "OP01-030": (80, True),
  "OP01-032": (80, True),
  "OP01-033": (80, True),
  "OP01-034": (30, True),
  "OP01-035": (80, True),
  "OP01-036": (30, True),
  "OP01-037": (30, True),
  "OP01-038": (30, True),
  "OP01-039": (80, True),
  "OP01-040": (80, True),
  "OP01-041": (80, True),
  "OP01-042": (80, True),
  "OP01-043": (80, True),
  "OP01-044": (80, True),
  "OP01-045": (30, True),
  "OP01-046": (80, True),
  "OP01-047": (120, True),
  "OP01-048": (30, True),
  "OP01-049": (80, True),
  "OP01-050": (80, True),
  "OP01-051": (120, True),
  "OP01-052": (80, True),
  "OP01-053": (30, True),
  "OP01-054": (80, True),
  "OP01-055": (80, True),
  "OP01-056": (80, True),
  "OP01-057": (180, True),
  "OP01-058": (120, True),
  "OP01-059": (30, True),
  "OP01-063": (80, True),
  "OP01-064": (30, True),
  "OP01-065": (30, True),
  "OP01-066": (80, True),
  "OP01-067": (80, True),
  "OP01-068": (80, True),
  "OP01-069": (80, True),
  "OP01-070": (80, True),
  "OP01-071": (80, True),
  "OP01-072": (30, True),
  "OP01-073": (80, True),
  "OP01-074": (80, True),
  "OP01-075": (80, True),
  "OP01-076": (30, True),
  "OP01-077": (80, True),
  "OP01-078": (120, True),
  "OP01-079": (80, True),
  "OP01-080": (30, True),
  "OP01-081": (30, True),
  "OP01-082": (30, True),
  "OP01-083": (80, True),
  "OP01-084": (80, True),
  "OP01-085": (80, True),
  "OP01-086": (80, True),
  "OP01-087": (30, True),
  "OP01-088": (80, True),
  "OP01-089": (30, True),
  "OP01-090": (80, True),
  "OP01-092": (80, True),
  "OP01-093": (120, True),
  "OP01-094": (120, True),
  "OP01-095": (80, True),
  "OP01-096": (120, True),
  "OP01-097": (80, True),
  "OP01-098": (80, True),
  "OP01-099": (30, True),
  "OP01-100": (80, True),
  "OP01-101": (80, True),
  "OP01-102": (80, True),
  "OP01-103": (30, True),
  "OP01-106": (80, True),
  "OP01-108": (80, True),
  "OP01-109": (80, True),
  "OP01-111": (80, True),
  "OP01-112": (80, True),
  "OP01-114": (80, True),
  "OP01-116": (80, True),
  "OP01-118": (80, True),
  "OP01-119": (180, True),
  "OP01-120": (220, False),
  "OP01-121": (220, False),
}

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+Thai:wght@300;400;600;700&display=swap');
:root {
  --gold: #c9a84c;
  --gold-light: #f0d080;
  --dark: #0a0a0a;
  --dark2: #141414;
  --dark3: #1c1c1c;
  --dark4: #222;
  --red: #e83333;
  --text: #e8e0d0;
  --text-dim: #777;
  --border: #2a2a2a;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--dark); color: var(--text); font-family: 'Noto Sans Thai', sans-serif; min-height: 100vh; }

/* ── NAV ── */
.topbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  background: rgba(10,10,10,0.96);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  height: 52px;
  display: flex; align-items: center; gap: 0;
  padding: 0 16px;
  overflow-x: auto;
  scrollbar-width: none;
}
.topbar::-webkit-scrollbar { display: none; }
.topbar-brand {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.25rem;
  color: var(--gold);
  letter-spacing: 0.1em;
  white-space: nowrap;
  margin-right: 20px;
  text-decoration: none;
  flex-shrink: 0;
}
.nav-sep { width: 1px; height: 24px; background: #2a2a2a; margin: 0 6px; flex-shrink: 0; }
.nav-btn {
  display: flex; align-items: center; gap: 5px;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.72rem;
  font-family: 'Noto Sans Thai', sans-serif;
  color: var(--text-dim);
  text-decoration: none;
  white-space: nowrap;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s;
  border: 1px solid transparent;
}
.nav-btn:hover { background: rgba(201,168,76,0.1); color: var(--gold-light); border-color: rgba(201,168,76,0.3); }
.nav-btn.active { background: rgba(201,168,76,0.15); color: var(--gold); border-color: var(--gold); }
.nav-btn .dot {
  width: 6px; height: 6px; border-radius: 50%; background: currentColor; flex-shrink: 0;
}

/* ── PAGE HEADER ── */
.page-header {
  margin-top: 52px;
  padding: 28px 24px 20px;
  background: linear-gradient(180deg, #111 0%, var(--dark) 100%);
  border-bottom: 1px solid var(--border);
}
.page-header-inner { max-width: 1400px; margin: 0 auto; display: flex; align-items: flex-end; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.set-label { font-family: 'Bebas Neue', sans-serif; font-size: 0.9rem; color: var(--text-dim); letter-spacing: 0.2em; }
.set-title { font-family: 'Bebas Neue', sans-serif; font-size: clamp(1.8rem, 4vw, 3rem); letter-spacing: 0.06em;
  background: linear-gradient(135deg, var(--gold), var(--gold-light));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1; margin-top: 2px;
}
.set-meta { font-size: 0.78rem; color: var(--text-dim); margin-top: 6px; }
.rate-pill { display: inline-block; background: rgba(201,168,76,0.12); border: 1px solid rgba(201,168,76,0.4); border-radius: 20px; padding: 3px 10px; font-size: 0.72rem; color: var(--gold-light); }

/* ── FILTER ── */
.filter-wrap { max-width: 1400px; margin: 0 auto; padding: 10px 24px; display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.filter-label-txt { font-size: 0.72rem; color: var(--text-dim); }
.filter-btn {
  padding: 3px 10px; border-radius: 12px; border: 1px solid #2a2a2a;
  background: transparent; color: var(--text-dim); font-size: 0.7rem;
  cursor: pointer; font-family: 'Noto Sans Thai', sans-serif;
  transition: all 0.15s;
}
.filter-btn:hover { border-color: var(--gold); color: var(--gold-light); background: rgba(201,168,76,0.1); }
.filter-btn.on { border-color: var(--gold); color: var(--gold); background: rgba(201,168,76,0.12); }
.filter-divider { width: 1px; height: 16px; background: #2a2a2a; }

/* ── GRID ── */
.content { max-width: 1400px; margin: 0 auto; padding: 0 24px 60px; }
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
}

/* ── CARD ── */
.card-item {
  background: var(--dark3);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.18s, border-color 0.18s, box-shadow 0.18s;
  position: relative;
}
.card-item:hover { transform: translateY(-3px); border-color: var(--gold); box-shadow: 0 6px 20px rgba(0,0,0,0.5); }
.card-img-wrap { position: relative; aspect-ratio: 5/7; background: #111; overflow: hidden; }
.card-img-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; transition: opacity 0.3s; }
.card-img-wrap img.loading { opacity: 0; }
.card-img-wrap img.loaded { opacity: 1; }
.card-num-badge {
  position: absolute; bottom: 5px; left: 5px;
  background: rgba(0,0,0,0.75); backdrop-filter: blur(4px);
  border-radius: 3px; padding: 1px 5px;
  font-size: 0.6rem; color: #aaa; font-family: monospace;
}
.rarity-pip {
  position: absolute; top: 5px; right: 5px;
  width: 7px; height: 7px; border-radius: 50%;
}
.card-info { padding: 6px 8px 8px; }
.card-price-jpy { font-size: 0.88rem; font-weight: 700; color: var(--gold-light); }
.card-price-thb { font-size: 0.72rem; color: #999; }
.no-price { font-size: 0.7rem; color: #555; }
.out-of-stock { font-size: 0.65rem; color: var(--red); margin-top: 2px; }

/* rarity colors */
.pip-psec { background:#ff3333; box-shadow:0 0 5px #ff3333; }
.pip-sec  { background:#ff8c00; box-shadow:0 0 5px #ff8c00; }
.pip-psr  { background:#c9a84c; box-shadow:0 0 4px #c9a84c; }
.pip-sr   { background:#c0c0c0; box-shadow:0 0 4px #c0c0c0; }
.pip-pr   { background:#7ab8ff; box-shadow:0 0 4px #7ab8ff; }
.pip-r    { background:#4d9fff; }
.pip-puc  { background:#c47aff; box-shadow:0 0 3px #c47aff; }
.pip-uc   { background:#9955dd; }
.pip-pc   { background:#66cc66; }
.pip-c    { background:#555; }

.card-item.has-price:hover { border-color: var(--gold-light); }
.card-item.no-stock-item { opacity: 0.6; }

/* link overlay */
.card-link { position: absolute; inset: 0; z-index: 2; }

/* view toggle */
.view-toggle { display: flex; gap: 6px; }
.view-btn { padding: 3px 10px; border-radius: 4px; border: 1px solid #2a2a2a; background: transparent; color: var(--text-dim); font-size: 0.7rem; cursor: pointer; font-family: 'Noto Sans Thai', sans-serif; transition: all 0.15s; }
.view-btn.on { border-color: #555; color: var(--text); background: #222; }

/* big grid mode */
.cards-grid.big { grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 14px; }
.cards-grid.small { grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 6px; }
.cards-grid.small .card-info { padding: 4px 6px 6px; }
.cards-grid.small .card-price-jpy { font-size: 0.78rem; }

/* count badge */
.count-badge { font-size: 0.75rem; color: var(--text-dim); margin-left: auto; }

/* footer */
.page-footer { text-align: center; font-size: 0.68rem; color: #444; padding: 20px; border-top: 1px solid #1a1a1a; }
.page-footer a { color: #666; }
</style>
"""

NAV_ITEMS = "".join([
    f'<a class="nav-btn" href="{sid}.html" id="nav-{sid}"><span class="dot"></span>{slabel}</a>'
    for (sid, slabel, _, _) in SETS
])

def make_nav(current_id):
    items = []
    for (sid, slabel, sname, _) in SETS:
        active = ' active' if sid == current_id else ''
        items.append(f'<a class="nav-btn{active}" href="{sid}.html" id="nav-{sid}"><span class="dot"></span>{slabel}</a>')
    return f'''<nav class="topbar">
  <a class="topbar-brand" href="index.html">⚓ OPCG</a>
  <div class="nav-sep"></div>
  {"".join(items)}
</nav>'''

# ── OP02 prices (SEC/P-SEC/P-SR only — key highlights) ──────────────────────
OP02_CARD_PRICES = {
  # P-SEC
  "OP02-120": (2480, True),   # Uta Parallel
  "OP02-121": (980, False),   # Kuzan Parallel
  # SEC
  "OP02-120_sec": (420, False),
  "OP02-121_sec": (320, True),
  # P-SR
  "OP02-004": (1280, True),   # Newgate P
  "OP02-013": (2980, False),  # Ace P
  "OP02-030": (580, True),    # Oden P
  "OP02-036": (2480, False),  # Nami P
  "OP02-051": (580, True),    # Ivankov P
  "OP02-062": (1980, False),  # Luffy P
  "OP02-085": (980, False),   # Magellan P
  "OP02-096": (980, False),   # Kuzan P
  "OP02-099": (580, True),    # Sakazuki P
  "OP02-114": (780, True),    # Borsalino P
}

# ── OP03 prices ──────────────────────────────────────────────────────────────
OP03_CARD_PRICES = {
  # P-SEC
  "OP03-122": (780, False),   # Sogeking P
  "OP03-123": (1280, False),  # Katakuri P
  # SEC
  "OP03-122_sec": (320, True),
  "OP03-123_sec": (320, True),
  # P-SR
  "OP03-013": (780, True),    # Marco P
  "OP03-025": (580, True),    # Creek P
  "OP03-041": (580, True),    # Usopp P
  "OP03-066": (580, True),    # Paulie P
  "OP03-078": (780, True),    # Issho P
  "OP03-080": (580, False),   # Kaku P
  "OP03-092": (580, True),    # Rob Lucci P
  "OP03-108": (580, True),    # Cracker P
  "OP03-113": (580, True),    # Perospero P
  "OP03-114": (1480, True),   # Big Mom P
}

# ── OP04 prices ──────────────────────────────────────────────────────────────
OP04_CARD_PRICES = {
  # P-SEC
  "OP04-118": (1280, False),  # Vivi P (OOS)
  "OP04-119": (780, True),    # Rosinante P
  # SEC
  "OP04-118_sec": (500, False),
  "OP04-119_sec": (320, True),
  # P-SR
  "OP04-013": (580, True),    # Pell P
  "OP04-024": (580, False),   # Sugar P
  "OP04-031": (580, True),    # Doflamingo P
  "OP04-044": (580, True),    # Kaido P
  "OP04-060": (580, True),    # Crocodile P
  "OP04-064": (980, False),   # Miss All Sunday P
  "OP04-083": (1780, True),   # Sabo P
  "OP04-090": (1480, True),   # Luffy P
  "OP04-104": (580, True),    # Sanji P
  "OP04-112": (780, True),    # Yamato P
}

# ── OP05 prices ──────────────────────────────────────────────────────────────
OP05_CARD_PRICES = {
  # P-SEC
  "OP05-118": (780, True),    # Kaido P
  "OP05-119": (14800, True),  # Luffy P
  # SEC
  "OP05-118_sec": (320, True),
  "OP05-119_sec": (580, True),
  # P-SR
  "OP05-006": (580, False),   # Koala P
  "OP05-007": (580, True),    # Sabo P
  "OP05-032": (580, True),    # Pica P
  "OP05-043": (580, True),    # Ulti P
  "OP05-051": (580, True),    # Borsalino P
  "OP05-069": (780, True),    # Law P
  "OP05-074": (780, True),    # Kid P
  "OP05-091": (580, True),    # Rebecca P
  "OP05-098": (580, True),    # Nami P (est)
  "OP05-107": (780, True),    # Luffy P (est)
}

# ── OP06 prices ──────────────────────────────────────────────────────────────
OP06_CARD_PRICES = {
  # P-SEC
  "OP06-118": (5980, False),  # Zoro P
  "OP06-119": (1980, True),   # Sanji P
  # SEC
  "OP06-118_sec": (680, True),
  "OP06-119_sec": (320, True),
  # P-SR
  "OP06-007": (1780, True),   # Shanks P
  "OP06-009": (780, True),    # Shuraiya P
  "OP06-035": (980, True),    # Hody P
  "OP06-043": (580, True),    # Aramaki P
  "OP06-062": (580, True),    # Judge P
  "OP06-069": (1280, True),   # Reiju P
  "OP06-086": (980, False),   # Moria P
  "OP06-093": (1980, True),   # Perona P
  "OP06-106": (1980, True),   # Hiyori P
  "OP06-107": (780, True),    # Momonosuke P
}

# ── OP07 prices ──────────────────────────────────────────────────────────────
OP07_CARD_PRICES = {
  # P-SEC
  "OP07-118": (780, False),   # Sabo P
  "OP07-119": (1280, False),  # Ace P
  # SEC
  "OP07-118_sec": (220, True),
  "OP07-119_sec": (420, True),
  # P-SR
  "OP07-015": (780, True),    # Dragon P
  "OP07-026": (1780, True),   # Bonney P
  "OP07-029": (580, True),    # Hawkins P
  "OP07-045": (500, True),    # Jinbei P
  "OP07-051": (2980, True),   # Hancock P
  "OP07-064": (1280, True),   # Sanji P
  "OP07-072": (780, True),    # Porche P
  "OP07-085": (1480, True),   # Stussy P
  "OP07-109": (2480, True),   # Luffy P
  "OP07-111": (780, True),    # Lilith P
}

# ── OP08 prices ──────────────────────────────────────────────────────────────
OP08_CARD_PRICES = {
  # P-SEC
  "OP08-118": (1480, True),   # Rayleigh P
  "OP08-119": (580, False),   # Kaido&Linlin P
  # SEC
  "OP08-118_sec": (580, True),
  "OP08-119_sec": (220, True),
  # P-SR
  "OP08-007": (980, True),    # Chopper P
  "OP08-023": (1280, True),   # Carrot P
  "OP08-043": (780, True),    # Newgate P
  "OP08-069": (500, False),   # Linlin P
  "OP08-074": (980, True),    # Black Maria P
  "OP08-079": (580, True),    # Kaido P
  "OP08-084": (780, True),    # Jack P
  "OP08-105": (980, True),    # Bonney P
  "OP08-106": (1980, True),   # Nami P
  "OP08-112": (780, True),    # S-Snake P
}

# ── OP09 prices ──────────────────────────────────────────────────────────────
OP09_CARD_PRICES = {
  # P-SEC
  "OP09-118": (2480, False),  # Roger P
  "OP09-119": (1480, True),   # Luffy P
  # SEC
  "OP09-118_sec": (680, True),
  "OP09-119_sec": (780, True),
  # P-SR
  "OP09-004": (1280, True),   # Shanks P
  "OP09-009": (780, True),    # Benn Beckman P
  "OP09-023": (580, True),    # Adio P
  "OP09-037": (580, True),    # Rim P
  "OP09-046": (580, True),    # Crocodile P
  "OP09-048": (580, True),    # Mihawk P
  "OP09-065": (580, True),    # Sanji P
  "OP09-079": (780, True),    # Nami P (est)
  "OP09-099": (780, True),    # Luffy P (est)
  "OP09-112": (780, True),    # Coby P (est)
}

# ── OP10 prices ──────────────────────────────────────────────────────────────
OP10_CARD_PRICES = {
  # P-SEC
  "OP10-118": (2480, True),   # Luffy P
  "OP10-119": (1980, True),   # Law P
  # SEC
  "OP10-118_sec": (580, True),
  "OP10-119_sec": (220, False),
  # P-SR
  "OP10-005": (1280, True),   # Sanji P
  "OP10-016": (780, True),    # Monet P
  "OP10-030": (980, True),    # Smoker P
  "OP10-032": (1480, True),   # Tashigi P
  "OP10-046": (780, True),    # Kyros P
  "OP10-058": (780, False),   # Rebecca P
  "OP10-071": (1980, True),   # Doflamingo P
  "OP10-072": (1780, True),   # Rosinante P
  "OP10-082": (1280, True),   # Kuzan P
  "OP10-112": (980, True),    # Kid P
}

# ── OP11 prices ──────────────────────────────────────────────────────────────
OP11_CARD_PRICES = {
  # P-SEC
  "OP11-118": (1780, True),   # Luffy P
  "OP11-119": (980, True),    # Coby P
  # SEC
  "OP11-118_sec": (780, True),
  "OP11-119_sec": (320, True),
  # P-SR
  "OP11-004": (1480, True),   # Kujaku P
  "OP11-010": (780, True),    # Hibari P
  "OP11-031": (580, True),    # Jinbei P
  "OP11-051": (780, True),    # Sanji P
  "OP11-054": (2980, True),   # Nami P
  "OP11-067": (1280, True),   # Katakuri P
  "OP11-070": (780, True),    # Pudding P
  "OP11-092": (1480, True),   # Helmeppo P
  "OP11-095": (580, True),    # Garp P
  "OP11-101": (780, True),    # Bege P
}

# ── OP12 prices ──────────────────────────────────────────────────────────────
OP12_CARD_PRICES = {
  # P-SEC
  "OP12-118": (2480, True),   # Bonney P
  "OP12-119": (4980, True),   # Kuma P
  # SEC
  "OP12-118_sec": (1480, True),
  "OP12-119_sec": (3980, True),
  # P-SR
  "OP12-014": (1780, True),   # Hancock P
  "OP12-015": (1280, True),   # Luffy P
  "OP12-030": (1480, True),   # Mihawk P
  "OP12-034": (3480, True),   # Perona P
  "OP12-056": (1280, True),   # Garp P
  "OP12-063": (1280, True),   # Reiju P
  "OP12-073": (1780, True),   # Law P
  "OP12-087": (1480, True),   # Robin P
  "OP12-094": (1280, True),   # Dragon P
}

# ── OP13 prices ──────────────────────────────────────────────────────────────
OP13_CARD_PRICES = {
  # P-SEC
  "OP13-118": (5980, False),  # Luffy P
  "OP13-119": (1480, True),   # Ace P
  "OP13-120": (1780, False),  # Sabo P
  # SEC
  "OP13-118_sec": (780, True),
  "OP13-119_sec": (500, True),
  "OP13-120_sec": (420, True),
  # P-SR
  "OP13-007": (1780, False),  # Ace&Sabo&Luffy P
  "OP13-023": (980, True),    # Uta P
  "OP13-035": (780, True),    # Nami P (est)
  "OP13-052": (980, True),    # Luffy P (est)
  "OP13-070": (780, True),    # Sanji P (est)
  "OP13-089": (780, True),    # Zoro P (est)
}

# ── OP14 prices ──────────────────────────────────────────────────────────────
OP14_CARD_PRICES = {
  # P-SEC
  "OP14-119": (2480, False),  # Mihawk P
  "OP14-120": (2980, True),   # Crocodile P
  # SEC
  "OP14-119_sec": (1480, True),
  "OP14-120_sec": (1480, True),
  # P-SR
  "OP14-009": (980, True),    # Law P
  "OP14-013": (980, False),   # Luffy P
  "OP14-031": (3480, True),   # Nami P
  "OP14-033": (3480, True),   # Perona P
  "OP14-049": (1280, True),   # Jinbei P
  "OP14-069": (2480, True),   # Doflamingo P
  "OP14-084": (2480, True),   # Miss All Sunday P
  "OP14-091": (1480, True),   # Mr.2 P
  "OP14-104": (1280, True),   # Moria P
}

# ── OP15 prices ──────────────────────────────────────────────────────────────
OP15_CARD_PRICES = {
  # P-SEC
  "OP15-118": (7980, False),  # Enel P
  "OP15-119": (9980, True),   # Luffy P
  # SEC
  "OP15-118_sec": (4980, True),
  "OP15-119_sec": (3980, True),
  # P-SR
  "OP15-007": (980, True),    # Gin P
  "OP15-008": (1280, True),   # Creek P
  "OP15-032": (1980, True),   # Brook P
  "OP15-046": (1980, True),   # Sabo P
  "OP15-053": (2980, True),   # Rebecca P
  "OP15-060": (4980, False),  # Enel P-SR
  "OP15-078": (4980, False),  # Manerva P
  "OP15-086": (7980, False),  # Nami P
  "OP15-113": (9980, True),   # Zoro P
  "OP15-114": (1280, True),   # Wiper P
}

ALL_PRICES = {
  "op01": OP01_CARD_PRICES,
  "op02": OP02_CARD_PRICES,
  "op03": OP03_CARD_PRICES,
  "op04": OP04_CARD_PRICES,
  "op05": OP05_CARD_PRICES,
  "op06": OP06_CARD_PRICES,
  "op07": OP07_CARD_PRICES,
  "op08": OP08_CARD_PRICES,
  "op09": OP09_CARD_PRICES,
  "op10": OP10_CARD_PRICES,
  "op11": OP11_CARD_PRICES,
  "op12": OP12_CARD_PRICES,
  "op13": OP13_CARD_PRICES,
  "op14": OP14_CARD_PRICES,
  "op15": OP15_CARD_PRICES,
}

def make_price_js(set_id):
    prices = ALL_PRICES.get(set_id, {})
    if not prices:
        return "const PRICES = {};"
    lines = []
    for card_id, (jpy, stock) in prices.items():
        if jpy:
            thb = round(jpy * 0.2011)
            lines.append(f'  "{card_id}": {{jpy:{jpy},thb:{thb},stock:{str(stock).lower()}}}')
    return "const PRICES = {\n" + ",\n".join(lines) + "\n};"

def make_set_page(set_id, set_label, set_name, total):
    set_upper = set_id.upper()  # OP01
    set_hyphen = set_label       # OP-01
    yuyu_code = set_id           # op01

    price_js = make_price_js(set_id)

    has_prices = set_id in ALL_PRICES and len(ALL_PRICES[set_id]) > 0
    price_note = "ราคาการ์ดหายากจาก yuyu-tei.jp (มี.ค. 2569)" if has_prices else "คลิกการ์ดเพื่อดูราคาที่ yuyu-tei.jp"

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{set_hyphen} {set_name} — OPCG Price List</title>
{SHARED_CSS}
</head>
<body>

{make_nav(set_id)}

<div class="page-header">
  <div class="page-header-inner">
    <div>
      <div class="set-label">{set_hyphen} · ONE PIECE CARD GAME</div>
      <div class="set-title">{set_name}</div>
      <div class="set-meta">{total} การ์ด (numbered) · <span class="rate-pill">100 ¥ = 20.11 ฿</span></div>
    </div>
  </div>
</div>

<div style="background:var(--dark2); border-bottom:1px solid var(--border);">
  <div class="filter-wrap">
    <span class="filter-label-txt">ขนาด:</span>
    <button class="view-btn" onclick="setSize('small')">เล็ก</button>
    <button class="view-btn on" onclick="setSize('normal')">ปกติ</button>
    <button class="view-btn" onclick="setSize('big')">ใหญ่</button>
    <div class="filter-divider"></div>
    <span class="filter-label-txt">{price_note}</span>
    <span class="count-badge" id="count-badge"></span>
  </div>
</div>

<div class="content" style="padding-top:16px;">
  <div class="cards-grid" id="cards-grid"></div>
</div>

<footer class="page-footer">
  รูปภาพจาก <a href="https://asia-th.onepiece-cardgame.com" target="_blank">onepiece-cardgame.com</a> ·
  ราคาจาก <a href="https://yuyu-tei.jp/sell/opc/s/{yuyu_code}" target="_blank">yuyu-tei.jp</a>
</footer>

<script>
const SET_ID = "{set_upper}";
const TOTAL = {total};
const RATE = 0.2011;
{price_js}

function imgUrl(num) {{
  const n = String(num).padStart(3,'0');
  return `https://asia-th.onepiece-cardgame.com/images/cardlist/card/${{SET_ID}}-${{n}}.png?240426`;
}}

function yuyuUrl(num) {{
  const n = String(num).padStart(3,'0');
  return `https://yuyu-tei.jp/sell/opc/s/{yuyu_code}`;
}}

function buildGrid() {{
  const grid = document.getElementById('cards-grid');
  let html = '';
  for (let i = 1; i <= TOTAL; i++) {{
    const num = String(i).padStart(3,'0');
    const cardId = `${{SET_ID}}-${{num}}`;
    const pData = PRICES[cardId];
    let priceHtml = '';
    let stockClass = '';
    let hasPrice = '';
    if (pData) {{
      hasPrice = ' has-price';
      if (!pData.stock) stockClass = ' no-stock-item';
      priceHtml = `<div class="card-price-jpy">¥${{pData.jpy.toLocaleString()}}</div>
        <div class="card-price-thb">฿${{pData.thb.toLocaleString()}}</div>
        ${{!pData.stock ? '<div class="out-of-stock">หมดสต็อก</div>' : ''}}`;
    }} else {{
      priceHtml = `<div class="no-price">ดูราคา →</div>`;
    }}
    html += `<div class="card-item${{hasPrice}}${{stockClass}}">
      <a class="card-link" href="https://yuyu-tei.jp/sell/opc/s/{yuyu_code}" target="_blank" title="${{cardId}}"></a>
      <div class="card-img-wrap">
        <img src="${{imgUrl(i)}}" alt="${{cardId}}" loading="lazy"
          onload="this.classList.add('loaded')" onerror="this.style.opacity=0.15">
        <div class="card-num-badge">${{cardId}}</div>
      </div>
      <div class="card-info">${{priceHtml}}</div>
    </div>`;
  }}
  grid.innerHTML = html;
  document.getElementById('count-badge').textContent = TOTAL + ' การ์ด';
}}

function setSize(s) {{
  const grid = document.getElementById('cards-grid');
  grid.className = 'cards-grid';
  if (s !== 'normal') grid.classList.add(s);
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('on'));
  event.target.classList.add('on');
}}

buildGrid();
</script>
</body>
</html>"""


def make_index():
    cards_html = ""
    for (sid, slabel, sname, total) in SETS:
        cards_html += f"""
    <a class="set-card" href="{sid}.html">
      <div class="set-card-label">{slabel}</div>
      <div class="set-card-name">{sname}</div>
      <div class="set-card-meta">{total} การ์ด</div>
      <div class="set-card-arrow">→</div>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ONE PIECE CARD GAME — ราคาการ์ด</title>
{SHARED_CSS}
<style>
.hero {{
  margin-top: 52px;
  padding: 60px 24px 40px;
  text-align: center;
  background: radial-gradient(ellipse at 50% 0%, #1a0f00 0%, var(--dark) 70%);
  border-bottom: 1px solid var(--border);
}}
.hero-title {{
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(2.5rem, 8vw, 5rem);
  letter-spacing: 0.1em;
  background: linear-gradient(135deg, #c9a84c, #f0d080, #c9a84c);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1;
}}
.hero-sub {{ font-size: 0.9rem; color: var(--text-dim); margin-top: 10px; }}
.hero-rate {{ display: inline-block; margin-top: 12px; background: rgba(201,168,76,0.12); border: 1px solid rgba(201,168,76,0.35); border-radius: 20px; padding: 4px 14px; font-size: 0.78rem; color: var(--gold-light); }}

.sets-grid {{
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 24px 60px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}}
.set-card {{
  background: var(--dark3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 16px;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: transform 0.18s, border-color 0.18s, background 0.18s;
  position: relative;
  overflow: hidden;
}}
.set-card::before {{
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  opacity: 0;
  transition: opacity 0.18s;
}}
.set-card:hover {{ transform: translateY(-3px); border-color: var(--gold); background: #222; }}
.set-card:hover::before {{ opacity: 1; }}
.set-card-label {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; color: var(--gold); letter-spacing: 0.08em; }}
.set-card-name {{ font-size: 0.82rem; font-weight: 600; color: var(--text); line-height: 1.3; margin-top: 2px; }}
.set-card-meta {{ font-size: 0.7rem; color: var(--text-dim); margin-top: 4px; }}
.set-card-arrow {{ position: absolute; right: 14px; top: 50%; transform: translateY(-50%); font-size: 1.2rem; color: var(--text-dim); transition: color 0.18s, right 0.18s; }}
.set-card:hover .set-card-arrow {{ color: var(--gold); right: 12px; }}

.section-title {{
  text-align: center;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1rem;
  letter-spacing: 0.2em;
  color: var(--text-dim);
  margin: 30px 0 0;
  padding: 0 24px;
}}
</style>
</head>
<body>

{make_nav(None)}

<div class="hero">
  <div class="hero-title">ONE PIECE CARD GAME</div>
  <div class="hero-sub">ราคาการ์ดทุกชุด OP-01 ถึง OP-15</div>
  <div class="hero-rate">100 ¥ = 20.11 ฿ (มี.ค. 2569) · ราคาจาก yuyu-tei.jp</div>
</div>

<div class="section-title">เลือกชุดการ์ด</div>

<div class="sets-grid">
  {cards_html}
</div>

<footer class="page-footer">
  ราคาจาก <a href="https://yuyu-tei.jp/top/opc" target="_blank">yuyu-tei.jp</a> ·
  รูปภาพจาก <a href="https://asia-th.onepiece-cardgame.com" target="_blank">onepiece-cardgame.com</a>
</footer>

</body>
</html>"""


# Generate all files
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Index
with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(make_index())
print("✓ index.html")

# Set pages
for (sid, slabel, sname, total) in SETS:
    html = make_set_page(sid, slabel, sname, total)
    with open(f"{OUTPUT_DIR}/{sid}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ {sid}.html ({total} cards)")

print("\nDone! Generated", 1 + len(SETS), "files.")
