# Project Memory — The Price Is Right

> This file records standing rules and conventions for this project.
> It must be read and followed in every future session.

---

## Standing Rules

### Rule 1 — GitHub Upload on Every Code Change

**Every code change, fix, patch, or documentation update MUST be committed and pushed to GitHub immediately after the change is made.**

- Repository: `https://github.com/lalitnayyar/priceisright.git`
- Branch: `main`
- Commit message format: `<type>: <short description>` (e.g. `fix:`, `feat:`, `docs:`, `patch:`)
- Never leave uncommitted changes in the sandbox at the end of a task.

**Workflow to follow after every file change:**
```bash
cd /home/ubuntu/priceisright
git add -A
git commit -m "<type>: <description>"
git push origin main
```

---

## Project Info

| Item | Value |
|------|-------|
| Repo | https://github.com/lalitnayyar/priceisright.git |
| App dir | `priceisrightcapstone/` |
| Dashboard port | `7860` |
| API port | `8001` |
| ChromaDB port | `8000` |
| Manage script (Linux) | `./manage.sh` |
| Manage script (Windows) | `.\manage.ps1` |

---

## Author

Lalit Nayyar | lalitnayyar@gmail.com | +971508320336 | +919595353336
