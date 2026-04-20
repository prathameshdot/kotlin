#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Converts data.txt -> kotlin_course.html
Proper Kotlin learning sequence:
  1. Kotlin Basics (Parts 1-11)
  2. OOP Sections 1-2 (Fundamentals + Core)
  3. OOP Concepts 1-18 (Hinglish deep-dive)
  4. OOP Sections 3-8 (Advanced + Practice + Summary)
"""

import html as html_lib
import re
import sys

def esc(t): return html_lib.escape(str(t), quote=False)

def apply_inline(text):
    t = esc(text)
    t = re.sub(r'`([^`]+)`', r'<code class="ic">\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', t)
    return t

BOX_CHARS = set('┌└│╔╠╚║├┐┘╗╝┤┬┴┼─═▶◀▲▼')
def has_box(s): return any(c in s for c in BOX_CHARS)

_SUB_HEADS = [
    'What is it?','Why do we use it?','Why use it?','Why Use','When to Use',
    'How it Works','How it works','Syntax in Kotlin','Syntax:','Syntax',
    'Real-Life Analogy','Common Mistakes','Best Practices','Best Practice',
    'Interview Questions','Interview Q','Coding Practice','Coding Challenge',
    'Pro Tips','Tips','Memory Trick',
    'When NOT','Interview','Practice Problems','Practice:',
    'Quick Summary','Real World','Real-World',
    'Comparison Table:','Two Types:','Compile-Time','Runtime Polymorphism',
    'Basic Example:','Intermediate Example:','Advanced Example:',
    'Easy Example','Medium Example','Hard Example',
    'Real-World Example:','Real-World Android','Practical Example',
    'DRY RUN','Dry Run','Output:','Output','STEP ','FLOWCHART',
    'PRIMARY CONSTRUCTOR','SECONDARY CONSTRUCTOR','DEFAULT VALUES',
    'BINA CONSTRUCTOR','CONSTRUCTOR KE SAATH','Timeline:',
    'Stack Memory','Heap Memory','Memory Diagram','Memory Model',
    'Summary:','Summary','Revision','Key Points','Key Takeaways',
    'Important:','Note:','Tip:','Warning:','Remember:',
]

_PROSE_STARTERS = [
    'Real','Common','Best','Interview','Coding',
    'Example','Basic','Intermediate','Advanced','Simple',
    'Q:','A:','Why ','What ','How ','When ','Where ','Problem','Solution',
    'Output','Aspect','Comparison','Note:','Tip:',
    'JVM','Android','Kotlin ','Stack ','Heap ','Caller',
    'Procedural','Encapsulation','Inheritance','Polymorphism','Abstraction',
    'Two Types','Compile','Runtime','Method ','Class ','Object ',
    'Extension','Delegation','Lateinit','Sealed','Enum','Data Class',
    'Companion','Singleton','Inner ','Nested ','MEMORY','QUICK',
    'DRY RUN','Dry Run','FLOWCHART','PATTERN','STEP ','GOAL:',
    'Socho','Matlab','Yahi','Agar','Jab ','Toh ','Aur ','Lekin ',
    'Easy Example','Medium Example','Hard Example','Practical Example',
    'Kotlin mein','Java mein','PRIMARY ','SECONDARY ','DEFAULT ',
    'BINA ','CONSTRUCTOR KE','Timeline:','Stack Memory','Heap Memory',
    'POLYMORPHISM','INHERITANCE','ENCAPSULATION',
]

def is_code_end(s):
    if not s: return False
    for p in _PROSE_STARTERS:
        if s.startswith(p): return True
    if len(s) > 50 and not any(c in s for c in ['{','}','->','==','!=','+=','-=','::','?.','!!','(',')']):
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
#  BLOCK EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

def find_course_start(lines):
    for i, raw in enumerate(lines):
        s = raw.strip()
        if '🎓' in s and 'Complete OOP' in s:
            return i
    # Fallback: first SECTION header
    for i, raw in enumerate(lines):
        if re.match(r'^[🔷🔶]*\s*SECTION\s+\d+', raw.strip(), re.I):
            return i
    return 0

def get_block_ranges(lines):
    """Returns list of (type, num, start, end) for each major block."""
    markers = []
    for i, raw in enumerate(lines):
        s = raw.strip()
        m = re.match(r'^[🔷🔶]*\s*SECTION\s+(\d+)', s, re.I)
        if m: markers.append(('section', int(m.group(1)), i)); continue
        m = re.match(r'^🔹\s*CONCEPT\s+(\d+)', s)
        if m: markers.append(('concept', int(m.group(1)), i)); continue
        m = re.match(r'^🔹\s*PART\s+(\d+)', s)
        if m: markers.append(('part', int(m.group(1)), i)); continue

    result = []
    for idx, (typ, num, start) in enumerate(markers):
        end = markers[idx + 1][2] if idx + 1 < len(markers) else len(lines)
        result.append((typ, num, start, end))
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  HTML CONTENT BUILDER (single slice)
# ─────────────────────────────────────────────────────────────────────────────

def build_html(lines):
    out = []
    i, n = 0, len(lines)

    def emit_code(buf):
        while buf and not buf[-1].strip(): buf.pop()
        if buf:
            code_text = esc('\n'.join(buf))
            out.append(
                '<div class="code-wrap">'
                '<div class="code-header">'
                '<span class="code-lang">Kotlin</span>'
                '<button class="copy-btn" onclick="copyCode(this)">Copy</button>'
                '</div>'
                '<pre class="code-block"><code class="language-kotlin">'
                + code_text +
                '</code></pre>'
                '</div>'
            )

    while i < n:
        raw = lines[i]
        s   = raw.strip()

        # ── skip stray UI lines ──────────────────────────────────────────────
        if not s or s == 'Show more' or (s.startswith('Apr ') and len(s) < 12):
            i += 1; continue

        # ── decorative separators ────────────────────────────────────────────
        if re.match(r'^[=\-]{5,}$', s):
            i += 1; continue

        # ── explicit kotlin code block ───────────────────────────────────────
        if s == 'kotlin':
            i += 1
            buf = []
            while i < n:
                cl = lines[i]; cs = cl.strip()
                if cs == 'kotlin': break
                if cs and is_code_end(cs): break
                if not cs:
                    j = i + 1
                    while j < n and not lines[j].strip(): j += 1
                    nxt = lines[j].strip() if j < n else ''
                    if not nxt or nxt == 'kotlin' or is_code_end(nxt): break
                    buf.append(cl)
                else:
                    buf.append(cl)
                i += 1
            emit_code(buf)
            continue  # do NOT i+=1; inner loop already advanced past block

        # ── BIG SECTION header ───────────────────────────────────────────────
        m = re.match(r'^[🔷🔶🔹]*\s*SECTION\s+(\d+)\s*[:\-]?\s*(.*)', s, re.I)
        if m:
            num   = m.group(1)
            title = m.group(2).strip().lstrip('🔷🔶🔹 ').strip()
            out.append(f'<div class="section-hdr" id="section-{num}">'
                       f'<div class="section-badge">SECTION {num}</div>'
                       f'<div class="section-title">{esc(title)}</div></div>')
            i += 1; continue

        # ── PART header ──────────────────────────────────────────────────────
        m = re.match(r'^🔹\s*PART\s+(\d+)\s*[:\-]?\s*(.+)', s)
        if m:
            num, title = m.group(1), m.group(2).strip()
            out.append(f'<div class="part-hdr" id="part-{num}">'
                       f'<div class="part-badge">PART {num}</div>'
                       f'<div class="part-title">{esc(title)}</div></div>')
            i += 1; continue

        # ── CONCEPT header ───────────────────────────────────────────────────
        m = re.match(r'^🔹\s*CONCEPT\s+(\d+)\s*[:\-]?\s*(.+)', s)
        if m:
            num, title = m.group(1), m.group(2).strip()
            out.append(f'<div class="concept-hdr" id="concept-{num}">'
                       f'<div class="concept-badge">#{num}</div>'
                       f'<div class="concept-title">{esc(title)}</div></div>')
            i += 1; continue

        # ── numbered list item (1. text) ─────────────────────────────────────
        m = re.match(r'^(\d{1,2})\.\s+(.+)', s)
        if m and 1 <= int(m.group(1)) <= 30:
            num, title = m.group(1), m.group(2).strip()
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower())[:38].strip('-')
            out.append(f'<h2 class="sub-topic" id="sub-{num}-{slug}">'
                       f'<span class="sub-num">{num}</span>'
                       f'<span class="sub-title">{apply_inline(title)}</span></h2>')
            i += 1; continue

        # ── callouts (emoji-prefixed lines, checked before sub-headings) ─────
        if s.startswith('💡'):
            out.append(f'<div class="callout tip"><span class="callout-icon">💡</span>{apply_inline(s[1:].strip())}</div>')
            i += 1; continue
        if s.startswith('❌'):
            out.append(f'<div class="callout err"><span class="callout-icon">❌</span>{apply_inline(s[1:].strip())}</div>')
            i += 1; continue
        if s.startswith('✅'):
            out.append(f'<div class="callout ok"><span class="callout-icon">✅</span>{apply_inline(s[1:].strip())}</div>')
            i += 1; continue
        if s.startswith(('⚠', '🚨')):
            out.append(f'<div class="callout warn"><span class="callout-icon">⚠️</span>{apply_inline(s[1:].strip())}</div>')
            i += 1; continue

        # ── emoji topic headers ───────────────────────────────────────────────
        if s[0] in '🔷🔶🎓🏗📦🔒🔑🧩🎯🔥🧠🌍⚙🧒💻🧪🎮':
            out.append(f'<h2 class="topic-hdr">{esc(s)}</h2>')
            i += 1; continue

        # ── sub-headings ─────────────────────────────────────────────────────
        matched_sub = False
        for sh in _SUB_HEADS:
            if s.startswith(sh):
                out.append(f'<h3 class="sub-heading">{apply_inline(s)}</h3>')
                matched_sub = True; break
        if matched_sub:
            i += 1; continue

        # ── Q & A ────────────────────────────────────────────────────────────
        if re.match(r'^Q\d*\s*[:.)]', s):
            out.append(f'<div class="qa-q">{apply_inline(s)}</div>'); i += 1; continue
        if re.match(r'^A\d*\s*[:.)]', s):
            out.append(f'<div class="qa-a">{apply_inline(s)}</div>'); i += 1; continue

        # ── pipe table ───────────────────────────────────────────────────────
        if s.startswith('|') and s.count('|') >= 2:
            rows = []
            while i < n:
                r = lines[i].strip()
                if not (r.startswith('|') and r.count('|') >= 2): break
                rows.append(r); i += 1
            rows = [r for r in rows if not re.match(r'^\|[\s\-:|]+\|$', r)]
            if rows:
                out.append('<div class="tbl-wrap"><table class="data-table">')
                for ri, row in enumerate(rows):
                    cells = [c.strip() for c in row.strip('|').split('|')]
                    tag = 'th' if ri == 0 else 'td'
                    out.append('<tr>' + ''.join(f'<{tag}>{apply_inline(c)}</{tag}>' for c in cells) + '</tr>')
                out.append('</table></div>')
            continue  # i already advanced

        # ── tab table ────────────────────────────────────────────────────────
        if '\t' in s and not s.startswith(('//', 'val ', 'var ', 'fun ', 'class ', 'object ', 'import ')):
            rows = []
            while i < n:
                r = lines[i].strip()
                if '\t' not in r: break
                if r.startswith(('//', 'val ', 'var ', 'fun ')): break
                rows.append(r); i += 1
            if rows:
                out.append('<div class="tbl-wrap"><table class="data-table">')
                for ri, row in enumerate(rows):
                    cells = [c.strip() for c in row.split('\t') if c.strip()]
                    if not cells: continue
                    tag = 'th' if ri == 0 else 'td'
                    out.append('<tr>' + ''.join(f'<{tag}>{apply_inline(c)}</{tag}>' for c in cells) + '</tr>')
                out.append('</table></div>')
            continue  # i already advanced

        # ── ASCII / box art ──────────────────────────────────────────────────
        if has_box(raw):
            art = []
            while i < n and (has_box(lines[i]) or (not lines[i].strip() and art)):
                if not lines[i].strip():
                    j = i + 1
                    if j >= n or not has_box(lines[j]): break
                art.append(lines[i]); i += 1
            while art and not art[-1].strip(): art.pop()
            if art:
                out.append(f'<pre class="ascii-art">{esc(chr(10).join(art))}</pre>')
            continue  # i already advanced

        # ── vs header ────────────────────────────────────────────────────────
        if re.match(r'.+\s+vs\.?\s+.+', s, re.I) and len(s) < 80:
            out.append(f'<h3 class="vs-hdr">{esc(s)}</h3>'); i += 1; continue

        # ── default paragraph ─────────────────────────────────────────────────
        out.append(f'<p class="prose">{apply_inline(s)}</p>')
        i += 1

    return '\n'.join(out)


# ─────────────────────────────────────────────────────────────────────────────
#  NAV BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def extract_nav(lines):
    sections, concepts, parts = [], [], []
    for line in lines:
        s = line.strip()
        m = re.match(r'^[🔷🔶]*\s*SECTION\s+(\d+)\s*[:\-]?\s*(.*)', s, re.I)
        if m:
            title = m.group(2).strip().lstrip('🔷🔶 ').strip() or f'Section {m.group(1)}'
            sections.append((m.group(1), title)); continue
        m = re.match(r'^🔹\s*CONCEPT\s+(\d+)\s*[:\-]?\s*(.+)', s)
        if m: concepts.append((m.group(1), m.group(2).strip())); continue
        m = re.match(r'^🔹\s*PART\s+(\d+)\s*[:\-]?\s*(.+)', s)
        if m: parts.append((m.group(1), m.group(2).strip())); continue
    return sections, concepts, parts


def build_nav(sections, concepts, parts):
    def group(icon, title, items, prefix, badge_cls, open_=True):
        closed = '' if open_ else ' closed'
        h = [
            f'<div class="nav-group{closed}">',
            f'<button class="nav-group-btn" onclick="toggleGroup(this)">',
            f'<span class="ngi">{icon}</span>',
            f'<span class="ng-title">{title}</span>',
            f'<span class="ng-count">{len(items)}</span>',
            f'<span class="nav-arr">▾</span>',
            f'</button>',
            '<ul class="nav-items">',
        ]
        for num, t in items:
            short = t[:34] + ('…' if len(t) > 34 else '')
            h.append(
                f'<li><a href="#{prefix}-{num}" class="nav-link" data-anchor="{prefix}-{num}">'
                f'<span class="nav-badge {badge_cls}">{num}</span>'
                f'<span class="nav-lbl">{esc(short)}</span>'
                f'</a></li>'
            )
        h += ['</ul>', '</div>']
        return '\n'.join(h)

    # Sidebar order: Kotlin Basics → OOP Sections → OOP Concepts
    return (
        '<div class="nav-inner">'
        + group('📝', 'Kotlin Basics', parts, 'part', 'b-part', True)
        + group('📖', 'OOP Sections', sections, 'section', 'b-sec', True)
        + group('🏗️', 'OOP Concepts', concepts, 'concept', 'b-con', False)
        + '</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Complete Kotlin OOP Course — Beginner to Advanced</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<style>
/* ── VARIABLES ───────────────────────────────────────────────────────────── */
:root{
  --bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--bg4:#2d333b;--bg5:#1c2128;
  --brd:#30363d;--brd2:#444c56;--brd3:#545d68;
  --tx:#cdd9e5;--tx2:#768390;--tx3:#adbac7;--tx4:#636e7b;
  --kt:#7f52ff;--kt2:#a37aff;--kt3:#c8b3ff;
  --bl:#539bf5;--bl2:#6cb6ff;
  --gn:#57ab5a;--gn2:#82cf85;
  --rd:#e5534b;--rd2:#ff7b72;
  --yl:#c69026;--yl2:#e3b341;
  --or:#cc6b2c;--pr:#986ee2;--cy:#39c5cf;
  --sw:285px;--th:60px;--r:12px;--rs:8px;--rv:6px;
  --fn:'Inter',system-ui,sans-serif;
  --mo:'JetBrains Mono','Fira Code',monospace;
  --shadow:0 1px 3px rgba(0,0,0,.4),0 4px 16px rgba(0,0,0,.3);
  --shadow2:0 8px 32px rgba(0,0,0,.5);
}
.light{
  --bg:#ffffff;--bg2:#f6f8fa;--bg3:#eaeef2;--bg4:#dde1e6;--bg5:#f0f3f6;
  --brd:#d0d7de;--brd2:#bbc1c9;--brd3:#9ea7b3;
  --tx:#1f2328;--tx2:#656d76;--tx3:#424a53;--tx4:#818b96;
  --shadow:0 1px 3px rgba(0,0,0,.12),0 4px 16px rgba(0,0,0,.08);
  --shadow2:0 8px 32px rgba(0,0,0,.15);
}

/* ── RESET ───────────────────────────────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;font-size:15px}
body{font-family:var(--fn);background:var(--bg);color:var(--tx);min-height:100vh;line-height:1.75}
a{color:var(--bl2);text-decoration:none}
a:hover{text-decoration:underline;color:var(--kt2)}
::selection{background:rgba(127,82,255,.35)}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg2)}
::-webkit-scrollbar-thumb{background:var(--brd2);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--tx2)}

/* ── PROGRESS BAR ────────────────────────────────────────────────────────── */
#prog{
  position:fixed;top:0;left:0;height:3px;width:0;
  background:linear-gradient(90deg,var(--kt),var(--bl),var(--pr),var(--cy));
  z-index:9999;transition:width .08s linear;
  box-shadow:0 0 10px var(--kt);
}

/* ── TOPBAR ──────────────────────────────────────────────────────────────── */
#topbar{
  position:fixed;top:0;left:0;right:0;height:var(--th);
  background:var(--bg2);border-bottom:1px solid var(--brd);
  display:flex;align-items:center;gap:12px;padding:0 20px;
  z-index:900;backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
}
#topbar .logo{
  display:flex;align-items:center;gap:10px;
  font-weight:800;font-size:17px;white-space:nowrap;
  color:var(--tx);letter-spacing:-.3px;
}
#topbar .logo .badge{
  background:linear-gradient(135deg,var(--kt),var(--pr));
  color:#fff;font-size:10px;font-weight:700;padding:2px 8px;
  border-radius:12px;letter-spacing:.5px;
}
#menu-btn{
  background:none;border:none;color:var(--tx3);cursor:pointer;
  padding:8px;border-radius:var(--rv);font-size:18px;line-height:1;
  display:none;
}
#menu-btn:hover{background:var(--bg4);color:var(--tx)}
.tb-sep{flex:1}
.tb-btn{
  background:none;border:1px solid var(--brd);color:var(--tx3);
  cursor:pointer;padding:6px 14px;border-radius:var(--rv);
  font-size:12.5px;font-weight:500;font-family:var(--fn);
  transition:all .15s;white-space:nowrap;
}
.tb-btn:hover{background:var(--bg4);border-color:var(--brd2);color:var(--tx)}
#search-wrap{position:relative;flex:0 1 340px}
#search{
  width:100%;padding:7px 14px 7px 36px;
  background:var(--bg3);border:1px solid var(--brd);
  border-radius:20px;color:var(--tx);font-size:13.5px;
  font-family:var(--fn);outline:none;transition:all .2s;
}
#search:focus{border-color:var(--kt);background:var(--bg);box-shadow:0 0 0 3px rgba(127,82,255,.18)}
#search::placeholder{color:var(--tx4)}
.search-icon{
  position:absolute;left:11px;top:50%;transform:translateY(-50%);
  color:var(--tx4);font-size:13px;pointer-events:none;
}

/* ── SIDEBAR ─────────────────────────────────────────────────────────────── */
.ovl{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:799;backdrop-filter:blur(3px)}
.ovl.show{display:block}
.sidebar{
  position:fixed;top:var(--th);left:0;
  width:var(--sw);height:calc(100vh - var(--th));
  background:var(--bg2);border-right:1px solid var(--brd);
  overflow-y:auto;overflow-x:hidden;z-index:800;
  transition:transform .28s cubic-bezier(.4,0,.2,1);
}
.sidebar::-webkit-scrollbar{width:3px}
.sidebar::-webkit-scrollbar-thumb{background:var(--brd);border-radius:2px}
.nav-inner{padding:6px 0 32px}
.nav-group{border-bottom:1px solid var(--brd)}
.nav-group-btn{
  width:100%;display:flex;align-items:center;gap:8px;
  padding:11px 16px;background:none;border:none;
  color:var(--tx3);font-size:12px;font-weight:700;
  cursor:pointer;text-align:left;font-family:var(--fn);
  letter-spacing:.6px;text-transform:uppercase;
  transition:background .15s,color .15s;
}
.nav-group-btn:hover{background:var(--bg3);color:var(--tx)}
.ngi{font-size:14px}
.ng-title{flex:1}
.ng-count{
  background:var(--bg4);color:var(--tx4);font-size:10px;
  padding:1px 6px;border-radius:10px;font-weight:600;
}
.nav-arr{font-size:10px;color:var(--tx4);transition:transform .2s}
.nav-group.closed .nav-arr{transform:rotate(-90deg)}
.nav-items{list-style:none;display:block;padding-bottom:4px}
.nav-group.closed .nav-items{display:none}
.nav-link{
  display:flex;align-items:center;gap:9px;
  padding:6px 12px 6px 16px;
  color:var(--tx3);font-size:12.5px;
  border-left:3px solid transparent;
  transition:all .14s;line-height:1.4;
}
.nav-link:hover{background:var(--bg3);color:var(--tx);text-decoration:none;border-left-color:var(--brd2)}
.nav-link.active{background:rgba(127,82,255,.12);color:var(--kt3);border-left-color:var(--kt);font-weight:600}
.nav-badge{
  min-width:24px;height:20px;display:flex;align-items:center;justify-content:center;
  border-radius:5px;font-size:10px;font-weight:700;flex-shrink:0;padding:0 4px;
}
.b-part{background:rgba(87,171,90,.2);color:var(--gn2)}
.b-sec {background:rgba(83,155,245,.2);color:var(--bl2)}
.b-con {background:rgba(127,82,255,.2);color:var(--kt3)}
.nav-lbl{flex:1;font-size:12px;line-height:1.35}

/* ── MAIN LAYOUT ─────────────────────────────────────────────────────────── */
.layout{margin-left:var(--sw);margin-top:var(--th);min-height:calc(100vh - var(--th))}
.content{max-width:820px;margin:0 auto;padding:32px 28px 80px}

/* ── HERO ────────────────────────────────────────────────────────────────── */
.hero{
  background:linear-gradient(135deg,rgba(127,82,255,.12),rgba(83,155,245,.08),rgba(152,110,226,.1));
  border:1px solid rgba(127,82,255,.25);
  border-radius:var(--r);padding:40px 36px;margin-bottom:40px;
  position:relative;overflow:hidden;
}
.hero::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at 30% 50%,rgba(127,82,255,.08),transparent 60%),
             radial-gradient(ellipse at 80% 20%,rgba(83,155,245,.06),transparent 50%);
}
.hero h1{
  font-size:clamp(22px,3.5vw,34px);font-weight:800;
  background:linear-gradient(135deg,var(--kt2),var(--bl2),var(--pr));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin-bottom:10px;line-height:1.25;
  position:relative;
}
.hero p{color:var(--tx3);font-size:14.5px;margin-bottom:20px;position:relative;line-height:1.6}
.hero-tags{display:flex;flex-wrap:wrap;gap:8px;position:relative}
.hero-tag{
  padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;
  border:1px solid;letter-spacing:.3px;
}
.tag-kt{background:rgba(127,82,255,.15);border-color:rgba(127,82,255,.4);color:var(--kt2)}
.tag-oop{background:rgba(83,155,245,.12);border-color:rgba(83,155,245,.4);color:var(--bl2)}
.tag-hi{background:rgba(87,171,90,.12);border-color:rgba(87,171,90,.4);color:var(--gn2)}
.tag-adv{background:rgba(198,144,38,.12);border-color:rgba(198,144,38,.4);color:var(--yl2)}

/* ── CHAPTER DIVIDERS ────────────────────────────────────────────────────── */
.chapter-div{
  display:flex;align-items:center;gap:16px;
  margin:48px 0 32px;padding:20px 24px;
  background:linear-gradient(135deg,var(--bg2),var(--bg3));
  border:1px solid var(--brd);border-radius:var(--r);
  border-left:4px solid var(--kt);
}
.chapter-div.ch-basics{border-left-color:var(--gn)}
.chapter-div.ch-oop{border-left-color:var(--bl)}
.chapter-div.ch-concepts{border-left-color:var(--kt)}
.chapter-div.ch-advanced{border-left-color:var(--yl)}
.ch-icon{font-size:28px}
.ch-info h2{font-size:18px;font-weight:800;color:var(--tx);margin-bottom:3px}
.ch-info p{font-size:13px;color:var(--tx2)}

/* ── SECTION HEADER ──────────────────────────────────────────────────────── */
.section-hdr{
  background:linear-gradient(135deg,rgba(83,155,245,.1),rgba(83,155,245,.04));
  border:1px solid rgba(83,155,245,.25);border-left:4px solid var(--bl);
  border-radius:var(--r);padding:24px 28px;margin:40px 0 24px;
}
.section-badge{
  display:inline-block;background:rgba(83,155,245,.2);color:var(--bl2);
  font-size:10px;font-weight:800;padding:3px 10px;border-radius:10px;
  letter-spacing:1px;margin-bottom:8px;border:1px solid rgba(83,155,245,.3);
}
.section-title{font-size:22px;font-weight:800;color:var(--tx);letter-spacing:-.3px}

/* ── CONCEPT HEADER ──────────────────────────────────────────────────────── */
.concept-hdr{
  background:linear-gradient(135deg,rgba(127,82,255,.1),rgba(127,82,255,.04));
  border:1px solid rgba(127,82,255,.25);border-left:4px solid var(--kt);
  border-radius:var(--r);padding:24px 28px;margin:40px 0 24px;
}
.concept-badge{
  display:inline-block;background:rgba(127,82,255,.2);color:var(--kt3);
  font-size:10px;font-weight:800;padding:3px 10px;border-radius:10px;
  letter-spacing:1px;margin-bottom:8px;border:1px solid rgba(127,82,255,.3);
}
.concept-title{font-size:22px;font-weight:800;color:var(--tx);letter-spacing:-.3px}

/* ── PART HEADER ─────────────────────────────────────────────────────────── */
.part-hdr{
  background:linear-gradient(135deg,rgba(87,171,90,.1),rgba(87,171,90,.04));
  border:1px solid rgba(87,171,90,.25);border-left:4px solid var(--gn);
  border-radius:var(--r);padding:24px 28px;margin:40px 0 24px;
}
.part-badge{
  display:inline-block;background:rgba(87,171,90,.2);color:var(--gn2);
  font-size:10px;font-weight:800;padding:3px 10px;border-radius:10px;
  letter-spacing:1px;margin-bottom:8px;border:1px solid rgba(87,171,90,.3);
}
.part-title{font-size:22px;font-weight:800;color:var(--tx);letter-spacing:-.3px}

/* ── SUB TOPIC ───────────────────────────────────────────────────────────── */
.sub-topic{
  display:flex;align-items:center;gap:14px;
  font-size:17px;font-weight:700;color:var(--tx);
  margin:28px 0 14px;padding:14px 18px;
  background:var(--bg2);border:1px solid var(--brd);border-radius:var(--rs);
  border-left:3px solid var(--yl);
}
.sub-num{
  display:flex;align-items:center;justify-content:center;
  min-width:28px;height:28px;background:rgba(198,144,38,.2);
  color:var(--yl2);border-radius:6px;font-size:13px;font-weight:800;
  border:1px solid rgba(198,144,38,.3);flex-shrink:0;
}
.sub-title{flex:1}

/* ── HEADINGS ────────────────────────────────────────────────────────────── */
.topic-hdr{
  font-size:18px;font-weight:800;color:var(--tx);
  margin:28px 0 12px;padding:12px 0;
  border-bottom:2px solid var(--brd);
  display:flex;align-items:center;gap:8px;
}
.sub-heading{
  font-size:14.5px;font-weight:700;color:var(--tx3);
  margin:22px 0 10px;display:flex;align-items:center;gap:6px;
}
.sub-heading::before{content:'▸';color:var(--kt2);font-size:11px}
.vs-hdr{
  font-size:15px;font-weight:700;color:var(--pr);
  margin:20px 0 10px;padding:8px 14px;
  background:rgba(152,110,226,.1);border:1px solid rgba(152,110,226,.25);
  border-radius:var(--rv);
}

/* ── PROSE ───────────────────────────────────────────────────────────────── */
.prose{
  color:var(--tx3);font-size:14.5px;margin:8px 0;
  line-height:1.8;
}
.prose code.ic,.ic{
  font-family:var(--mo);font-size:13px;
  background:var(--bg4);color:var(--kt3);
  padding:1px 6px;border-radius:4px;
  border:1px solid var(--brd);
}
p code.ic{font-size:13px}

/* ── CODE BLOCKS ─────────────────────────────────────────────────────────── */
.code-wrap{
  margin:16px 0;border-radius:var(--r);overflow:hidden;
  border:1px solid var(--brd);box-shadow:var(--shadow);
}
.code-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:8px 16px;background:var(--bg3);border-bottom:1px solid var(--brd);
}
.code-lang{
  font-size:11px;font-weight:700;color:var(--kt2);letter-spacing:.5px;
  text-transform:uppercase;font-family:var(--fn);
}
.copy-btn{
  background:var(--bg4);border:1px solid var(--brd);color:var(--tx3);
  padding:3px 10px;border-radius:5px;font-size:11px;font-weight:600;
  cursor:pointer;font-family:var(--fn);transition:all .15s;
}
.copy-btn:hover{background:var(--bg5);color:var(--tx);border-color:var(--brd2)}
.copy-btn.copied{background:rgba(87,171,90,.2);color:var(--gn2);border-color:rgba(87,171,90,.4)}
.code-block{
  margin:0!important;padding:20px 22px!important;
  background:var(--bg5)!important;border-radius:0!important;
  font-family:var(--mo)!important;font-size:13.5px!important;
  line-height:1.65!important;overflow-x:auto;tab-size:4;
}
.code-block code{font-family:var(--mo)!important;font-size:13.5px!important}

/* ── ASCII ART ───────────────────────────────────────────────────────────── */
.ascii-art{
  font-family:var(--mo);font-size:12.5px;line-height:1.5;
  background:var(--bg2);border:1px solid var(--brd);
  border-radius:var(--rs);padding:18px 20px;margin:14px 0;
  overflow-x:auto;color:var(--cy);white-space:pre;
}

/* ── TABLES ──────────────────────────────────────────────────────────────── */
.tbl-wrap{
  margin:18px 0;border-radius:var(--r);overflow:hidden;
  border:1px solid var(--brd);box-shadow:var(--shadow);
  overflow-x:auto;
}
.data-table{
  width:100%;border-collapse:collapse;font-size:13.5px;
  min-width:400px;
}
.data-table th{
  background:linear-gradient(135deg,var(--bg3),var(--bg4));
  color:var(--tx);font-weight:700;padding:12px 16px;
  text-align:left;border-bottom:2px solid var(--brd2);
  font-size:12.5px;letter-spacing:.3px;
  white-space:nowrap;
}
.data-table td{
  padding:10px 16px;border-bottom:1px solid var(--brd);
  color:var(--tx3);line-height:1.6;vertical-align:top;
}
.data-table tr:last-child td{border-bottom:none}
.data-table tr:nth-child(even) td{background:rgba(255,255,255,.02)}
.data-table tr:hover td{background:rgba(127,82,255,.06);color:var(--tx)}
.data-table td code,.data-table th code{
  font-family:var(--mo);font-size:12px;
  background:var(--bg4);color:var(--kt3);
  padding:1px 5px;border-radius:3px;
  border:1px solid var(--brd);
}

/* ── Q & A ───────────────────────────────────────────────────────────────── */
.qa-q{
  background:rgba(83,155,245,.08);border:1px solid rgba(83,155,245,.25);
  border-left:3px solid var(--bl);border-radius:var(--rs);
  padding:12px 16px;margin:12px 0 4px;
  font-weight:600;color:var(--bl2);font-size:14px;
}
.qa-a{
  background:var(--bg2);border:1px solid var(--brd);
  border-left:3px solid var(--gn);border-radius:var(--rs);
  padding:12px 16px;margin:0 0 12px 20px;
  color:var(--tx3);font-size:14px;line-height:1.7;
}

/* ── CALLOUTS ────────────────────────────────────────────────────────────── */
.callout{
  display:flex;align-items:flex-start;gap:10px;
  padding:13px 16px;border-radius:var(--rs);margin:12px 0;
  font-size:14px;line-height:1.65;
  border:1px solid;
}
.callout-icon{font-size:15px;flex-shrink:0;margin-top:1px}
.callout.tip {background:rgba(198,144,38,.08);border-color:rgba(198,144,38,.3);color:var(--yl2)}
.callout.err {background:rgba(229,83,75,.08);border-color:rgba(229,83,75,.3);color:var(--rd2)}
.callout.ok  {background:rgba(87,171,90,.08);border-color:rgba(87,171,90,.3);color:var(--gn2)}
.callout.warn{background:rgba(229,83,75,.06);border-color:rgba(204,107,44,.35);color:var(--or)}

/* ── BACK TO TOP ─────────────────────────────────────────────────────────── */
#btt{
  position:fixed;bottom:28px;right:28px;
  width:42px;height:42px;background:var(--kt);color:#fff;
  border:none;border-radius:50%;cursor:pointer;font-size:16px;
  display:none;align-items:center;justify-content:center;
  box-shadow:0 4px 16px rgba(127,82,255,.5);
  transition:all .2s;z-index:500;
}
#btt.show{display:flex}
#btt:hover{background:var(--kt2);transform:translateY(-2px);box-shadow:0 8px 24px rgba(127,82,255,.6)}

/* ── SEARCH HIGHLIGHT ────────────────────────────────────────────────────── */
mark{background:rgba(198,144,38,.4);color:var(--yl2);border-radius:2px;padding:0 2px}

/* ── PRINT ───────────────────────────────────────────────────────────────── */
@media print{
  #topbar,#prog,.sidebar,.ovl,#btt{display:none!important}
  .layout{margin-left:0!important;margin-top:0!important}
  .content{max-width:100%;padding:0}
}

/* ── MOBILE ──────────────────────────────────────────────────────────────── */
@media(max-width:900px){
  #menu-btn{display:flex;align-items:center;justify-content:center}
  .sidebar{transform:translateX(-100%)}
  .sidebar.open{transform:translateX(0)}
  .layout{margin-left:0}
  #search-wrap{flex:0 1 200px}
  .content{padding:24px 16px 60px}
}
@media(max-width:600px){
  #search-wrap{display:none}
  .hero{padding:28px 20px}
  .section-hdr,.concept-hdr,.part-hdr{padding:18px 20px}
  .content{padding:18px 12px 60px}
}
</style>
</head>
<body>

<div id="prog"></div>

<header id="topbar">
  <button id="menu-btn" onclick="toggleSidebar()" aria-label="Menu">☰</button>
  <div class="logo">
    <span>Kotlin</span>
    <span class="badge">OOP COURSE</span>
  </div>
  <div class="tb-sep"></div>
  <div id="search-wrap">
    <span class="search-icon">🔍</span>
    <input id="search" type="search" placeholder="Search anything…" oninput="doSearch(this.value)" autocomplete="off">
  </div>
  <button class="tb-btn" onclick="toggleTheme()">☀ / ☾</button>
  <button class="tb-btn" onclick="window.print()">Print</button>
</header>

<div class="ovl" id="ovl" onclick="toggleSidebar()"></div>
<nav class="sidebar" id="sb">
{{NAV}}
</nav>

<div class="layout">
<main class="content">

<div class="hero">
  <h1>Complete Kotlin OOP Course</h1>
  <p>Beginner se Advanced tak — Hinglish + English explanations, real-world examples, interview prep, and hands-on practice.</p>
  <div class="hero-tags">
    <span class="hero-tag tag-kt">Kotlin</span>
    <span class="hero-tag tag-oop">OOP Concepts</span>
    <span class="hero-tag tag-hi">Hinglish</span>
    <span class="hero-tag tag-adv">Interview Ready</span>
  </div>
</div>

{{BODY}}

</main>
</div>

<button id="btt" onclick="scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">↑</button>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-kotlin.min.js"></script>
<script>
/* progress bar */
window.addEventListener('scroll',function(){
  var d=document.documentElement,b=document.body;
  var h=Math.max(d.scrollHeight,b.scrollHeight)-d.clientHeight;
  document.getElementById('prog').style.width=((window.scrollY/h)*100)+'%';
  document.getElementById('btt').classList.toggle('show',window.scrollY>400);
},{ passive:true });

/* sidebar toggle */
function toggleSidebar(){
  document.getElementById('sb').classList.toggle('open');
  document.getElementById('ovl').classList.toggle('show');
}

/* group collapse */
function toggleGroup(btn){
  btn.parentElement.classList.toggle('closed');
}

/* theme */
function toggleTheme(){
  document.documentElement.classList.toggle('light');
  try{localStorage.setItem('theme',document.documentElement.classList.contains('light')?'light':'dark')}catch(e){}
}
try{if(localStorage.getItem('theme')==='light')document.documentElement.classList.add('light')}catch(e){}

/* active nav link via IntersectionObserver */
var anchors=document.querySelectorAll('[id^=section-],[id^=concept-],[id^=part-]');
var links={};
document.querySelectorAll('.nav-link[data-anchor]').forEach(function(a){links[a.dataset.anchor]=a});
var active=null;
function setActive(id){
  if(active)active.classList.remove('active');
  active=links[id];
  if(active){active.classList.add('active');active.scrollIntoView({block:'nearest'})}
}
if(typeof IntersectionObserver!=='undefined'){
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){if(e.isIntersecting)setActive(e.target.id)});
  },{rootMargin:'-10% 0px -80% 0px'});
  anchors.forEach(function(el){obs.observe(el)});
}

/* copy to clipboard */
function copyCode(btn){
  var code=btn.closest('.code-wrap').querySelector('code');
  navigator.clipboard.writeText(code.innerText||code.textContent).then(function(){
    btn.textContent='Copied!';btn.classList.add('copied');
    setTimeout(function(){btn.textContent='Copy';btn.classList.remove('copied')},1800);
  }).catch(function(){btn.textContent='Error'});
}

/* search */
var searchTimeout=null;
function doSearch(q){
  clearTimeout(searchTimeout);
  searchTimeout=setTimeout(function(){runSearch(q)},200);
}
function runSearch(q){
  clearMarks();
  if(!q||q.length<2)return;
  var walker=document.createTreeWalker(document.querySelector('.content'),NodeFilter.SHOW_TEXT,null,false);
  var re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');
  var node,first=null;
  while((node=walker.nextNode())){
    if(node.parentNode.closest('script,style,pre'))continue;
    if(!re.test(node.nodeValue))continue;
    re.lastIndex=0;
    var frag=document.createDocumentFragment(),parts=node.nodeValue.split(re),j=0;
    parts.forEach(function(p){
      if(!p)return;
      if(j%2===1){var m=document.createElement('mark');m.textContent=p;frag.appendChild(m);if(!first)first=m}else{frag.appendChild(document.createTextNode(p))}j++;
    });
    node.parentNode.replaceChild(frag,node);
  }
  if(first)first.scrollIntoView({behavior:'smooth',block:'center'});
}
function clearMarks(){
  document.querySelectorAll('mark').forEach(function(m){
    var p=m.parentNode;if(!p)return;p.replaceChild(document.createTextNode(m.textContent),m);p.normalize();
  });
}
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    src = 'E:/kotlin/data.txt'
    out_path = 'E:/kotlin/kotlin_course.html'

    print('Reading file...')
    with open(src, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]
    print(f'{len(lines)} lines.')

    # ── extract nav info ──────────────────────────────────────────────────────
    sections, concepts, parts = extract_nav(lines)
    print(f'Nav: {len(sections)} sections / {len(concepts)} concepts / {len(parts)} parts')

    # ── get block ranges ──────────────────────────────────────────────────────
    ranges = get_block_ranges(lines)

    # Build lookup dicts by (type, num)
    sec_map = {n: (s, e) for t, n, s, e in ranges if t == 'section'}
    con_map = {n: (s, e) for t, n, s, e in ranges if t == 'concept'}
    part_map = {n: (s, e) for t, n, s, e in ranges if t == 'part'}

    # ── build body in proper Kotlin learning order ────────────────────────────
    body_parts = []

    # Chapter 1: Kotlin Basics (Parts 1-11)
    body_parts.append(
        '<div class="chapter-div ch-basics">'
        '<div class="ch-icon">📝</div>'
        '<div class="ch-info">'
        '<h2>Chapter 1: Kotlin Basics</h2>'
        '<p>Variables, Data Types, Operators, Strings, Arrays, Control Flow, Functions — step by step</p>'
        '</div></div>'
    )
    for num in sorted(part_map.keys()):
        s, e = part_map[num]
        body_parts.append(build_html(lines[s:e]))

    # Chapter 2: OOP Foundations — Sections 1 & 2
    body_parts.append(
        '<div class="chapter-div ch-oop">'
        '<div class="ch-icon">📖</div>'
        '<div class="ch-info">'
        '<h2>Chapter 2: OOP Foundations</h2>'
        '<p>Fundamentals + Core OOP concepts with detailed explanations and diagrams</p>'
        '</div></div>'
    )
    for num in [1, 2]:
        if num in sec_map:
            s, e = sec_map[num]
            body_parts.append(build_html(lines[s:e]))

    # Chapter 3: OOP Deep Dive — All 18 Concepts (Hinglish)
    body_parts.append(
        '<div class="chapter-div ch-concepts">'
        '<div class="ch-icon">🏗️</div>'
        '<div class="ch-info">'
        '<h2>Chapter 3: OOP Concepts Deep Dive</h2>'
        '<p>18 core OOP concepts — Hinglish explanations, real-world analogies, code examples</p>'
        '</div></div>'
    )
    for num in sorted(con_map.keys()):
        s, e = con_map[num]
        body_parts.append(build_html(lines[s:e]))

    # Chapter 4: Advanced + Practice + Summary — Sections 3-8
    body_parts.append(
        '<div class="chapter-div ch-advanced">'
        '<div class="ch-icon">🚀</div>'
        '<div class="ch-info">'
        '<h2>Chapter 4: Advanced OOP, Practice & Interview Mastery</h2>'
        '<p>Real-world patterns, comparisons, interview Q&A, coding challenges, and revision notes</p>'
        '</div></div>'
    )
    for num in [3, 4, 5, 6, 7, 8]:
        if num in sec_map:
            s, e = sec_map[num]
            body_parts.append(build_html(lines[s:e]))

    body_html = '\n'.join(body_parts)

    # ── build nav ─────────────────────────────────────────────────────────────
    nav_html = build_nav(sections, concepts, parts)

    # ── assemble & write ──────────────────────────────────────────────────────
    page = PAGE.replace('{{NAV}}', nav_html).replace('{{BODY}}', body_html)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)

    size_kb = len(page) // 1024
    print('Done! ' + out_path + '  (' + str(size_kb) + ' KB)')


if __name__ == '__main__':
    main()
