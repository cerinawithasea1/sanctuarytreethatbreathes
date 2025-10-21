# Keeper Persona Kit

This folder mirrors the vault structure hinted by your `seed_structure.sh`.
Place the `personas/keeper/` folder inside your Obsidian vault (e.g. `.../Bookfairys/`).

**Files:**
- `personas/keeper/seed.md` — Keeper's seed prompt (identity, procedures, values).
- `personas/keeper/profile.md` — Editable profile (voice, revisions).
- `personas/keeper/memories.md` — Append-only durable notes and summaries.

## Quick Start
1) Copy `personas/keeper/` into your vault.
2) Ensure your server loads `seed.md` on Keeper init.
3) Wire a memory store that appends to `memories.md` (or a DB) and retrieves relevant notes each turn.
4) Add a context-limit hook: summarize old turns into a dated block and persist.

## Minimal Loader Pseudocode
```python
seed = read('personas/keeper/seed.md')
profile = read('personas/keeper/profile.md')
mems = load_vector_index('personas/keeper/memories.md')
def keeper_reply(user_msg):
    recalls = mems.search(user_msg, top_k=5)
    system = seed + '\n\n' + profile
    return call_llm(system=system, messages=[user_msg], memories=recalls)
```

Adjust to your Lumi/server framework.
