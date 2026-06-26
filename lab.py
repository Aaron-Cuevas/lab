#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lab — replication workbench for Aaron-Cuevas

A minimal terminal tool to run a personal, AI-free practice of replicating
systems across three domains:
    🔬 Academic   🔩 Industrial   ❄️ Natural

It does not generate anything for you. It just automates the boring parts:
write a LaTeX insight and render it, push the PDF to the wiki, keep guides and
research links one keystroke away, and log field notes to a separate repo.

Usage:
    lab                  intro + menu ("what will you replicate today?")
    lab insight          write a LaTeX insight, render it, push PDF to the wiki
    lab github           git/GitHub cheat sheet
    lab latex            LaTeX (math) cheat sheet
    lab resources        scientific research resources (papers, free tools)
    lab field            write a field note (separate field-notes repo)
    lab --help

Needs: Python 3, git, and a LaTeX engine (latexmk or pdflatex). Optional: gh.
"""

import os
import re
import sys
import time
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

USER = "Aaron-Cuevas"

# domain key -> (menu label, folder/page name)
DOMAINS = {
    "1": ("🔬 Academic Systems", "academic", "Academic"),
    "2": ("🔩 Industrial Systems", "industrial", "Industrial"),
    "3": ("❄️ Natural Systems", "natural", "Natural"),
}
TODAY = None  # chosen at startup: (label, folder, page)

# ----------------------------------------------------------------------- #
#  terminal helpers
# ----------------------------------------------------------------------- #

if os.name == "nt":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
def _c(x): return x if _COLOR else ""
CY, GR, DIM, BOLD, RST = _c("\033[36m"), _c("\033[32m"), _c("\033[2m"), _c("\033[1m"), _c("\033[0m")

def clear(): os.system("cls" if os.name == "nt" else "clear")
def w(s): sys.stdout.write(s); sys.stdout.flush()

def run(cmd, cwd=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", f"not found: {cmd[0]}"

def repo_root():
    code, out, _ = run(["git", "rev-parse", "--show-toplevel"])
    return out.strip() if code == 0 else None

def git_publish(repo_dir, paths, message):
    """add + commit + push in any repo dir. Safe if push fails."""
    run(["git", "pull", "--quiet", "--no-rebase"], cwd=repo_dir)
    run(["git", "add"] + paths, cwd=repo_dir)
    code, o, e = run(["git", "commit", "-m", message], cwd=repo_dir)
    if code != 0 and "nothing to commit" in (o + e):
        print(f"{DIM}Nothing new to publish.{RST}"); return True
    code, o, e = run(["git", "push"], cwd=repo_dir)
    if code != 0:
        print(f"{DIM}Committed locally, but push failed:{RST}")
        last = (e or o).strip().splitlines()[-1] if (e or o).strip() else ""
        print("  " + last + f"  ({BOLD}gh auth login{RST} or push manually)")
        return False
    print(f"{GR}Published \u2713{RST}"); return True

def open_editor(path):
    ed = os.environ.get("EDITOR")
    if ed:
        subprocess.call(ed.split() + [path])
    elif shutil.which("code"):
        subprocess.call(["code", "--wait", path])
    elif os.name == "nt":
        subprocess.call(["notepad", path])
    elif shutil.which("nano"):
        subprocess.call(["nano", path])
    else:
        subprocess.call(["vi", path])

def open_file(path):
    try:
        if os.name == "nt":
            os.startfile(path)               # noqa
        elif sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception:
        pass

def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "note"

def ask(label, default=""):
    extra = f" {DIM}[{default}]{RST}" if default else ""
    try:
        r = input(f"  {label}{extra}: ").strip()
    except EOFError:
        r = ""
    return r or default

# ----------------------------------------------------------------------- #
#  ASCII art: atom, nut, plant  (each 5 lines, width 11)
# ----------------------------------------------------------------------- #

def _atom(f):
    e = [(1, 4), (2, 9), (3, 4), (1, 2)][f % 4]  # electron (row, col)
    g = ["    ___    ",
         "  /     \\  ",
         " |  (+)  | ",
         "  \\ ___ /  ",
         "           "]
    row, col = e
    line = list(g[row]); line[col] = "o"; g[row] = "".join(line)
    return g

def _nut(f):
    s = "|/-\\"[f % 4]
    return ["   ____    ",
            "  /    \\   ",
            f" / ( {s} ) \\  ",
            "  \\    /   ",
            "   \\__/    "]

def _plant(f):
    return [
        ["           ", "           ", "     |     ", "    \\|/    ", "   __|__   ", ],
        ["     ^     ", "    \\|/    ", "   \\\\|//   ", "     |     ", "   __|__   ", ],
        ["    \\*/    ", "   \\\\|//   ", "    \\|/    ", "     |     ", "   __|__   ", ],
        ["     .     ", "     |     ", "    \\|/    ", "     |     ", "   __|__   ", ],
    ][f % 4]

def _join3(f):
    a, n, p = _atom(f), _nut(f), _plant(f)
    out = []
    for i in range(5):
        line = f"{CY}{a[i]}{RST}    {CY}{n[i]}{RST}    {GR}{p[i]}{RST}"
        out.append(line.center(64 + len(CY) * 3 + len(RST) * 3 + len(GR)))
    return out

def intro():
    clear()
    print("\n")
    block = _join3(0)
    for l in block:
        print(l)
    for f in range(1, 8):
        w("\033[5A")
        for l in _join3(f):
            w("\r\033[K" + l + "\n")
        time.sleep(0.16)
    labels = "        🔬 Academic        🔩 Industrial        ❄️ Natural"
    print(f"\n{DIM}{labels}{RST}")
    print(f"\n{BOLD}    What will you replicate today?{RST}")

def pick_domain():
    print()
    for k, (label, _, _) in DOMAINS.items():
        print(f"    [{k}] {label}")
    print(f"    {DIM}[enter] skip{RST}")
    try:
        sel = input(f"  {CY}>{RST} ").strip()
    except EOFError:
        sel = ""
    return DOMAINS.get(sel)

# ----------------------------------------------------------------------- #
#  wiki helpers (the lab repo's wiki holds the rendered PDFs)
# ----------------------------------------------------------------------- #

def _origin():
    code, out, _ = run(["git", "remote", "get-url", "origin"])
    return out.strip() if code == 0 else None

def _owner_repo(origin):
    s = origin.rstrip("/")
    if s.endswith(".git"):
        s = s[:-4]
    s = s.replace("git@github.com:", "").replace("https://github.com/", "")
    parts = s.split("/")
    return parts[-2], parts[-1]

def _wiki_dir(origin):
    _, repo = _owner_repo(origin)
    return Path.home() / ".lab" / (repo + ".wiki")

def _ensure_wiki(origin):
    wdir = _wiki_dir(origin)
    wurl = (origin[:-4] + ".wiki.git") if origin.endswith(".git") else origin + ".wiki.git"
    if (wdir / ".git").exists():
        run(["git", "pull", "--quiet", "--no-rebase"], cwd=str(wdir))
        return wdir
    wdir.parent.mkdir(parents=True, exist_ok=True)
    code, _, _ = run(["git", "clone", wurl, str(wdir)])
    return wdir if code == 0 else None

# ----------------------------------------------------------------------- #
#  LaTeX render
# ----------------------------------------------------------------------- #

def render_pdf(texpath):
    d, name = os.path.dirname(texpath), os.path.basename(texpath)
    if shutil.which("latexmk"):
        run(["latexmk", "-pdf", "-interaction=nonstopmode", name], cwd=d)
    elif shutil.which("pdflatex"):
        run(["pdflatex", "-interaction=nonstopmode", name], cwd=d)
        run(["pdflatex", "-interaction=nonstopmode", name], cwd=d)
    elif shutil.which("tectonic"):
        run(["tectonic", name], cwd=d)
    else:
        print(f"{DIM}No LaTeX engine found. Install MiKTeX/TeX Live (latexmk/pdflatex).{RST}")
        return None
    pdf = texpath[:-4] + ".pdf"
    # tidy up LaTeX build leftovers (keep .tex and .pdf)
    base = texpath[:-4]
    for ext in (".aux", ".log", ".out", ".fls", ".fdb_latexmk",
                ".synctex.gz", ".toc", ".bbl", ".blg"):
        try:
            os.remove(base + ext)
        except OSError:
            pass
    return pdf if os.path.exists(pdf) else None

# ----------------------------------------------------------------------- #
#  Action: LaTeX insight -> render -> wiki
# ----------------------------------------------------------------------- #

def insight(domain=None):
    root = repo_root()
    if not root:
        print(f"{DIM}Run inside the lab repo (cd lab).{RST}"); return
    dom = domain or TODAY or pick_domain()
    if not dom:
        print(f"{DIM}Pick a domain to file the insight under.{RST}"); return
    label, folder, page = dom

    title = ask("Insight title")
    if not title:
        print(f"{DIM}No title, cancelled.{RST}"); return
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    tdir = os.path.join(root, "insights", folder)
    os.makedirs(tdir, exist_ok=True)
    texpath = os.path.join(tdir, f"{date}-{slug}.tex")

    # build the .tex from the template
    tpl = os.path.join(root, "templates", "insight.tex")
    base = open(tpl, encoding="utf-8").read() if os.path.exists(tpl) else _FALLBACK_TEX
    base = (base.replace("@TITLE@", title)
                .replace("@AUTHOR@", f"Aaron Cuevas ({USER})")
                .replace("@DATE@", date)
                .replace("@DOMAIN@", label))
    with open(texpath, "w", encoding="utf-8") as f:
        f.write(base)

    print(f"\n{DIM}Opening the editor — write your insight (with equations), save and close.{RST}")
    open_editor(texpath)

    print(f"{DIM}Rendering...{RST}")
    pdf = render_pdf(texpath)
    if not pdf:
        print(f"{DIM}Could not produce a PDF. Saving the .tex source anyway.{RST}")
        git_publish(root, [texpath], f"insight ({folder}): {title}")
        return

    if ask("Open the PDF to preview? (y/N)", "n").lower().startswith("y"):
        open_file(pdf)

    # 1) source goes to the lab repo
    git_publish(root, [texpath], f"insight ({folder}): {title}")

    # 2) PDF goes to the wiki
    if not ask("Push the PDF to the wiki? (Y/n)", "y").lower().startswith("n"):
        origin = _origin()
        wdir = _ensure_wiki(origin) if origin else None
        if not wdir:
            print(f"{DIM}Wiki not ready. Open {origin and origin.replace('.git','')}/wiki once "
                  f"('Create the first page', save) and retry.{RST}")
            return
        owner, repo = _owner_repo(origin)
        dest_dir = wdir / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        fname = f"{date}-{slug}.pdf"
        shutil.copy(pdf, dest_dir / fname)
        raw = f"https://raw.githubusercontent.com/wiki/{owner}/{repo}/{folder}/{fname}"
        page_file = wdir / f"{page}.md"
        fresh = not page_file.exists()
        with open(page_file, "a", encoding="utf-8") as f:
            if fresh:
                f.write(f"# {label} — insights\n")
            f.write(f"- {date} — {title} — [PDF]({raw})\n")
        run(["git", "add", "."], cwd=str(wdir))
        run(["git", "commit", "-m", f"insight {folder} {date}: {title}"], cwd=str(wdir))
        code, o, e = run(["git", "push"], cwd=str(wdir))
        if code == 0:
            print(f"{GR}PDF on the wiki \u2713{RST}  {origin.replace('.git','')}/wiki/{page}")
        else:
            print(f"{DIM}Wiki push failed: {(e or o).strip().splitlines()[-1] if (e or o).strip() else ''}{RST}")

_FALLBACK_TEX = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb}
\title{@TITLE@}\author{@AUTHOR@}\date{@DATE@}
\begin{document}\maketitle
% Domain: @DOMAIN@
\end{document}
"""

