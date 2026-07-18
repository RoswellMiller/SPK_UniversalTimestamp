# Coding and Documenting Standards

> **Portable project standards, adopted on `SPK_UniversalTimestamp`
> 2026-07-18.**  This document was originally distilled on
> `SPK_UniversalReferenceFrame`; this project uses it as a shared
> baseline.  It is *not* re-authored per project — copy it in, add a
> project-specific overlay if needed (e.g. `docs/Project_Conventions.md`),
> and delete individual sections only if they genuinely do not apply.
> Nothing here is dogma — each rule earned its place by preventing a
> real failure or a real confusion at least once.

Last revised: 2026-07-18


## 1 — Document architecture

Every project of any size keeps **four kinds of records**, each with a
distinct job.  Confusing them is how documentation rots.

| Document | Job | Mutability |
|---|---|---|
| **Architecture** (e.g. `ProjectName_Architecture.md`) | Single source of truth for design — the rules the implemented system obeys.  Source-agnostic and tool-agnostic. | Living; rule numbers stable forever |
| **Developer Handbook** (e.g. `ProjectName_Developer_Handbook.md`) | Procedures and per-tool detail: CLI reference, rebuild recipes, inventories, audit workflows, math specs. | Living; organized by chapter |
| **Plan documents** (`docs/plans/XX-N_*.md`) | Work in flight: intent, rationale, phasing, open questions, decision log.  One plan per initiative. | Frozen once ratified or retired |
| **TODO backlog** (`docs/TODO_BACKLOG.md`) | Durable open items that have no plan document yet.  Part of the printable state-of-the-project package. | Living list |

### 1.1 — Project structure

1. Standard GitHub project layout (`src/`, `tests/`, `pyproject.toml`,
   `LICENSE`, `README.md`).
2. Folder additions:
   * `deprecated/` — documents and code retired as files (kept
     locally for reference; **not committed** — see § 8).
   * `docs/` — all generated .md documents except plans.
   * `docs/plans/` — all `XX-N …` plan documents.
   * `tools/` — durable command-line utilities (see § 6).
   * `tools/work_product/` — converter outputs (regenerable; not
     committed except small review artifacts — see § 8).
   * `build_logs/` — scratch diagnostics and one-off scripts (never
     committed).
   * `data/` — seeds (committed) and built databases (not committed).
   * `user-data/` — per-user work library (never committed).

### 1.2 — Governance loop

1. New work starts as a **backlog item** (B-N).
2. When activated, it graduates to a **plan document** with a prefix
   that names its domain (examples from the source project: `PL-N`
   pipeline/loader, `IN-N` infrastructure, `TR-N` triangulation,
   `T-N` tests).  The backlog entry is marked with the plan number.
3. On completion of a plan element, **the Architecture doc absorbs the
   new invariant and the Handbook absorbs the new procedure** — the
   knowledge moves to the steady-state records, it does not stay
   trapped in the plan.
4. The plan document then either **ratifies** (a change-log entry
   notes it) or is **retired** to `deprecated/docs/plans/`.  Plan
   status sections must be updated when work lands — a plan that
   reads "not started" for shipped code is worse than no plan.
5. Ephemeral session checklists live in the editor/agent todo tracker
   only.  They never clutter the durable documents.

### 1.3 — Rules within the Architecture doc

* **Rule numbers are stable.**  Never renumber.  Superseded rules stay
  in place marked **[obsolete]** with a pointer to the replacement.
* Every rule states an invariant, not a hope: "X *is* Y", with the
  enforcing code or check named.
* A rule that cannot name its enforcement is a proposal, not a rule —
  it belongs in a plan document.

### 1.4 — Change logs

* Architecture doc, Handbook, and any long-lived spec end with a
  **change-log table**: date, sections touched, one-paragraph summary
  in **bold lead-in** style.  The change log is what makes a living
  document auditable.
* Write change-log entries as post-mortems when the change fixed a
  defect: symptom → root cause → fix.  Future readers search for
  symptoms.

### 1.5 — Status preambles

Every living document opens with a short blockquote answering:

* What is this document's job, in one sentence?
* What is its companion document, and what does the split mean?
* Where do things that don't belong here go?


