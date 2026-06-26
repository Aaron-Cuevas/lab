
GIT / GitHub — quick guide (Aaron-Cuevas)

  EVERYDAY CYCLE
    git pull                          get the latest before you work
    git status                        what changed
    git add .                         stage everything
    git commit -m "what I did"         save a checkpoint
    git push                          upload to GitHub

  NEW REPO (from the terminal)
    gh repo create Aaron-Cuevas/NAME --public --clone
    gh repo create Aaron-Cuevas/NAME --private --clone

  CLONE / OPEN
    gh repo clone Aaron-Cuevas/NAME
    gh browse                         open this repo in the browser
    gh browse <file>                  open a specific file/folder

  THE WIKI (where lab pushes the insight PDFs)
    - Create it once on the web: <repo>/wiki -> "Create the first page" -> save
    - It is a separate git repo: <repo>.wiki.git
    git clone https://github.com/Aaron-Cuevas/NAME.wiki.git
    - Files are served at: raw.githubusercontent.com/wiki/Aaron-Cuevas/NAME/<path>

  BRANCHES (try things without breaking main)
    git switch -c idea                 create + switch to a branch
    git switch main                    back to main
    git merge idea                     bring it into main

  IF PUSH IS REJECTED (something changed upstream)
    git pull                           fetch + merge
    git add . && git commit && git push

  UNDO (safe-ish)
    git restore <file>                 discard changes in a file (not committed)
    git revert <hash>                  new commit that undoes an old one

  TAGS / RELEASES
    git tag v0.1 && git push --tags