# ----------------------------------------------------------------------- #
#  Action: field note (separate repo)
# ----------------------------------------------------------------------- #

def find_field_repo():
    # 1) env  2) sibling  3) home  4) config in lab repo
    candidates = []
    if os.environ.get("LAB_FIELD_NOTES"):
        candidates.append(os.environ["LAB_FIELD_NOTES"])
    root = repo_root()
    if root:
        candidates.append(os.path.join(os.path.dirname(root), "field-notes"))
        cfg = os.path.join(root, ".lab.cfg")
        if os.path.exists(cfg):
            for line in open(cfg, encoding="utf-8"):
                if line.startswith("FIELD_NOTES="):
                    candidates.append(line.split("=", 1)[1].strip())
    candidates.append(str(Path.home() / "field-notes"))
    for c in candidates:
        if c and os.path.isdir(os.path.join(c, ".git")):
            return c
    return None

def field_note():
    fr = find_field_repo()
    if not fr:
        print(f"\n{DIM}field-notes repo not found.{RST}")
        print(f"  Create it:  gh repo create {USER}/field-notes --public --clone")
        print(f"  Place it next to this repo (../field-notes), or set LAB_FIELD_NOTES=path,")
        print(f"  or add a line  FIELD_NOTES=/full/path  to .lab.cfg in the lab repo.")
        return
    topic = ask("Field note topic")
    if not topic:
        print(f"{DIM}No topic, cancelled.{RST}"); return
    dom = TODAY or pick_domain()
    label = dom[0] if dom else "—"
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(topic)
    ndir = os.path.join(fr, "notes")
    os.makedirs(ndir, exist_ok=True)
    path = os.path.join(ndir, f"{date}-{slug}.md")
    tpl = os.path.join(fr, "templates", "field-note.md")
    if os.path.exists(tpl):
        base = open(tpl, encoding="utf-8").read()
    else:
        base = ("# @TOPIC@\n\n*@DATE@ · relates to: @DOMAIN@*\n\n"
                "## Problem\n\n## Process (how I broke it into subsystems)\n\n"
                "## Insight / pattern\n\n## Code\n\n")
    base = base.replace("@TOPIC@", topic).replace("@DATE@", date).replace("@DOMAIN@", label)
    with open(path, "w", encoding="utf-8") as f:
        f.write(base)
    print(f"\n{DIM}Opening the editor — write freely, save and close.{RST}")
    open_editor(path)
    git_publish(fr, [path], f"field note: {topic}")