## 2 — Document style

* **American spelling** throughout (`color`, `behavior`, `center`).
  Legacy files keep their spelling until otherwise refactored.
* Headings numbered `## N — Title` so sections can be cited as "§ N".
* Tables for anything with more than two parallel facts; prose for
  rationale.  A table row that needs a paragraph gets a footnote or a
  subsection instead.
* Cross-reference by relative markdown link, never by bare filename.
* File, function, and constant names in backticks; the first mention
  of a companion doc gets a link.
* Prefer worked examples with real values over abstract description
  (the "canonical reproducer" pattern: name the exact polygon /
  record / input that exposed the issue).

### 2.1 — Printable output pipeline

Hard-won print rules (Chromium-based markdown→PDF exporters):

* Keep a **source-of-truth CSS file** in the user profile and a sync
  script that splices it into the exporter — extension updates wipe
  both the exporter's stylesheet *and* its embedded browser, so the
  sync script must be re-run after updates and the exporter pinned to
  an installed browser (`executablePath`).
* Page setup for 3-hole punch: Letter, left margin 1.25 in (binding),
  right 0.6 in, top/bottom 0.75 in.
* Approved type scale: body 11 pt / line-height 1.4; h1 16 pt,
  h2 14 pt, h3 12 pt, h4–h6 11 pt; code and tables 10 pt.
* **Defeat print shrink-to-fit**: one over-wide table or unwrappable
  code line silently scales the WHOLE document down (observed: ⅔
  size).  CSS: `table { width:100%; table-layout:fixed }`,
  `td,th,code { overflow-wrap:anywhere }`, `img { max-width:100% }`,
  `pre { white-space:pre-wrap }`.
* Never compare PDFs of different ages — re-export both before
  judging a formatting change.


## 3 — Coding style

### 3.1 — Type hints on every function

* Every `def` carries type hints — arguments and return type.  Public
  APIs are non-negotiable; internal helpers follow the same rule so
  the type checker sees the whole call graph.
* Prefer precise types (`tuple[float, float]`, `dict[str, Any]`,
  `str | None`) over bare containers; use `Any` only where the value
  is genuinely dynamic and say why in the docstring.

### 3.2 — Comments explain WHY, at the site of the decision

* Every non-obvious constant carries a comment with **units, the
  chosen value's rationale, and what breaks if it changes**.
* Functions which are non-obvious all have descriptive headers after the def statement
* When code deviates from the obvious approach, the comment says what
  the obvious approach was and why it lost.
* Comments are maintained like code: a landed fix updates the nearby
  comment that described the old behavior.

### 3.3 — Docstrings state contracts

* Public functions/methods: one-line summary, then the contract —
  argument semantics, return value, error behavior, side effects.
