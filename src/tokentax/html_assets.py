"""Static CSS and JS for the HTML report.

Kept as plain strings so the generated page stays a single self-contained file
with no network dependencies — it opens from disk, from GitHub Pages, or from
an offline machine identically.

Colour comes from one sequential blue ramp, light to dark. The ramp is
reversed in dark mode so that "more tax" always means "more prominent against
the surface".

Because the ramp reverses, cell ink has to reverse with it — a slot that is the
darkest blue in light mode is the lightest in dark mode. Ink is therefore a
per-slot variable declared in each mode block rather than a rule on the slot
number. Every pairing clears WCAG AA: the tightest are slot 4 on dark ink
(5.41:1) and slot 5 on white (5.39:1) in light mode, mirrored in dark.
"""

CSS = """
:root {
  --surface: #fcfcfb; --plane: #f9f9f7;
  --ink: #0b0b0b; --ink-2: #52514e; --ink-muted: #898781;
  --hairline: #e1e0d9; --ring: rgba(11,11,11,0.10);
  --s1:#cde2fb; --s2:#9ec5f4; --s3:#6da7ec; --s4:#3987e5;
  --s5:#256abf; --s6:#184f95; --s7:#0d366b;
  --i1:#0b0b0b; --i2:#0b0b0b; --i3:#0b0b0b; --i4:#0b0b0b;
  --i5:#ffffff; --i6:#ffffff; --i7:#ffffff;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) {
    --surface: #1a1a19; --plane: #0d0d0d;
    --ink: #ffffff; --ink-2: #c3c2b7; --ink-muted: #898781;
    --hairline: #2c2c2a; --ring: rgba(255,255,255,0.10);
    --s1:#0d366b; --s2:#184f95; --s3:#256abf; --s4:#3987e5;
    --s5:#6da7ec; --s6:#9ec5f4; --s7:#cde2fb;
    --i1:#ffffff; --i2:#ffffff; --i3:#ffffff; --i4:#0b0b0b;
    --i5:#0b0b0b; --i6:#0b0b0b; --i7:#0b0b0b;
  }
}
:root[data-theme="dark"] {
  --surface: #1a1a19; --plane: #0d0d0d;
  --ink: #ffffff; --ink-2: #c3c2b7; --ink-muted: #898781;
  --hairline: #2c2c2a; --ring: rgba(255,255,255,0.10);
  --s1:#0d366b; --s2:#184f95; --s3:#256abf; --s4:#3987e5;
  --s5:#6da7ec; --s6:#9ec5f4; --s7:#cde2fb;
  --i1:#ffffff; --i2:#ffffff; --i3:#ffffff; --i4:#0b0b0b;
  --i5:#0b0b0b; --i6:#0b0b0b; --i7:#0b0b0b;
}

* { box-sizing: border-box; }
body {
  margin: 0; padding: 2rem 1.25rem 4rem;
  background: var(--plane); color: var(--ink);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
}
/* Wide enough for the full tokenizer matrix without horizontal scrolling on a
   laptop. Prose blocks below keep their own narrower measure. */
.wrap { max-width: 1420px; margin: 0 auto; }
h1 { font-size: 1.6rem; margin: 0 0 .35rem; letter-spacing: -0.01em; }
.sub { color: var(--ink-2); margin: 0 0 1.75rem; max-width: 62ch; }
.meta { color: var(--ink-muted); font-size: .82rem; margin-top: .4rem; }

.tiles { display: flex; flex-wrap: wrap; gap: .75rem; margin-bottom: 1.75rem; }
.tile {
  background: var(--surface); border: 1px solid var(--ring);
  border-radius: 10px; padding: .85rem 1.1rem; min-width: 168px;
}
.tile .n { font-size: 1.9rem; font-weight: 650; line-height: 1.1; }
.tile .k { color: var(--ink-2); font-size: .8rem; margin-top: .15rem; }

.controls {
  display: flex; flex-wrap: wrap; gap: .4rem; align-items: center;
  margin-bottom: 1rem;
}
.controls .label { color: var(--ink-2); font-size: .82rem; margin-right: .25rem; }
button {
  font: inherit; font-size: .82rem; cursor: pointer;
  background: var(--surface); color: var(--ink-2);
  border: 1px solid var(--ring); border-radius: 999px; padding: .3rem .75rem;
}
button:hover { color: var(--ink); }
button[aria-pressed="true"] { background: var(--s4); color: #fff; border-color: transparent; }
button:focus-visible { outline: 2px solid var(--s4); outline-offset: 2px; }

.scroll { overflow-x: auto; background: var(--surface);
  border: 1px solid var(--ring); border-radius: 10px; }
table { border-collapse: separate; border-spacing: 2px; width: 100%; }
th, td { font-size: .8rem; text-align: right; white-space: nowrap; }
thead th {
  color: var(--ink-2); font-weight: 550; padding: .7rem .5rem;
  position: sticky; top: 0; background: var(--surface); text-align: right;
}
thead th.corner, tbody th { text-align: left; }
tbody th {
  color: var(--ink); font-weight: 500; padding: .3rem .6rem;
  position: sticky; left: 0; background: var(--surface);
}
tbody th .scr { color: var(--ink-muted); font-weight: 400; font-size: .74rem; }
td.cell {
  padding: .38rem .55rem; border-radius: 4px;
  font-variant-numeric: tabular-nums; cursor: default;
}
td.na { color: var(--ink-muted); background: transparent; }
td.cell.lossy { outline: 2px solid var(--ring); outline-offset: -2px; }
tr:hover td.cell { filter: brightness(1.06); }

.legend { display: flex; align-items: center; gap: .5rem; margin: 1rem 0 .25rem;
  color: var(--ink-2); font-size: .8rem; flex-wrap: wrap; }
.legend .sw { display: inline-block; width: 30px; height: 12px; border-radius: 3px; }
.note { color: var(--ink-muted); font-size: .8rem; margin-top: .75rem; max-width: 76ch; }

#tip {
  position: fixed; pointer-events: none; opacity: 0; transition: opacity .1s;
  background: var(--surface); color: var(--ink); border: 1px solid var(--ring);
  border-radius: 8px; padding: .55rem .7rem; font-size: .8rem;
  box-shadow: 0 6px 20px rgba(0,0,0,.16); max-width: 260px; z-index: 10;
}
#tip b { display: block; margin-bottom: .25rem; }
#tip .row { color: var(--ink-2); font-variant-numeric: tabular-nums; }
body.plain td.cell { background: transparent !important; color: var(--ink) !important; }
"""

