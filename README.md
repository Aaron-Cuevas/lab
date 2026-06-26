# lab — replication workbench

A minimal, **AI-free** terminal tool for a personal practice of replicating
systems across three domains:

🔬 **Academic** · 🔩 **Industrial** · ❄️ **Natural**

It generates nothing for you. It automates the boring parts: write a LaTeX
insight and render it, push the PDF to the wiki, keep the GitHub/LaTeX guides
and research links one keystroke away, and log field notes to a separate repo.

---

## Quick start

```bash
gh repo create Aaron-Cuevas/lab --public --clone   # first time
cd lab
# copy these files in, then:
git add . && git commit -m "lab" && git push
python lab.py
```

Open the wiki once on the web (`<repo>/wiki` → *Create the first page* → save) so
the LaTeX insights have somewhere to land.

Needs: Python 3, git, and a LaTeX engine (`latexmk` or `pdflatex` — you already
have these). Optional but handy: GitHub CLI (`gh`).

---

## What it does

Run `lab` → an atom/nut/plant animation asks **"what will you replicate today?"**
You pick a domain, then:

```
[1] Wiki · LaTeX insight     write -> render PDF -> push to the wiki
[2] GitHub guide             git/GitHub cheat sheet (guides/github.md)
[3] LaTeX guide              math cheat sheet (guides/latex.md)
[4] Research resources       papers + free tools (resources.md)
[5] Field notes              new note in the separate field-notes repo
```

Subcommands (skip the menu):

```
lab insight        lab github     lab latex     lab resources     lab field
```

---

## The daily LaTeX → wiki flow

`lab insight` (or `[1]`):

1. Asks a title and the domain.
2. Creates `insights/<domain>/YYYY-MM-DD-slug.tex` from `templates/insight.tex`
   (math preamble ready: `amsmath`, `physics`, `siunitx`).
3. Opens your editor — you write the insight with equations, save and close.
4. Renders it to PDF (`latexmk`/`pdflatex`).
5. Commits the **.tex source** to this repo and pushes the **PDF to the wiki**,
   linking it from the domain's wiki page.

The `.tex` lives in the repo (version-controlled source); the rendered `.pdf`
lives in the wiki at
`raw.githubusercontent.com/wiki/Aaron-Cuevas/lab/<domain>/<file>.pdf`.

---

## Field notes (separate repo)

Field notes live in their **own repo**, `Aaron-Cuevas/field-notes`, on purpose —
a free space to work across topics and find patterns. Create it once:

```bash
gh repo create Aaron-Cuevas/field-notes --public --clone
```

Put it next to this repo (`../field-notes`), or set `LAB_FIELD_NOTES=/path`, or
add `FIELD_NOTES=/full/path` to a `.lab.cfg` file in this repo. Then `lab field`
writes a dated note there and pushes it.

---

## Structure
```
lab/
├── lab.py                  the tool
├── lab.bat / lab           launchers (Windows / Unix)
├── guides/
│   ├── github.md           git/GitHub cheat sheet
│   └── latex.md            LaTeX (math) cheat sheet
├── resources.md            research resources (papers, free tools)
├── templates/insight.tex   LaTeX template for the daily insight
├── insights/
│   ├── academic/           🔬  .tex sources
│   ├── industrial/         🔩
│   └── natural/            ❄️
└── .gitignore              (ignores LaTeX build leftovers)
```

The three domains mirror my GitHub Stars lists (Academic / Industrial / Natural).