* Document *invariants and guarantees* ("returns pieces that pass the
  gate"; "never mutates the input ring"), not implementation prose.
* Known limitations are part of the contract ("produces T-junctions;
  not watertight — do not use for 3-D").

### 3.4 — Diagnostics and observability

* Diagnostic prints carry a **bracketed tag** naming the subsystem
  (`[3D-lut-push]`, `[polygon-split]`, `[perf 2D _redraw]`) so logs
  can be grepped by feature.
* Perf-sensitive paths print wall-clock traces gated by thresholds
  (only report when > N ms) so the console stays quiet in the normal
  case.
* Long-running tools print progress with running counters and rates;
  final summaries are aligned key–value blocks suitable for pasting
  into a report.
* Diagnostics write to stderr with `flush=True` so they interleave
  correctly with other output.

### 3.5 — Defensive boundaries, not defensive everywhere

* Validate at system boundaries (file loads, DB rows, user input,
  cross-process payloads).  Interior code trusts its callers.
* Guard clauses with named failure counters
  (`counter("repair_polygon_ring", tag="degenerate-skip")`) beat
  silent `except: pass`.
* When a guard drops data, it says so once, loudly, with the count.

### 3.6 — Feature gates and environment switches

* Risky or expensive alternates hide behind environment variables
  with a `SPK_`-style project prefix (`SPK_2D_GL_VIEWPORT=1`,
  `SPK_ENABLE_3D_PAINT_SETS=1`).  The default is the safe path; the
  comment at the gate explains both.

### 3.7 — Language and platform conventions

* American spelling in all identifiers, comments, and docs.
* PowerShell for automation on Windows.  Hard-won rules:
  * Save `.ps1` as ASCII (or UTF-8 **with** BOM) — PS 5.1 misparses
    no-BOM UTF-8 punctuation into baffling syntax errors.
  * Under `$ErrorActionPreference = "Stop"`, native-command stderr
    becomes a terminating error; run external tools via
    `Start-Process -Wait -PassThru` with output redirection and check
    `.ExitCode`.
  * `-replace` is case-insensitive; use `-creplace` or
    `[string].Replace()` for literal renames.
* Python: type hints on public signatures; lazy imports inside
  functions when the import is heavy or circular; f-strings for
  formatting.


## 4 — Testing conventions

* **Never touch real user data.**  Tests that exercise a persistence
  path get a temp store via fixture + monkeypatch of the store
  factory.  (Earned: a signals test silently wrote fixture styles
  into the developer's production user library.)
* **Version-relative assertions.**  Tests about "current version vs
  stale version" derive both from the live constant
  (`v0 = MODULE.VERSION; bump = v0 + 1`) — never hard-code versions.
* **Test the colliding pair.**  When ordering or substring collisions
  matter ("Antarctic" contains "arctic"), the regression test
  includes the colliding case by name.
* **Cross-check through the real artifacts.**  Prefer tests that pull
  real rows (real triangulations, real LUT blobs) and verify the
  production math end-to-end over synthetic-only fixtures; skip
  cleanly when the artifact (master DB) is absent.
* Regression tests carry the defect's story in the module docstring:
  symptom, root cause, what the test pins down.


## 5 — Data and database conventions

* **Explicit transactions.**  Writes require a named
  `BEGIN_transaction("purpose")` / `COMMIT_transaction()`; work
  outside a transaction rolls back on close *silently* — treat any
  "my insert vanished" symptom as a missing transaction first.
* **Schema versions with forward migrations.**  A single
  `SCHEMA_VERSION` int; `_create_schema` builds fresh, `_migrate`
  handles `if from_version < N:` steps.  Both paths produce identical
  schemas.
* **Data classes** (adapt names per project): class 1 = source
  geometry/science data; class 2 = derived scientific data; class 3 =
  display/graphics pre-computation (triangulation tiers, rasterized
  LUTs).  Class-3 rows carry a **generator version column** and
  readers pin their query to the current version so stale rows are
  invisible rather than wrong.
* Master (shipped/rebuilt) data vs user (work library) data live in
  separate database files; rebuilds may wipe the master, never the
  user library.
* Every destructive pipeline ends with an **automated verifier** — a
  script of named PASS/FAIL checks with thresholds, run as the final
  step, exiting nonzero on any failure.


## 6 — Tools and scripts

* One-off diagnostics live in a scratch folder (`build_logs/_*.py`),
  never in `src/`.  Durable utilities live in `tools/` with argparse
  CLIs and `--verbose` flags.
* Unattended pipelines: timestamped log file per run; per-step
  echo of the exact command; abort on first nonzero exit; final
  "finished OK" line.  A lock/busy check up front refuses to start
  against a resource in use.
* Before running a long destructive pipeline, run a **smoke variant**
  into a temp directory (minimal flags) to prove the plumbing.


## 7 — Workflow habits

* **Fix at the source, not the consumer.**  When bad geometry/data is
  detected at render/read time, the fix belongs in the
  loader/converter with a gate that rejects it thereafter.
* **Make accidents explicit.**  When behavior silently depended on a
  failure ("these shapes never filled because triangulation always
  failed"), landing the fix requires encoding the old accident as an
  explicit contract (`spherical_reference` = stroke-only).
* **Structural over timing fixes.**  If a race can be eliminated by
  construction (separate the resources) rather than by delay tuning,
  eliminate it; timing band-aids just move the race.
* Commits are checkpoints chosen by the project owner; assistants and
  scripts never commit or push on their own.
* After a defect is fixed, its diagnosis (symptom → root cause → fix)
  goes into the change log or the plan document — searchable by
  symptom.


## 8 — Repository, storage, and GitHub rules

### 8.1 — What is committed vs what is not

The test for every file: **is it source, or is it reproducible?**
Source (code, seeds, hand-curated reference data, documents) is
committed.  Anything a script can regenerate is not.

| Committed | Never committed |
|---|---|
| Source code, tests, tools | Built databases (`*.db`, `*.sqlite*`) |
| Hand-curated seeds (`.jsonc` reference data) | DB snapshots/backups (`*.db.*`, `*.bak`) |
| Documents (`docs/**`), plan docs | Derived sidecars (`*_ext.jsonc`, `*_sql.log`) |
| Small human-readable review artifacts (e.g. `entity_review.md`) | Converter outputs (`tools/work_product/**`) |
| `.gitkeep` placeholders for required-but-ignored dirs | Per-user work libraries (`user-data/*`) |
| Shared editor config (`.vscode/settings.json`, `extensions.json` — allowlisted) | Scratch/diagnostics (`build_logs/`, root `_*.py` / `_*.txt` / `_*.log`) |
| | `deprecated/` archives |

* Machine-readable manifests that churn on every regeneration (fresh
  timestamps, hundreds of MB) are NOT committed even when small
  — their human-readable review summaries are.
* Root-level scratch follows the **underscore prefix** convention
  (`_probe.py`, `_inv.py`) so one ignore pattern (`/_*.py`) covers
  all of it.

### 8.2 — Large files

* **GitHub's 100 MB hard limit is a wall**, and the practical limit
  is far lower — anything over a few MB that is reproducible should
  not be in history at all (history is forever; a deleted 600 MB
  blob still bloats every clone).
* Databases, DEM tiles, parquet mirrors, and converter payloads
  routinely exceed the limit — they live outside the repo (§ 8.3)
  or in ignored folders, never in git.  No Git LFS unless a shipped
  binary genuinely must version with the code.
* Named DB snapshots (`<stem>.db.<tag>`) need their own ignore
  pattern — `*.db` alone misses them.

### 8.3 — Downloads live outside the project tree

* Raw upstream downloads (publisher shapefiles, DEM tiles, parquet
  mirrors, API pulls) live in a dedicated **DATA-SOURCES folder
  outside the project**, one subfolder per publisher
  (`DATA-SOURCES\CopernicusDEM\`, `…\OvertureMaps\`, `…\GebCo\`,
  `…\JPL_Horizons\<run-stamp>\`).
* **A separate physical drive is preferred but not mandatory**
  (e.g. project on `C:\`, `D:\DATA-SOURCES\` for bulk data) — it
  keeps hundred-GB source sets off the system drive and survives
  project checkouts/deletes.
* The flow is one-way: converters in `tools/<source>/` READ from
  DATA-SOURCES and WRITE work products into `tools/work_product/`;
  nothing in the project ever writes back into DATA-SOURCES.
* Download scripts stamp each pull (dated run folders) so a load is
  reproducible against the exact snapshot it came from.

### 8.4 — .gitignore craft

* Comment the WHY next to each non-obvious pattern, exactly like
  code ("exceeds GitHub's 100 MB limit", "rewritten on every open").
* Allowlist style for exceptional keeps: ignore the tree, then
  un-ignore specific files (`/user-data/*` + `!/user-data/.gitkeep`).
* Gotcha: `dir/**` also ignores the intermediate directories, which
  BLOCKS `!` un-ignores of their children — re-include the directory
  levels explicitly (`!/dir/`, `!/dir/*/`) before the file negations.
* `git check-ignore -v <path>` is the debugging tool — it names the
  pattern and line that matched.

### 8.5 — Commit discipline

* Commits are checkpoints chosen by the project owner; assistants
  and scripts never commit or push on their own (see § 7).
* Before a checkpoint: run the test suite, glance at `git status`
  for surprise files (a new large artifact usually means a missing
  ignore pattern — add the pattern in the same commit).
* Commit messages name the initiative (plan number when one exists)
  and summarize outcome, not mechanics.