JS = """
const tip = document.getElementById('tip');
document.querySelectorAll('td.cell').forEach(cell => {
  const show = () => {
    tip.innerHTML = cell.dataset.tip;
    tip.style.opacity = '1';
    const r = cell.getBoundingClientRect();
    const t = tip.getBoundingClientRect();
    // Flip above the cell near the bottom edge, and clamp horizontally so the
    // tooltip never leaves the viewport on narrow screens.
    let top = r.bottom + 8;
    if (top + t.height > window.innerHeight - 8) top = r.top - t.height - 8;
    let left = Math.min(r.left, window.innerWidth - t.width - 8);
    tip.style.top = Math.max(8, top) + 'px';
    tip.style.left = Math.max(8, left) + 'px';
  };
  const hide = () => { tip.style.opacity = '0'; };
  cell.addEventListener('mouseenter', show);
  cell.addEventListener('mouseleave', hide);
  cell.tabIndex = 0;
  cell.addEventListener('focus', show);
  cell.addEventListener('blur', hide);
});

const rows = Array.from(document.querySelectorAll('tbody tr'));
document.querySelectorAll('[data-region]').forEach(btn => {
  btn.addEventListener('click', () => {
    const region = btn.dataset.region;
    document.querySelectorAll('[data-region]').forEach(
      b => b.setAttribute('aria-pressed', String(b === btn)));
    rows.forEach(row => {
      row.hidden = region !== 'all' && row.dataset.region !== region;
    });
  });
});

const plain = document.getElementById('plain');
plain.addEventListener('click', () => {
  const on = document.body.classList.toggle('plain');
  plain.setAttribute('aria-pressed', String(on));
  plain.textContent = on ? 'Show heatmap' : 'Show table view';
});
"""
