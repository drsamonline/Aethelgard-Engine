#!/usr/bin/env python3
"""
Aethelgard — "Chronicles" vector art overhaul.

Builds a full set of illustrated SVG models (layered shapes, gradients,
shading, rim light, outlines) for every sprite key the game asks for,
and rasterises an HD PNG copy of each with CairoSVG.

    python3 tools/make-overhaul-art.py

Output:
    mods/overhaul-vector/sprites/<key>.svg   crisp vector art
    mods/overhaul-vector/hd/<key>.png        rasterised HD copies
    mods/overhaul-vector/mod.js              the graphics-pack mod

Nothing here needs the game to change: it is a graphics pack, selected
in Settings -> Graphics pack.
"""
import pathlib
import math

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = ROOT / "mods" / "overhaul-vector"
SPR = PACK / "sprites"
HD = PACK / "hd"
SPR.mkdir(parents=True, exist_ok=True)
HD.mkdir(parents=True, exist_ok=True)

INK = "#151122"          # outline colour
V = 128                  # canvas


# ----------------------------------------------------------------- helpers
def doc(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {V} {V}" '
            f'width="{V}" height="{V}">\n<defs>{defs}</defs>\n{body}\n</svg>\n')


def lg(gid, c1, c2, x1=0, y1=0, x2=0, y2=1):
    return (f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')


def rg(gid, c1, c2, cx=0.5, cy=0.4, r=0.7):
    return (f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>')


def shadow(cx=64, cy=118, rx=26, ry=7, op=0.34):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="{op}"/>'


def outline(d):
    return f'stroke="{INK}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"'


def body(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}" {outline(d)}{(" " + extra) if extra else ""}/>'


def el(cx, cy, rx, ry, fill, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {outline("")}{(" " + extra) if extra else ""}/>'


def rim(d, color="#ffffff", op=0.5, w=2.2):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'


def eyes(cx=64, cy=40, spread=7, r=2.6, glow=None, angry=False):
    if glow:
        return (f'<circle cx="{cx-spread}" cy="{cy}" r="{r+1.6}" fill="{glow}" opacity=".55"/>'
                f'<circle cx="{cx+spread}" cy="{cy}" r="{r+1.6}" fill="{glow}" opacity=".55"/>')
    if angry:
        return (f'<path d="M{cx-spread-4} {cy-3} l7 3" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
                f'<path d="M{cx+spread+4} {cy-3} l-7 3" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
                f'<circle cx="{cx-spread}" cy="{cy+1}" r="{r}" fill="{INK}"/>'
                f'<circle cx="{cx+spread}" cy="{cy+1}" r="{r}" fill="{INK}"/>')
    return (f'<circle cx="{cx-spread}" cy="{cy}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{cx+spread}" cy="{cy}" r="{r}" fill="{INK}"/>')


# ----------------------------------------------------------------- weapons
def w_sword(x, y, blade="#d7dcea", hilt="#8a6a3a", scale=1.0, angle=-18):
    g = (f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">'
         f'<path d="M0 -40 L5 -30 L5 4 L-5 4 L-5 -30 Z" fill="{blade}" {outline("")}/>'
         f'<path d="M0 -38 L2.6 -30 L2.6 2 L0 2 Z" fill="#ffffff" opacity=".55"/>'
         f'<rect x="-13" y="4" width="26" height="5" rx="2.5" fill="{hilt}" {outline("")}/>'
         f'<rect x="-3.5" y="9" width="7" height="15" rx="3" fill="{hilt}" {outline("")}/>'
         f'<circle cx="0" cy="26" r="4" fill="{hilt}" {outline("")}/></g>')
    return g


def w_axe(x, y, head="#c9ced9", haft="#7a5a34", scale=1.0, angle=-14):
    return (f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">'
            f'<rect x="-3" y="-34" width="6" height="62" rx="3" fill="{haft}" {outline("")}/>'
            f'<path d="M-2 -34 q22 -6 24 12 q-14 6 -24 2 Z" fill="{head}" {outline("")}/>'
            f'<path d="M-2 -34 q-22 -6 -24 12 q14 6 24 2 Z" fill="{head}" {outline("")}/></g>')


def w_bow(x, y, wood="#8a6a3a", scale=1.0, angle=0):
    return (f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">'
            f'<path d="M0 -34 q22 34 0 68" fill="none" stroke="{wood}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M0 -34 q-16 34 0 68" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M0 -34 L0 34" stroke="#e8e8ee" stroke-width="2"/></g>')


def w_staff(x, y, orb="#7ad0ff", wood="#6a4a2e", scale=1.0, angle=0):
    return (f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">'
            f'<rect x="-3" y="-30" width="6" height="66" rx="3" fill="{wood}" {outline("")}/>'
            f'<circle cx="0" cy="-38" r="11" fill="{orb}" {outline("")}/>'
            f'<circle cx="-3" cy="-41" r="4" fill="#ffffff" opacity=".7"/></g>')


def w_dagger(x, y, blade="#d7dcea", scale=1.0, angle=-24):
    return (f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">'
            f'<path d="M0 -22 L4 -16 L4 2 L-4 2 L-4 -16 Z" fill="{blade}" {outline("")}/>'
            f'<rect x="-8" y="2" width="16" height="4" rx="2" fill="#8a6a3a" {outline("")}/>'
            f'<rect x="-3" y="6" width="6" height="11" rx="3" fill="#5c4020" {outline("")}/></g>')


def w_shield(x, y, base="#8a90a8", trim="#e0b34d", scale=1.0):
    return (f'<g transform="translate({x},{y}) scale({scale})">'
            f'<path d="M0 -30 L22 -20 L19 8 Q0 30 -19 8 L-22 -20 Z" fill="{base}" {outline("")}/>'
            f'<path d="M0 -24 L16 -16 L14 6 Q0 23 -14 6 L-16 -16 Z" fill="none" stroke="{trim}" stroke-width="3"/>'
            f'<circle cx="0" cy="-6" r="5" fill="{trim}" {outline("")}/></g>')


# ----------------------------------------------------------------- creatures
def humanoid(skin="#d8a273", cloth="#5b4a86", armor="#8f95ad", accent="#e0b34d",
             weapon="sword", hood=None, cape=None, big=0.0, aura=None):
    """A standing hero figure. `big` scales bulk (0 normal, 1 huge)."""
    s = 1 + big * 0.28
    d = []
    if aura:
        d.append(f'<circle cx="64" cy="66" r="52" fill="{aura}" opacity=".16"/>')
    d.append(shadow(64, 118, 24 + big * 6))
    # legs
    for lx in (54, 74):
        d.append(body(f"M{lx-7} 84 L{lx+7} 84 L{lx+6} 112 L{lx-6} 112 Z", cloth))
    d.append(body("M46 110 L64 110 L64 118 L44 118 Q42 112 46 110 Z", "#3b3350"))
    d.append(body("M64 110 L82 110 Q86 112 84 118 L64 118 Z", "#3b3350"))
    # cape behind
    if cape:
        d.append(body("M64 46 Q34 60 32 116 L96 116 Q94 60 64 46 Z", cape, 'opacity=".95"'))
    # torso
    tw = 17 * s
    d.append(body(f"M64 {50} q-{tw} 2 -{tw} 14 q0 16 {tw-2} 22 q{tw-2} 2 {2*tw-2} -2 q{tw-2} -6 {tw-2} -22 q0 -12 -{tw} -14 Z", armor))
    d.append(f'<path d="M64 56 q-10 3 -10 14" fill="none" stroke="#ffffff" stroke-width="2" opacity=".35"/>')
    # belt
    d.append(f'<rect x="{64-tw+1}" y="78" width="{2*tw-2}" height="6" rx="3" fill="{accent}" {outline("")}/>')
    # pauldrons
    d.append(el(64 - tw - 3, 55, 10, 8, armor))
    d.append(el(64 + tw + 3, 55, 10, 8, armor))
    d.append(el(64 - tw - 4, 53, 6, 4, accent, 'opacity=".55"'))
    d.append(el(64 + tw + 4, 53, 6, 4, accent, 'opacity=".55"'))
    # arms
    d.append(body(f"M{64-tw-2} 60 q-8 14 -4 26 l9 1 q-3 -14 3 -24 Z", skin))
    d.append(body(f"M{64+tw+2} 60 q8 14 4 26 l-9 1 q3 -14 -3 -24 Z", skin))
    # neck + head
    d.append(f'<rect x="58" y="42" width="12" height="10" fill="{skin}" {outline("")}/>')
    d.append(el(64, 36, 14, 15, skin))
    d.append(f'<path d="M56 26 q8 -6 16 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity=".3"/>')
    # hair / hood / helm
    if hood:
        d.append(body("M64 18 q-20 4 -18 24 q10 -6 18 -6 q8 0 18 6 q2 -20 -18 -24 Z", hood))
    elif weapon == "staff":
        d.append(body("M64 18 q-20 4 -18 24 q10 -6 18 -6 q8 0 18 6 q2 -20 -18 -24 Z", cloth))
    else:
        d.append(body("M64 20 q-16 2 -15 14 q7 -8 15 -8 q8 0 15 8 q1 -12 -15 -14 Z", "#4a3a2a"))
        d.append(f'<path d="M49 30 q15 -10 30 0" fill="none" stroke="{accent}" stroke-width="4"/>')
    # face
    d.append(eyes(64, 37, 5.5, 2.2))
    d.append(f'<path d="M60 44 q4 3 8 0" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    # weapon
    if weapon == "sword":
        d.append(w_sword(94, 66, scale=0.9))
    elif weapon == "axe":
        d.append(w_axe(94, 64, scale=0.9))
    elif weapon == "bow":
        d.append(w_bow(94, 60, scale=0.85))
    elif weapon == "staff":
        d.append(w_staff(94, 62, scale=0.9))
    elif weapon == "dagger":
        d.append(w_dagger(92, 72, scale=1.0))
    elif weapon == "twin":
        d.append(w_dagger(92, 70, scale=0.95))
        d.append(w_dagger(36, 70, scale=0.95, angle=24))
    elif weapon == "shield":
        d.append(w_shield(36, 68, base=armor, trim=accent, scale=0.95))
    return doc("".join(d))


def beast(body_c="#8a8f9e", dark="#5c6070", eye="#ffd36b", ears="pointy", tail=True,
          tusks=False, size=1.0):
    d = [shadow(64, 116, 30, 7)]
    if ears == "pointy":
        d.append(body("M40 52 L34 30 L52 44 Z", dark))
        d.append(body("M88 52 L94 30 L76 44 Z", dark))
    if tail:
        d.append(body("M92 70 q22 -6 20 -24 q-3 16 -22 16 Z", dark))
    # legs
    for lx in (44, 60, 74, 90):
        d.append(body(f"M{lx-6} 84 L{lx+6} 84 L{lx+5} 110 L{lx-5} 110 Z", dark))
    # body
    d.append(el(64, 76, 34 * size, 22 * size, body_c))
    d.append(f'<path d="M40 66 q24 -12 48 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity=".22"/>')
    # head
    d.append(el(40, 60, 20, 17, body_c))
    d.append(body("M22 62 L6 66 L22 72 Z", dark))          # snout
    if tusks:
        d.append(body("M14 70 L10 80 L18 72 Z", "#f2f0e6"))
    d.append(eyes(38, 56, 6, 2.6, glow=eye))
    # chest fur
    d.append(f'<path d="M52 62 q14 10 0 22" fill="none" stroke="{dark}" stroke-width="4" stroke-linecap="round"/>')
    return doc("".join(d))


def brute(skin="#7fa25e", dark="#4f6b3a", cloth="#6b4a2a", accent="#c9a227",
          horns=True, tusks=True, size=1.0, weapon="club"):
    d = [shadow(64, 118, 28, 7)]
    # legs
    for lx in (50, 78):
        d.append(body(f"M{lx-9} 86 L{lx+9} 86 L{lx+7} 116 L{lx-7} 116 Z", dark))
    # torso
    d.append(body("M64 48 q-26 3 -24 22 q2 18 24 20 q22 -2 24 -20 q2 -19 -24 -22 Z", skin))
    d.append(f'<path d="M48 60 q16 -8 32 0" fill="none" stroke="#ffffff" stroke-width="2.6" opacity=".22"/>')
    # cloth
    d.append(body("M40 82 q24 10 48 0 l2 10 q-26 10 -52 0 Z", cloth))
    d.append(f'<rect x="42" y="80" width="44" height="5" rx="2.5" fill="{accent}" {outline("")}/>')
    # arms
    d.append(body("M42 56 q-14 12 -12 30 l12 2 q-2 -18 8 -26 Z", skin))
    d.append(body("M86 56 q14 12 12 30 l-12 2 q2 -18 -8 -26 Z", skin))
    # head
    d.append(el(64, 36, 17, 15, skin))
    if horns:
        d.append(body("M50 24 q-10 -10 -2 -18 q6 8 10 14 Z", "#e8e0cc"))
        d.append(body("M78 24 q10 -10 2 -18 q-6 8 -10 14 Z", "#e8e0cc"))
    if tusks:
        d.append(body("M56 46 L54 56 L60 48 Z", "#f2f0e6"))
        d.append(body("M72 46 L74 56 L68 48 Z", "#f2f0e6"))
    d.append(eyes(64, 36, 6.5, 2.6, angry=True))
    # weapon
    if weapon == "club":
        d.append(body("M94 40 l14 10 l-4 22 l-14 -6 Z", "#7a5a34"))
    elif weapon == "axe":
        d.append(w_axe(96, 66, scale=0.95))
    return doc("".join(d))


def boss(kind="coven", aura="#b45cff"):
    d = [f'<circle cx="64" cy="64" r="56" fill="{aura}" opacity=".18"/>',
         f'<circle cx="64" cy="64" r="44" fill="{aura}" opacity=".12"/>',
         shadow(64, 118, 30, 8)]
    if kind == "coven":
        # horned sorcerer-lord
        d.append(body("M64 44 Q28 62 30 118 L98 118 Q100 62 64 44 Z", "#3a2450"))
        d.append(f'<path d="M64 52 Q44 66 44 112" fill="none" stroke="{aura}" stroke-width="3" opacity=".8"/>')
        d.append(el(64, 34, 15, 15, "#6a4a86"))
        d.append(body("M50 22 q-12 -12 -4 -22 q8 10 12 16 Z", "#e8e0cc"))
        d.append(body("M78 22 q12 -12 4 -22 q-8 10 -12 16 Z", "#e8e0cc"))
        d.append(eyes(64, 34, 6, 2.8, glow="#ff6ad5"))
        d.append(f'<circle cx="98" cy="60" r="13" fill="{aura}" opacity=".9"/>')
        d.append(f'<circle cx="98" cy="60" r="6" fill="#ffffff" opacity=".8"/>')
    elif kind == "warden":
        # iron colossus
        for lx in (46, 82):
            d.append(body(f"M{lx-11} 84 L{lx+11} 84 L{lx+9} 118 L{lx-9} 118 Z", "#6c7288"))
        d.append(body("M64 40 q-30 4 -28 26 q2 20 28 22 q26 -2 28 -22 q2 -22 -28 -26 Z", "#8f95ad"))
        d.append(f'<path d="M44 56 q20 -10 40 0" fill="none" stroke="#e8ecf5" stroke-width="3" opacity=".5"/>')
        d.append(el(64, 30, 16, 15, "#9aa0b8"))
        d.append(f'<rect x="52" y="26" width="24" height="6" rx="3" fill="{aura}"/>')
        d.append(el(40, 52, 12, 10, "#8f95ad"))
        d.append(el(88, 52, 12, 10, "#8f95ad"))
        d.append(body("M92 44 l20 8 l-2 26 l-18 -6 Z", "#a8aec6"))
    elif kind == "warlord":
        for lx in (50, 78):
            d.append(body(f"M{lx-9} 84 L{lx+9} 84 L{lx+7} 118 L{lx-7} 118 Z", "#4a3a2a"))
        d.append(body("M64 44 q-26 3 -24 22 q2 18 24 20 q22 -2 24 -20 q2 -19 -24 -22 Z", "#c98f6a"))
        d.append(body("M40 80 q24 10 48 0 l2 12 q-26 10 -52 0 Z", "#7a2f2f"))
        d.append(el(64, 34, 17, 16, "#c98f6a"))
        d.append(body("M46 26 q18 -14 36 0 q-6 -16 -18 -16 q-12 0 -18 16 Z", "#3a2a20"))
        d.append(eyes(64, 34, 6.5, 2.6, angry=True))
        d.append(w_axe(98, 62, scale=1.05, head="#e0b34d"))
    elif kind == "spider_queen":
        d.append(f'<ellipse cx="64" cy="76" rx="34" ry="26" fill="#6a3f8a" {outline("")}/>')
        for i, (dx, dy) in enumerate([(-1, -1), (-1, 0.2), (-1, 1), (1, -1), (1, 0.2), (1, 1)]):
            x2, y2 = 64 + dx * 46, 76 + dy * 34
            d.append(f'<path d="M64 76 Q{(64+x2)/2} {y2-16} {x2} {y2}" fill="none" stroke="#3a2450" stroke-width="6" stroke-linecap="round"/>')
        d.append(el(64, 46, 16, 14, "#8a5aa8"))
        d.append(eyes(64, 44, 7, 3, glow="#ff6ad5"))
        d.append(f'<circle cx="64" cy="82" r="12" fill="{aura}" opacity=".8"/>')
    else:  # bog_horror
        d.append(body("M64 46 q-32 6 -30 30 q2 24 30 26 q28 -2 30 -26 q2 -24 -30 -30 Z", "#4f7a52"))
        d.append(el(64, 34, 18, 16, "#5f8f5f"))
        d.append(eyes(64, 34, 7, 3, glow="#9cf07a"))
        d.append(f'<path d="M40 70 q10 12 24 12 q14 0 24 -12" fill="none" stroke="#2f4a32" stroke-width="4"/>')
        for x in (34, 94):
            d.append(body(f"M{x} 60 q10 -8 12 6 q-8 6 -12 -6 Z", "#3f5f42"))
    return doc("".join(d))


def undead(kind="wraith"):
    d = [f'<circle cx="64" cy="62" r="46" fill="#7ad0ff" opacity=".14"/>']
    if kind == "skull":
        d.append(body("M64 26 q-26 2 -26 26 q0 18 12 22 l2 16 l24 0 l2 -16 q12 -4 12 -22 q0 -24 -26 -26 Z", "#e6e6de"))
        d.append(f'<ellipse cx="53" cy="50" rx="7" ry="8" fill="{INK}"/>')
        d.append(f'<ellipse cx="75" cy="50" rx="7" ry="8" fill="{INK}"/>')
        d.append(f'<path d="M60 66 l4 6 l4 -6 Z" fill="{INK}"/>')
        d.append(f'<path d="M56 84 l0 -8 M64 84 l0 -8 M72 84 l0 -8" stroke="{INK}" stroke-width="2.4"/>')
    else:
        d.append(body("M64 22 q-24 4 -22 30 q2 20 10 30 q4 14 12 20 q8 -6 12 -20 q8 -10 10 -30 q2 -26 -22 -30 Z", "#cfe8ff", 'opacity=".92"'))
        d.append(body("M64 30 q-14 4 -13 22 q1 14 6 22 q7 -4 7 -12 q0 8 7 12 q5 -8 6 -22 q1 -18 -13 -22 Z", "#8fd0ff", 'opacity=".7"'))
        d.append(eyes(64, 46, 7, 3, glow="#dff3ff"))
        d.append(f'<path d="M64 90 q-10 14 -2 24 q-12 -6 -12 -22" fill="none" stroke="#8fd0ff" stroke-width="4" opacity=".7"/>')
    return doc("".join(d))


def construct():
    d = [shadow(64, 118, 30, 8)]
    for lx in (48, 80):
        d.append(body(f"M{lx-12} 82 L{lx+12} 82 L{lx+10} 118 L{lx-10} 118 Z", "#6b7182"))
    d.append(body("M64 34 q-30 4 -28 26 q2 22 28 24 q26 -2 28 -24 q2 -22 -28 -26 Z", "#8b91a4"))
    d.append(f'<path d="M40 48 q24 -12 48 0" fill="none" stroke="#c9ced9" stroke-width="3" opacity=".55"/>')
    d.append(f'<rect x="52" y="58" width="24" height="16" rx="4" fill="#5fc8ff" opacity=".8"/>')
    d.append(el(64, 26, 15, 13, "#9aa0b8"))
    d.append(eyes(64, 26, 6, 2.4, glow="#5fc8ff"))
    d.append(el(38, 48, 12, 10, "#8b91a4"))
    d.append(el(90, 48, 12, 10, "#8b91a4"))
    return doc("".join(d))


# ----------------------------------------------------------------- items
def flask(liquid="#d15cff", glass="#cfe4f2", cap="#c9a227"):
    return doc(
        f'<path d="M52 20 h24 v14 l16 40 q4 14 -8 20 h-40 q-12 -6 -8 -20 l16 -40 Z" fill="{glass}" opacity=".55" {outline("")}/>'
        f'<path d="M50 62 q14 -6 28 0 l8 22 q2 8 -6 12 h-32 q-8 -4 -6 -12 Z" fill="{liquid}" {outline("")}/>'
        f'<path d="M54 66 q10 -4 20 0" fill="none" stroke="#ffffff" stroke-width="3" opacity=".5"/>'
        f'<rect x="50" y="14" width="28" height="10" rx="4" fill="{cap}" {outline("")}/>'
        f'<ellipse cx="56" cy="52" rx="4" ry="12" fill="#ffffff" opacity=".35"/>')


def gemstone(c="#e2556a", c2="#8a1f34"):
    return doc(
        f'<path d="M64 16 L96 46 L64 112 L32 46 Z" fill="{c}" {outline("")}/>'
        f'<path d="M64 16 L96 46 L64 58 L32 46 Z" fill="{c2}" {outline("")}/>'
        f'<path d="M64 58 L96 46 L64 112 Z" fill="{c}" opacity=".55"/>'
        f'<path d="M48 34 L58 26" stroke="#ffffff" stroke-width="4" opacity=".6" stroke-linecap="round"/>')


def coin():
    return doc(f'<ellipse cx="64" cy="64" rx="38" ry="38" fill="#e0b34d" {outline("")}/>'
               f'<ellipse cx="64" cy="64" rx="28" ry="28" fill="none" stroke="#8a6a2e" stroke-width="4"/>'
               f'<path d="M64 46 l6 12 l13 2 l-9 10 l2 13 l-12 -6 l-12 6 l2 -13 l-9 -10 l13 -2 Z" fill="#8a6a2e"/>'
               f'<path d="M44 44 q10 -12 24 -14" fill="none" stroke="#fff" stroke-width="4" opacity=".45" stroke-linecap="round"/>')


def log():
    return doc(f'<rect x="22" y="46" width="84" height="36" rx="16" fill="#8a6a3a" {outline("")}/>'
               f'<ellipse cx="100" cy="64" rx="12" ry="18" fill="#b98d52" {outline("")}/>'
               f'<ellipse cx="100" cy="64" rx="6" ry="9" fill="#8a6a3a"/>'
               f'<path d="M30 54 h56" stroke="#a8814a" stroke-width="3" opacity=".7"/>'
               f'<path d="M30 74 h56" stroke="#6f5330" stroke-width="3" opacity=".7"/>')


def ore():
    return doc(f'<path d="M22 96 L40 40 L74 32 L106 74 L92 102 L34 104 Z" fill="#7b8093" {outline("")}/>'
               f'<path d="M40 40 L74 32 L80 62 L52 70 Z" fill="#939ab0"/>'
               f'<path d="M56 56 l14 -8 l10 16 l-14 12 Z" fill="#5fc8ff" {outline("")}/>'
               f'<path d="M74 78 l12 -6 l6 12 l-12 8 Z" fill="#e0b34d" {outline("")}/>')


def herb():
    return doc(f'<path d="M64 106 q-4 -40 0 -62" stroke="#4f7a3a" stroke-width="5" fill="none" stroke-linecap="round"/>'
               f'<path d="M64 62 q-26 -6 -30 -26 q26 -4 30 26 Z" fill="#6fbf5f" {outline("")}/>'
               f'<path d="M64 74 q26 -6 30 -26 q-26 -4 -30 26 Z" fill="#5aa84c" {outline("")}/>'
               f'<path d="M64 46 q-8 -18 0 -28 q8 10 0 28 Z" fill="#7fd06a" {outline("")}/>')


def fish():
    return doc(f'<path d="M24 64 q22 -26 52 -26 q26 0 28 26 q-2 26 -28 26 q-30 0 -52 -26 Z" fill="#6fb6d8" {outline("")}/>'
               f'<path d="M104 64 l18 -16 l-4 16 l4 16 Z" fill="#4a8fb0" {outline("")}/>'
               f'<circle cx="42" cy="58" r="4" fill="{INK}"/>'
               f'<path d="M46 72 q14 8 28 0" fill="none" stroke="#3f7d99" stroke-width="3"/>')


def bread():
    return doc(f'<path d="M24 74 q6 -34 40 -34 q34 0 40 34 q-2 20 -40 20 q-38 0 -40 -20 Z" fill="#d8a25c" {outline("")}/>'
               f'<path d="M40 60 q10 -10 24 -10 q14 0 24 10" fill="none" stroke="#b37f3a" stroke-width="4"/>'
               f'<path d="M50 74 h28 M46 82 h36" stroke="#b37f3a" stroke-width="4" stroke-linecap="round"/>')


def lockpick():
    return doc(f'<path d="M30 84 q-10 -10 0 -20 q10 -10 20 0 q10 10 0 20 q-10 10 -20 0 Z" fill="#c9ced9" {outline("")}/>'
               f'<path d="M50 70 L100 34" stroke="#c9ced9" stroke-width="8" stroke-linecap="round"/>'
               f'<path d="M96 30 l10 6 l-8 8 Z" fill="#c9ced9" {outline("")}/>')


def relic():
    return doc(f'<path d="M40 44 h48 l-6 46 q-18 10 -36 0 Z" fill="#c9a227" {outline("")}/>'
               f'<path d="M40 44 h48 l-2 12 h-44 Z" fill="#8a6a2e" {outline("")}/>'
               f'<circle cx="64" cy="70" r="10" fill="#e2556a" {outline("")}/>'
               f'<path d="M46 40 q18 -12 36 0" fill="none" stroke="#c9a227" stroke-width="5"/>')


def gear_icon(kind, c="#c9ced9", c2="#8a6a3a"):
    if kind == "sword":
        return doc(w_sword(64, 70, blade=c, hilt=c2, scale=1.5))
    if kind == "axe":
        return doc(w_axe(64, 68, head=c, haft=c2, scale=1.4))
    if kind == "bow":
        return doc(w_bow(64, 64, wood=c2, scale=1.4))
    if kind == "staff":
        return doc(w_staff(64, 66, orb="#7ad0ff", wood=c2, scale=1.4))
    if kind == "dagger":
        return doc(w_dagger(64, 74, blade=c, scale=1.6))
    if kind == "shield":
        return doc(w_shield(64, 62, base=c, trim="#e0b34d", scale=1.5))
    if kind == "armor":
        return doc(f'<path d="M64 26 q-26 2 -24 20 q2 18 6 24 l18 8 l18 -8 q4 -6 6 -24 q2 -18 -24 -20 Z" fill="{c}" {outline("")}/>'
                   f'<path d="M64 40 v40" stroke="{INK}" stroke-width="3"/>'
                   f'<path d="M44 44 q20 -10 40 0" fill="none" stroke="#fff" stroke-width="3" opacity=".4"/>')
    if kind == "helm":
        return doc(f'<path d="M64 22 q-26 2 -26 26 q0 20 10 26 h32 q10 -6 10 -26 q0 -24 -26 -26 Z" fill="{c}" {outline("")}/>'
                   f'<rect x="48" y="48" width="32" height="7" rx="3" fill="{INK}"/>'
                   f'<path d="M64 24 v-8" stroke="{c2}" stroke-width="5"/>')
    if kind == "boots":
        return doc(f'<path d="M38 34 h20 v44 q10 4 12 14 h-32 q-6 -2 -4 -12 Z" fill="{c}" {outline("")}/>'
                   f'<path d="M70 34 h20 v44 q10 4 12 14 h-32 q-6 -2 -4 -12 Z" fill="{c}" {outline("")}/>')
    if kind == "ring":
        return doc(f'<circle cx="64" cy="70" r="24" fill="none" stroke="#e0b34d" stroke-width="9"/>'
                   f'<circle cx="64" cy="70" r="24" fill="none" stroke="{INK}" stroke-width="2"/>'
                   f'<path d="M64 30 l10 12 l-10 14 l-10 -14 Z" fill="{c}" {outline("")}/>')
    if kind == "amulet":
        return doc(f'<path d="M40 30 q24 30 48 0" fill="none" stroke="#e0b34d" stroke-width="5"/>'
                   f'<path d="M64 52 l16 16 l-16 24 l-16 -24 Z" fill="{c}" {outline("")}/>')
    return doc(el(64, 64, 30, 30, c))


# ----------------------------------------------------------------- places
def place(kind):
    if kind == "town":
        return doc(shadow(64, 112, 40, 8) +
                   f'<rect x="26" y="56" width="76" height="52" rx="4" fill="#b98d52" {outline("")}/>'
                   f'<path d="M18 58 L64 26 L110 58 Z" fill="#a04a3a" {outline("")}/>'
                   f'<rect x="54" y="76" width="20" height="32" rx="3" fill="#5a3a22" {outline("")}/>'
                   f'<rect x="34" y="68" width="14" height="14" rx="2" fill="#7ad0ff" {outline("")}/>'
                   f'<rect x="80" y="68" width="14" height="14" rx="2" fill="#7ad0ff" {outline("")}/>'
                   f'<rect x="58" y="34" width="12" height="20" fill="#8a6a3a" {outline("")}/>')
    if kind == "tree":
        return doc(shadow(64, 112, 30, 7) +
                   f'<rect x="56" y="70" width="16" height="42" rx="4" fill="#6a4a2a" {outline("")}/>'
                   f'<ellipse cx="64" cy="52" rx="40" ry="34" fill="#4f8a4a" {outline("")}/>'
                   f'<ellipse cx="50" cy="42" rx="20" ry="16" fill="#67ab5c" opacity=".85"/>'
                   f'<ellipse cx="80" cy="60" rx="16" ry="12" fill="#3f733c" opacity=".7"/>')
    if kind == "cave":
        return doc(shadow(64, 112, 38, 8) +
                   f'<path d="M14 108 q0 -70 50 -70 q50 0 50 70 Z" fill="#6b6480" {outline("")}/>'
                   f'<path d="M40 108 q0 -40 24 -40 q24 0 24 40 Z" fill="#1a1626"/>'
                   f'<circle cx="46" cy="60" r="4" fill="#5fc8ff" opacity=".8"/>'
                   f'<circle cx="82" cy="52" r="3" fill="#5fc8ff" opacity=".6"/>')
    if kind == "mountain":
        return doc(shadow(64, 112, 42, 8) +
                   f'<path d="M6 106 L40 40 L74 106 Z" fill="#7b8093" {outline("")}/>'
                   f'<path d="M56 106 L88 46 L120 106 Z" fill="#9aa0b8" {outline("")}/>'
                   f'<path d="M40 40 L30 62 L50 62 Z" fill="#e8ecf5"/>'
                   f'<path d="M88 46 L79 66 L97 66 Z" fill="#f2f5fb"/>')
    if kind == "temple":
        return doc(shadow(64, 112, 40, 8) +
                   f'<path d="M64 20 L110 48 L18 48 Z" fill="#e6dcc0" {outline("")}/>'
                   f'<rect x="24" y="48" width="80" height="8" fill="#c9b98e" {outline("")}/>'
                   + "".join(f'<rect x="{x}" y="56" width="9" height="42" fill="#e6dcc0" {outline("")}/>' for x in (28, 46, 64, 82)) +
                   f'<rect x="18" y="98" width="92" height="10" rx="3" fill="#c9b98e" {outline("")}/>')
    if kind == "ruins":
        return doc(shadow(64, 112, 38, 8) +
                   f'<rect x="40" y="46" width="48" height="64" fill="#6b6480" {outline("")}/>'
                   f'<path d="M36 46 L64 20 L92 46 Z" fill="#5a5470" {outline("")}/>'
                   f'<rect x="54" y="76" width="20" height="34" fill="#1a1626"/>'
                   f'<path d="M92 60 l14 -6 l-2 24 l-12 4 Z" fill="#5a5470" {outline("")}/>'
                   f'<circle cx="64" cy="58" r="5" fill="#b45cff" opacity=".85"/>')
    if kind == "camp":
        return doc(shadow(64, 112, 40, 8) +
                   f'<path d="M34 96 L64 44 L94 96 Z" fill="#7a5a3a" {outline("")}/>'
                   f'<path d="M64 44 L64 96" stroke="{INK}" stroke-width="3"/>'
                   f'<path d="M64 58 L74 96 L54 96 Z" fill="#3a2a1a"/>'
                   f'<circle cx="98" cy="88" r="10" fill="#ff8a3a" opacity=".9"/>'
                   f'<circle cx="98" cy="88" r="5" fill="#ffd36b"/>')
    # depths
    return doc(f'<circle cx="64" cy="64" r="50" fill="#b45cff" opacity=".14"/>' +
               f'<path d="M20 108 q0 -76 44 -76 q44 0 44 76 Z" fill="#2a2240" {outline("")}/>' +
               f'<path d="M44 108 q0 -44 20 -44 q20 0 20 44 Z" fill="#0d0a18"/>' +
               f'<circle cx="64" cy="52" r="12" fill="#b45cff" opacity=".55"/>' +
               f'<circle cx="64" cy="52" r="6" fill="#e6b3ff"/>' +
               "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#b45cff" opacity=".7"/>'
                       for x, y in [(36, 70), (92, 62), (30, 92), (98, 88), (52, 40), (80, 34)]))


# ----------------------------------------------------------------- statuses
def status(kind):
    c = {
        "bleed": "#e04a4a", "poison": "#6fbf5f", "burn": "#ff8a3a", "stun": "#ffd36b",
        "weaken": "#8a7fd0", "shield": "#5fc8ff", "rage": "#ff5a3a", "regen": "#5fe08a",
        "focus": "#e0b34d", "mark": "#d15cff",
    }.get(kind, "#c9ced9")
    g = [f'<circle cx="64" cy="64" r="42" fill="{c}" opacity=".16"/>']
    if kind == "bleed":
        g.append(f'<path d="M64 26 q18 26 18 40 q0 18 -18 18 q-18 0 -18 -18 q0 -14 18 -40 Z" fill="{c}" {outline("")}/>')
        g.append(f'<path d="M56 62 q4 10 12 12" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
    elif kind == "poison":
        g.append(f'<path d="M64 26 q20 22 20 38 q0 20 -20 20 q-20 0 -20 -20 q0 -16 20 -38 Z" fill="{c}" {outline("")}/>')
        g.append(f'<circle cx="58" cy="64" r="4" fill="#e6ffe6"/><circle cx="70" cy="72" r="3" fill="#e6ffe6"/>')
    elif kind == "burn":
        g.append(f'<path d="M64 24 q16 20 16 34 q0 22 -16 22 q-16 0 -16 -22 q0 -14 16 -34 Z" fill="{c}" {outline("")}/>')
        g.append(f'<path d="M64 46 q8 12 8 20 q0 12 -8 12 q-8 0 -8 -12 q0 -8 8 -20 Z" fill="#ffe08a"/>')
    elif kind == "stun":
        g.append(f'<path d="M64 30 l10 20 l22 4 l-16 16 l4 22 l-20 -12 l-20 12 l4 -22 l-16 -16 l22 -4 Z" fill="{c}" {outline("")}/>')
    elif kind == "weaken":
        g.append(f'<path d="M64 28 l16 12 l-6 44 l-10 12 l-10 -12 l-6 -44 Z" fill="{c}" {outline("")}/>')
        g.append(f'<path d="M52 60 l24 12" stroke="{INK}" stroke-width="4"/>')
    elif kind == "shield":
        g.append(f'<path d="M64 24 L94 38 L90 76 Q64 100 38 76 L34 38 Z" fill="{c}" {outline("")}/>')
        g.append(f'<path d="M64 34 L84 44 L82 70 Q64 88 46 70 L44 44 Z" fill="none" stroke="#eaf7ff" stroke-width="3"/>')
    elif kind == "rage":
        g.append(f'<path d="M64 26 l8 26 l24 -8 l-16 20 l18 14 l-26 2 l2 24 l-10 -20 l-10 20 l2 -24 l-26 -2 l18 -14 l-16 -20 l24 8 Z" fill="{c}" {outline("")}/>')
    elif kind == "regen":
        g.append(f'<path d="M64 94 q-30 -18 -30 -40 q0 -20 18 -20 q8 0 12 8 q4 -8 12 -8 q18 0 18 20 q0 22 -30 40 Z" fill="{c}" {outline("")}/>')
        g.append(f'<path d="M52 52 h24 M64 40 v24" stroke="#eaffef" stroke-width="4"/>')
    elif kind == "focus":
        g.append(f'<circle cx="64" cy="64" r="26" fill="none" stroke="{c}" stroke-width="7"/>')
        g.append(f'<circle cx="64" cy="64" r="10" fill="{c}"/>')
        g.append(f'<path d="M64 26 v10 M64 92 v10 M26 64 h10 M92 64 h10" stroke="{c}" stroke-width="6" stroke-linecap="round"/>')
    else:
        g.append(f'<path d="M64 24 l12 24 l26 4 l-19 18 l5 26 l-24 -13 l-24 13 l5 -26 l-19 -18 l26 -4 Z" fill="none" stroke="{c}" stroke-width="6"/>')
        g.append(f'<circle cx="64" cy="64" r="8" fill="{c}"/>')
    return doc("".join(g))


# ----------------------------------------------------------------- assembly
SPRITES = {}

def add(key, svg):
    SPRITES[key] = svg

# enemies
add("enemy.rat", beast("#9a9086", "#6a6058", "#e04a4a", ears="round", tail=True, size=0.8))
add("enemy.wolf", beast("#8a8f9e", "#5c6070", "#ffd36b"))
add("enemy.boar", beast("#8a6a52", "#5a4536", "#ffd36b", tusks=True, size=1.05))
add("enemy.goblin", brute("#7fa25e", "#4f6b3a", "#6b4a2a", "#c9a227", horns=False, size=0.85, weapon="dagger"))
add("enemy.ogre", brute("#c98f6a", "#8a5a3a", "#5a3a22", "#c9a227", size=1.25, weapon="club"))
add("enemy.bandit", humanoid("#c98f6a", "#4a3a2a", "#7a5a3a", "#b03a3a", weapon="dagger", hood="#3a2a1a"))
add("enemy.rogue_mage", humanoid("#d8a273", "#4a2a6a", "#5a3a86", "#b45cff", weapon="staff", hood="#3a2450"))
add("enemy.assassin", humanoid("#b98f6a", "#22202e", "#3a3850", "#8a90a8", weapon="twin", hood="#22202e"))
add("enemy.bat", doc(shadow(64, 96, 24, 6) +
    f'<path d="M64 52 q-30 -20 -48 -6 q16 6 20 24 q10 -8 28 -6 Z" fill="#6a5a86" {outline("")}/>'
    f'<path d="M64 52 q30 -20 48 -6 q-16 6 -20 24 q-10 -8 -28 -6 Z" fill="#6a5a86" {outline("")}/>'
    f'<ellipse cx="64" cy="62" rx="14" ry="16" fill="#8a7aa6" {outline("")}/>'
    + eyes(64, 60, 5, 2.4, glow="#ffd36b") +
    f'<path d="M56 44 l-4 -10 l8 6 Z" fill="#8a7aa6" {outline("")}/><path d="M72 44 l4 -10 l-8 6 Z" fill="#8a7aa6" {outline("")}/>'))
add("enemy.spider", doc(shadow(64, 104, 28, 7) +
    f'<ellipse cx="64" cy="70" rx="26" ry="20" fill="#6a3f8a" {outline("")}/>'
    + "".join(f'<path d="M64 70 Q{64+dx*30} {70+dy*30-14} {64+dx*44} {70+dy*34}" fill="none" stroke="#3a2450" stroke-width="5" stroke-linecap="round"/>'
              for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]) +
    f'<ellipse cx="64" cy="48" rx="15" ry="13" fill="#8a5aa8" {outline("")}/>'
    + eyes(64, 46, 6, 2.6, glow="#ff6ad5")))
add("enemy.golem", construct())
add("enemy.wraith", undead("wraith"))
add("enemy.harpy", doc(shadow(64, 112, 22, 6) +
    f'<path d="M64 46 q-34 -26 -52 -10 q20 4 24 26 q12 -12 28 -6 Z" fill="#a8845c" {outline("")}/>'
    f'<path d="M64 46 q34 -26 52 -10 q-20 4 -24 26 q-12 -12 -28 -6 Z" fill="#a8845c" {outline("")}/>'
    f'<ellipse cx="64" cy="66" rx="14" ry="22" fill="#c9a07a" {outline("")}/>'
    f'<ellipse cx="64" cy="40" rx="12" ry="12" fill="#d8b48f" {outline("")}/>'
    + eyes(64, 38, 5, 2.2) +
    f'<path d="M58 48 l6 8 l6 -8 Z" fill="#e0b34d" {outline("")}/>'
    f'<path d="M58 92 l-6 18 M70 92 l6 18" stroke="#c9a07a" stroke-width="5" stroke-linecap="round"/>'))
add("enemy.wyvern", doc(shadow(64, 112, 32, 8) +
    f'<path d="M64 44 q-38 -30 -58 -12 q24 6 28 30 q14 -14 30 -8 Z" fill="#8a3a2a" {outline("")}/>'
    f'<path d="M64 44 q38 -30 58 -12 q-24 6 -28 30 q-14 -14 -30 -8 Z" fill="#8a3a2a" {outline("")}/>'
    f'<ellipse cx="64" cy="72" rx="22" ry="18" fill="#b04a34" {outline("")}/>'
    f'<ellipse cx="50" cy="48" rx="14" ry="12" fill="#c05a40" {outline("")}/>'
    + eyes(46, 46, 5, 2.4, glow="#ffd36b") +
    f'<path d="M36 52 l-12 6 l12 4 Z" fill="#e0b34d" {outline("")}/>'
    f'<path d="M92 70 q20 -4 24 -20 q-6 20 -24 24 Z" fill="#8a3a2a" {outline("")}/>'))
add("enemy.coven", boss("coven"))
add("enemy.warden", boss("warden"))
add("enemy.warlord", boss("warlord"))
add("enemy.spider_queen", boss("spider_queen"))
add("enemy.bog_horror", boss("bog_horror"))

# classes
add("class.warrior", humanoid("#d8a273", "#5b4a86", "#8f95ad", "#e0b34d", weapon="sword"))
add("class.berserker", humanoid("#c98f6a", "#6a2f2f", "#8a5a3a", "#e8574a", weapon="axe", big=0.4))
add("class.defender", humanoid("#d8a273", "#3f5a86", "#9aa0b8", "#5fc8ff", weapon="shield", big=0.3))
add("class.archer", humanoid("#d8a273", "#4a6a3a", "#6a5a3a", "#7fd06a", weapon="bow"))
add("class.thief", humanoid("#b98f6a", "#2a2a3a", "#4a4a5e", "#8a90a8", weapon="twin", hood="#22222e"))
add("class.swordmaster", humanoid("#d8a273", "#5a4a3a", "#c9ced9", "#e0b34d", weapon="sword"))
add("class.duelist", humanoid("#c98f6a", "#3a3a5a", "#8f95ad", "#9ad0ff", weapon="twin"))
add("class.mage", humanoid("#d8a273", "#3a2a5a", "#5a3a86", "#b45cff", weapon="staff", hood="#2a1a44"))

# races
add("race.human", humanoid("#d8a273", "#6a5a8a", "#9aa0b8", "#e0b34d", weapon="sword"))
add("race.elf", humanoid("#e8d0b0", "#3a6a4a", "#7a9a6a", "#a8e0b0", weapon="bow"))
add("race.dwarf", humanoid("#c98f6a", "#6a4a2a", "#a88a5a", "#e0b34d", weapon="axe", big=0.35))
add("race.orc", brute("#7fa25e", "#4f6b3a", "#5a3a22", "#c9a227", horns=False, weapon="axe"))
add("race.halfling", humanoid("#e0b48a", "#7a6a3a", "#a89a6a", "#d8c060", weapon="dagger"))
add("race.tiefling", humanoid("#c0708a", "#5a2a4a", "#8a4a6a", "#ff6ad5", weapon="staff", hood="#3a1a2e"))
add("race.beastkin", humanoid("#c9a07a", "#6a5a3a", "#8a7a4a", "#e0b34d", weapon="dagger", big=0.15))
add("race.revenant", undead("skull"))

# companions
add("companion.bryn", humanoid("#c98f6a", "#3f5a86", "#9aa0b8", "#5fc8ff", weapon="shield", big=0.35))
add("companion.sylva", humanoid("#e8d0b0", "#3a6a4a", "#7a9a6a", "#a8e0b0", weapon="bow"))
add("companion.mordecai", humanoid("#b09a86", "#3a2a5a", "#5a3a86", "#b45cff", weapon="staff", hood="#2a1a44"))
add("companion.pip", humanoid("#e0b48a", "#7a6a3a", "#a89a6a", "#d8c060", weapon="dagger"))
add("companion.sister_maeve", humanoid("#e8d0b0", "#e6dcc0", "#c9b98e", "#ffd36b", weapon="staff"))

# player (per class, brighter accent so the hero reads)
for c in ("warrior", "berserker", "defender", "archer", "thief", "swordmaster", "duelist", "mage"):
    add("player." + c, SPRITES["class." + c])

# items
add("item.potion", flask("#d15cff"))
add("item.ether", flask("#5fc8ff"))
add("item.antidote", flask("#6fbf5f"))
add("item.wood", log())
add("item.iron", ore())
add("item.ore", ore())
add("item.leather", doc(f'<path d="M24 40 q40 -14 80 0 q-4 30 -14 44 q-26 10 -52 0 q-10 -14 -14 -44 Z" fill="#a8743f" {outline("")}/>'
                        f'<path d="M34 48 q30 -8 60 0" fill="none" stroke="#c99a5f" stroke-width="4"/>'))
add("item.ruby", gemstone("#e2556a", "#8a1f34"))
add("item.herb", herb())
add("item.food", bread())
add("item.fish", fish())
add("item.lockpick", lockpick())
add("item.relic", relic())

# gear
add("gear.dagger", gear_icon("dagger"))
add("gear.hand_axe", gear_icon("axe"))
add("gear.hunting_bow", gear_icon("bow"))
add("gear.steel_sword", gear_icon("sword"))
add("gear.runic_blade", gear_icon("sword", "#8fd0ff", "#4a3a6a"))
add("gear.dragonfang", gear_icon("sword", "#e0b34d", "#7a2f2f"))
add("gear.twin_dagger", gear_icon("dagger", "#c9ced9", "#3a3a5a"))
add("gear.katana", gear_icon("sword", "#e8ecf5", "#3a2a2a"))
add("gear.arcane_staff", gear_icon("staff"))
add("gear.iron_plate", gear_icon("armor", "#9aa0b8"))
add("gear.leather_armor", gear_icon("armor", "#a8743f"))
add("gear.dragonscale", gear_icon("armor", "#c05a40"))
add("gear.iron_helm", gear_icon("helm", "#9aa0b8"))
add("gear.swift_boots", gear_icon("boots", "#8a6a3a"))
add("gear.ruby_ring", gear_icon("ring", "#e2556a"))
add("gear.guardian_amulet", gear_icon("amulet", "#5fc8ff"))

# locations
for k in ("oakhaven", "mire", "cave", "mountains", "temple", "ruins", "banditcamp", "depths"):
    add("loc." + k, place({"oakhaven": "town", "mire": "tree", "cave": "cave", "mountains": "mountain",
                           "temple": "temple", "ruins": "ruins", "banditcamp": "camp", "depths": "depths"}[k]))

# gems
for k, (c1, c2) in {"ruby": ("#e2556a", "#8a1f34"), "sapphire": ("#5fa8ff", "#1f3a8a"),
                    "emerald": ("#4fd88a", "#1f6a3a"), "topaz": ("#ffd36b", "#8a6a1a"),
                    "amethyst": ("#b45cff", "#5a1a8a"), "diamond": ("#cfefff", "#5a8aa8"),
                    "onyx": ("#6a6a80", "#1a1a24")}.items():
    add("gem." + k, gemstone(c1, c2))

# statuses
for k in ("bleed", "poison", "burn", "stun", "weaken", "shield", "rage", "regen", "focus", "mark"):
    add("status." + k, status(k))

# ----------------------------------------------------------------- write
written = []
for key, svg in SPRITES.items():
    fn = key.replace(".", "_") + ".svg"
    (SPR / fn).write_text(svg, encoding="utf-8")
    written.append((key, fn))

print(f"Wrote {len(written)} SVG models to {SPR}")

# HD raster copies (optional but handy for tools that want bitmaps)
try:
    import cairosvg
    made = 0
    for key, fn in written:
        cairosvg.svg2png(url=str(SPR / fn), write_to=str(HD / (fn[:-4] + ".png")),
                         output_width=256, output_height=256)
        made += 1
    print(f"Rasterised {made} HD PNGs to {HD}")
except Exception as e:  # pragma: no cover
    print("CairoSVG unavailable, skipping HD raster:", e)

# ----------------------------------------------------------------- mod file
sprite_lines = "".join(f'      "{k}": "{f}",\n' for k, f in written)
mod = """/* ============================================================
   CHRONICLES — vector art overhaul (generated by
   tools/make-overhaul-art.py). A graphics pack, not an engine change.
   Select it in Settings -> Graphics pack.
   ============================================================ */
window.AETHELGARD_MODS = window.AETHELGARD_MODS || [];

window.AETHELGARD_MODS.push({
  id: "overhaul-vector",
  name: "Chronicles Vector Overhaul",
  version: "1.0.0",
  author: "Dr. Sohil Momin",
  description: "Illustrated vector models for every enemy, class, race, item and region. Crisp at any size.",
  impact: "additive",

  GRAPHICS: {
    id: "chronicles-vector",
    name: "Chronicles (vector)",
    base: "mods/overhaul-vector/sprites/",
    pixel: false,
    scale: 1.25,
    sprites: {
""" + sprite_lines + """    },
  },
});
"""
(PACK / "mod.js").write_text(mod, encoding="utf-8")
print("Wrote", PACK / "mod.js")