# ----------------------------------------------------------------------- #
#  Guides and resources (just print the files)
# ----------------------------------------------------------------------- #

def _print_file(rel, fallback=""):
    root = repo_root() or "."
    p = os.path.join(root, rel)
    if os.path.exists(p):
        print("\n" + open(p, encoding="utf-8").read())
    else:
        print(fallback)

def github_guide():
    _print_file("guides/github.md", "guides/github.md not found.")

def latex_guide():
    _print_file("guides/latex.md", "guides/latex.md not found.")

def resources():
    _print_file("resources.md", "resources.md not found.")

# ----------------------------------------------------------------------- #
#  menu / main
# ----------------------------------------------------------------------- #

def _header():
    here = f"  ·  today: {TODAY[0]}" if TODAY else ""
    print(f"\n{BOLD}  lab{RST}{DIM} — replicate{here}{RST}\n")
    print(f"    {CY}[1]{RST} Wiki · LaTeX insight")
    print(f"    {CY}[2]{RST} GitHub guide")
    print(f"    {CY}[3]{RST} LaTeX guide")
    print(f"    {CY}[4]{RST} Research resources")
    print(f"    {CY}[5]{RST} Field notes (separate repo)")
    print(f"    {CY}[q]{RST} Quit\n")

def menu():
    global TODAY
    intro()
    TODAY = pick_domain()
    while True:
        _header()
        try:
            op = input(f"  {CY}>{RST} ").strip().lower()
        except EOFError:
            print(); break
        if op in ("1", "i", "insight"):
            insight()
        elif op in ("2", "github", "g"):
            github_guide()
        elif op in ("3", "latex", "l"):
            latex_guide()
        elif op in ("4", "resources", "r"):
            resources()
        elif op in ("5", "field", "f"):
            field_note()
        elif op in ("q", "quit", "exit"):
            break
        else:
            print(f"  {DIM}Invalid option.{RST}")
        try:
            input(f"{DIM}  Enter to continue...{RST}")
        except EOFError:
            break

def main():
    args = sys.argv[1:]
    if not args:
        menu(); return
    kw = args[0].lower()
    if kw in ("insight", "i"):
        insight()
    elif kw in ("github", "g"):
        github_guide()
    elif kw in ("latex", "l"):
        latex_guide()
    elif kw in ("resources", "r"):
        resources()
    elif kw in ("field", "f"):
        field_note()
    elif kw in ("-h", "--help", "help"):
        print(__doc__)
    else:
        print(__doc__)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
