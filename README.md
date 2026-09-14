# Mathesis

*Mathesis* is not a finished book — it's a working record of an ongoing
attempt to understand mathematics from first principles: logic, sets,
algebra, analysis, and onward. It's released one booklet at a time, and
each booklet is written the way the ideas are actually being learned,
not polished into a textbook after the fact.

Some chapters are fully written. A lot of them are still **outlines** —
a title, a one-paragraph statement of what the chapter needs to
establish, why it matters, and what it depends on. That's intentional,
not unfinished business hidden from you: an outline chapter says so
plainly, right where it appears. See
[`booklets/shared/en/frontmatter/how-to-read.tex`](booklets/shared/en/frontmatter/how-to-read.tex)
for the full explanation, or `booklets/shared/fa/frontmatter/how-to-read.tex`
for the Persian version.

It sits alongside two companion projects by the same author: **Arliz**
(data and computation from the transistor up) and **The Art of
Algorithmic Analysis** (analyzing algorithms rigorously).

## The booklets

Fourteen independent booklets, each covering one branch of mathematics,
each buildable on its own, in **English** and **Persian**:

| # | Booklet |
|---|---|
| 01 | Mathematical Logic and Proof Theory |
| 02 | Set Theory |
| 03 | Linear Algebra |
| 04 | Abstract Algebra |
| 05 | Number Theory |
| 06 | Combinatorics and Graph Theory |
| 07 | Real Analysis and Measure Theory |
| 08 | Complex Analysis and Harmonic Analysis |
| 09 | Topology |
| 10 | Differential Geometry |
| 11 | Probability Theory |
| 12 | Functional Analysis and Spectral Theory |
| 13 | Category Theory and Universal Structures |
| 14 | Metamathematics |

The Persian edition of every booklet has its frontmatter and backmatter
(title, copyright, about pages, how-to-read, references) fully
translated. Chapters themselves are translated as they're written in
English, not before — so a Persian booklet's chapter files are often
still a one-line placeholder pointing back to the English original.

## Quick start

You'll need `pdflatex` and `xelatex` (English booklets build with
`pdflatex`, Persian ones with `xelatex`), `biber` for references, and
either `rsvg-convert` or `cairosvg` on `PATH` to turn each cover's
`cover.svg` into a `cover.pdf`. See [Requirements](#requirements) below
for exact package names.

```bash
make list                                          # every booklet + build status
make booklet SLUG=1                                # build booklet 01, both languages
make booklet SLUG=01-mathematical-logic-and-proof-theory LANG=en
make watch SLUG=3 LANG=en                          # rebuild on save
make new-booklet SLUG=15-new-topic                 # scaffold booklet 15
make build                                         # everything, every language
make clean                                         # remove build artifacts
```

`SLUG` accepts either the numeric index shown by `make list` or the
full slug. Every command also works through the underlying script
directly: `python3 scripts/px.py booklets <command>`.

Finished PDFs land in `build/booklets/<OUTPUT_NAME>.pdf` (the name each
booklet's `.conf` file sets, e.g. `Mamashli-Mathematical-Logic-EN.pdf`).

## License

Each booklet is released under CC BY-SA 4.0 --- share and adapt freely,
including commercially, with attribution and under the same license;
see that booklet's own copyright page for details.

Source: <https://github.com/papyrxis/mathesis>
