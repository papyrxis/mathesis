#!/usr/bin/env python3
"""
Generate the missing fa/frontmatter/cover.svg for every booklet, mirroring
the existing en/frontmatter/cover.svg design (same layout, same palette)
but in Persian, right-to-left, set in Amiri (title) and Vazirmatn (labels)
so it matches the fonts already used through the rest of the fa edition.

Run once from the project root:
    python3 scripts/tools/gen_fa_covers.py
"""
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONF_DIR = ROOT / "configs" / "booklets"
BOOKLETS_DIR = ROOT / "booklets"

BG_TOP = "#0A0E1A"
BG_BOTTOM = "#131A2C"
GOLD = "#C9A467"
CREAM = "#EDE7D9"
MUTED_GOLD = "#B79A6E"
FOOTER_GRAY = "#7C879C"

TITLE_FONT = "Amiri, 'Noto Naskh Arabic', serif"
LABEL_FONT = "Vazirmatn, Tahoma, sans-serif"


def parse_conf(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields = {}
    for m in re.finditer(r'^([A-Z_]+)="((?:[^"\\]|\\.)*)"', text, re.MULTILINE):
        fields[m.group(1)] = m.group(2)
    return fields


def wrap_by_chars(text: str, max_chars: int, max_lines: int) -> list[str]:
    """Word-wrap RTL-safe: textwrap works fine since it only reorders
    whitespace-delimited tokens, never reverses characters."""
    lines = textwrap.wrap(text, width=max_chars, break_long_words=False)
    if len(lines) <= max_lines:
        return lines
    # Too long even at max_lines: widen the wrap until it fits.
    width = max_chars
    while len(lines) > max_lines and width < max_chars * 2:
        width += 4
        lines = textwrap.wrap(text, width=width, break_long_words=False)
    return lines[:max_lines]


def build_svg(fields: dict, number: str) -> str:
    title = fields["BOOKLET_TITLE"]
    subtitle = fields.get("BOOKLET_SUBTITLE", "")
    author = fields.get("BOOKLET_AUTHOR", "")
    handle = fields.get("BOOKLET_AUTHOR_HANDLE", "")
    year = fields.get("BOOKLET_YEAR", "")
    edition = fields.get("BOOKLET_EDITION", "")

    title_lines = wrap_by_chars(title, 17, 2)
    subtitle_lines = wrap_by_chars(subtitle, 34, 2) if subtitle else []

    # Vertical layout mirrors the en/ cover: ornament ~232, title starts
    # ~330 growing downward, rule + subtitle follow, then author block
    # pinned near the bottom at the same y-coordinates as the EN cover.
    title_font_size = 58 if len(title_lines) == 2 else 62
    line_height = 74
    title_start_y = 330 if len(title_lines) == 1 else 322
    title_tspans = "\n".join(
        f'    <tspan x="500.0" y="{title_start_y + i * line_height}">{line}</tspan>'
        for i, line in enumerate(title_lines)
    )
    rule_y = title_start_y + (len(title_lines) - 1) * line_height + 56

    subtitle_start_y = rule_y + 62
    subtitle_tspans = "\n".join(
        f'    <tspan x="500.0" y="{subtitle_start_y + i * 40}">{line}</tspan>'
        for i, line in enumerate(subtitle_lines)
    )

    edition_line = " ".join(p for p in [edition, year] if p) or edition or year

    return f'''<svg viewBox="0 0 1000 1420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="100%" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1000" height="1420" fill="url(#bg)"/>

  <text x="500.0" y="150" text-anchor="middle" direction="rtl"
        font-family="{LABEL_FONT}" font-size="20"
        letter-spacing="3" fill="{GOLD}">متسیس &#183; کتابچه‌ی {number}</text>

  <g transform="translate(500.0,232)">
    <rect x="-22" y="-22" width="44" height="44"
          transform="rotate(45)" fill="none" stroke="{GOLD}"
          stroke-width="1.6" opacity="0.9"/>
    <circle cx="0" cy="0" r="4.2" fill="{GOLD}"/>
  </g>

  <text x="500.0" text-anchor="middle" direction="rtl"
        font-family="{TITLE_FONT}" font-weight="700"
        font-size="{title_font_size}" fill="{CREAM}">
{title_tspans}
  </text>

  <line x1="410.0" y1="{rule_y}" x2="590.0" y2="{rule_y}"
        stroke="{GOLD}" stroke-width="1.4"/>

  <text x="500.0" text-anchor="middle" direction="rtl"
        font-family="{TITLE_FONT}" font-style="italic"
        font-size="25" fill="{MUTED_GOLD}">
{subtitle_tspans}
  </text>

  <text x="500.0" y="1225" text-anchor="middle" direction="rtl"
        font-family="{TITLE_FONT}" font-weight="700"
        font-size="30" fill="{CREAM}">{author}</text>
  <text x="500.0" y="1268" text-anchor="middle"
        font-family="{LABEL_FONT}" font-size="19"
        letter-spacing="4" fill="{GOLD}">{handle.upper()}</text>
  <text x="500.0" y="1302" text-anchor="middle" direction="rtl"
        font-family="{LABEL_FONT}" font-size="16"
        fill="{FOOTER_GRAY}">{edition_line}</text>
</svg>
'''


def main():
    conf_files = sorted(CONF_DIR.glob("*-fa.conf"))
    if not conf_files:
        raise SystemExit(f"No fa .conf files found in {CONF_DIR}")

    written = []
    for conf_path in conf_files:
        fields = parse_conf(conf_path)
        slug = conf_path.name[: -len("-fa.conf")]
        number = fields.get("BOOKLET_NUMBER", "")
        booklet_dir = BOOKLETS_DIR / slug / "fa" / "frontmatter"
        if not booklet_dir.exists():
            print(f"  [skip] {slug}: {booklet_dir} does not exist")
            continue
        out_path = booklet_dir / "cover.svg"
        out_path.write_text(build_svg(fields, number), encoding="utf-8")
        written.append(out_path.relative_to(ROOT))
        print(f"  [ok]   {out_path.relative_to(ROOT)}")

    print(f"\n{len(written)} fa cover.svg file(s) written.")


if __name__ == "__main__":
    main()
