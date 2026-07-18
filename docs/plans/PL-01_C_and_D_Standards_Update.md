# PL-01 — Coding & Documenting Standards Update

> **Job of this document.**  Bring `SPK_UniversalTimestamp` into
> compliance with [`Coding and Documenting Standards.md`](../Coding%20and%20Documenting%20Standards.md)
> (the project-portable standards adopted 2026-07-18).  This is a
> project-wide clean-up plan: user-facing documentation, coding style,
> tests, and repository hygiene.
>
> **What this plan explicitly does *not* do.**
> * No `_Architecture.md` and no `_Developer_Handbook.md`.  Per the
>   project owner (2026-07-18), those two documents are overkill for a
>   library of this size and are deferred indefinitely.  The R&D book
>   plays the role the Architecture doc would otherwise play (see
>   § 2.1 below).
> * No behavioural changes to calendar math, no new calendars, no
>   `UnivMoment` / `UnivDuration` API extensions.  Those belong in
>   their own plans (proposed prefixes below).
> * No investigation of the known Chinese-calendar discrepancies
>   against R&D published values — that is seeded as a backlog item
>   for a future `CM-N` plan (see § 5, S-8, and Phase 5).
>
> **The one user-facing document this plan does create.**
> `docs/USERS_MANUAL.md` (display title *User's Manual*), replacing
> the stale `Copilot/USAGE_GUIDE.md`.  Structure mirrors `README.md`;
> every code block is executable and covered by an
> exec-the-markdown test analogous to `Tests/test_999_readme_examples.py`.
> See Phase 1.

Status: **DRAFT** — awaiting review of the open questions in § 6.
Created 2026-07-18.


## 1 — Background and intent

The Standards document arrived on 2026-07-18 as a portable distillation
of conventions developed on `SPK_UniversalReferenceFrame`.  A quick
audit of this project against those standards surfaces the gaps listed
in § 3 below.  None of the gaps are urgent defects — the code works —
but leaving them un-addressed erodes the same discipline the Standards
document exists to protect.

The plan is deliberately staged so each phase can land as its own
checkpoint and is independently reviewable.  Nothing here is a
behaviour change; every task either **adds a durable record** (docs,
tests) or **relocates / renames** existing artifacts (repo hygiene).


## 2 — Plan-prefix convention adopted for this project

The Standards doc (§ 1.2) names `PL-N`, `IN-N`, `TR-N`, `T-N` as
*examples* from its source project.  Below is the naming scheme
adopted here — subject to change when the second plan is written,
before which we have no cost of renaming:

| Prefix | Domain | First candidate |
|---|---|---|
| **PL-N** | Project-wide plans | `PL-01` (this document) |
| **CM-N** | Calendar math (adding a calendar, revising R&D algorithms, investigating discrepancies from R&D published values) | Chinese-calendar discrepancy investigation (§ 5 S-8) |
| **AS-N** | Astronomy / space (Astro_Space, JPL DE422 integration) | JPL DE422 migration for Chinese-calendar v2 (already flagged in `CHANGELOG.md` [1.0.0]) |
| **API-N** | Public API surface (`UnivMoment`, `UnivDuration`, format specs) | — |
| **T-N** | Test-suite initiatives | — |

> **Open question 6.1** — is this table right, or should `PL-N` be
> reserved (as in the source project) for pipeline/loader work and a
> different prefix (e.g. `STD-N`, `GOV-N`) used for project-wide
> plans?  Renaming after the second plan lands is annoying.

### 2.1 — Foundational principle: R&D citations are sacred

This project is a Python implementation of the algorithms in
**Reingold & Dershowitz, *Calendrical Calculations: The Ultimate
Edition*** (Cambridge University Press).  Every non-trivial
function traces to a specific numbered equation on a specific page
— the `# p 60 (2.17)` style comments already sprinkled through
`CC02_Gregorian.py`, `CC03_Julian.py`, `CC08_Hebrew.py`,
`CC14_Time_and_Astronomy.py`, and `CC19_Chinese_1645.py`.

**Rule.**  These citations are load-bearing and never removed.
Any future refactor that reorganises a `CC*` module carries the
citations with the code.  When a citation is added, it names the
R&D chapter/section as well as page + equation number, and (if
applicable) any errata reconciliation.  When a citation is
corrected, the previous cite is left in place struck through so
the audit trail survives.

The R&D book PDFs currently in `docs/` (16 chapter scans) are the
proof-of-work backing every citation.  They move to DATA-SOURCES
per Phase 2 task 2.4, but the citations in code do **not** change.

> **Open question 6.6** — where does this rule live durably?
> Options: (a) short `docs/Project_Conventions.md` overlay doc
> (single page, project-specific delta on top of the portable
> Standards); (b) new section in `README.md` titled
> *Development principles*; (c) nowhere written — enforced by
> reviewer memory.  Recommendation: (a).  It sidesteps the
> "Architecture doc" objection (it's an overlay, not an
> architecture spec) while giving the rule a permanent home.


## 3 — Audit findings (Standards → current state)

Numbered by Standards section for traceability.

### 3.1 — Document architecture (§ 1) — SCOPED DOWN

* **Architecture doc — deferred.**  Standards § 1 calls for a
  numbered-rule source-of-truth doc; project owner has decided
  (2026-07-18) that the R&D book plus the citation discipline in
  § 2.1 fills that role for a library of this size.  Not created
  by this plan.
* **Developer's Handbook — deferred.**  Same reasoning.  The
  `Makefile`, `README.md`, `CHANGELOG.md`, and the new `USERS_MANUAL.md`
  collectively cover the procedures a contributor needs.
* **`docs/TODO_BACKLOG.md` — will be created.**  Even without an
  Architecture doc, the backlog is where deferred items (see § 5
  S-8, and open question 6.2) durably live.
* `docs/plans/` exists but is empty (this document is its first
  inhabitant).
* **`Copilot/USAGE_GUIDE.md` — will be renamed and rewritten as
  `docs/USERS_MANUAL.md`** (see Phase 1).  Content today is stale:
  it references a `UniversalTimestamp` class that no longer exists
  (the class is `UnivMoment`) and utility functions
  (`sort_timestamps_ascending`, `create_julian_calendar_date`, …)
  that are not in the current package.  Almost none of it is
  salvageable verbatim, but the *shape* (task-oriented recipes
  keyed off the public API) is worth preserving.
* `docs/` currently mixes the Standards doc **with 16 chapter-scan
  PDFs from *Calendrical Calculations* (Reingold & Dershowitz)** and
  two ISO-19108 PDFs.  Standards § 8.3 says raw upstream sources
  live in a **DATA-SOURCES** folder **outside the project tree**.
  See task 2.4.  Removing the PDFs from the repo does not remove
  the citations in code — those stand on their own (§ 2.1).

### 3.2 — Document style (§ 2) — MINOR

* Standards § 2 uses `## N — Title` numbered headings so sections can
  be cited as § N.  `README.md` and `CHANGELOG.md` do not follow this
  yet.  Low priority for `README.md` (public face), higher for the
  new Architecture / Handbook docs where citation matters.

### 3.3 — Coding style (§ 3) — MEDIUM

* **Type hints (§ 3.1).**  Broadly good, but a few gaps:
  * `SPK_UniversalTimestamp/CC00_Decimal_library.py::to_roman_numeral`
    has no return type; several helpers use `def sin(x: Decimal) -> Decimal`
    correctly but the coverage is not exhaustive.
  * `SPK_UniversalTimestamp/Astro_Space.py::psoEarth` — every dunder
    (`__init__`, `__str__`, `__eq__`, `__ne__`, `__hash__`) is
    unannotated.
* **Docstrings state contracts (§ 3.3).**  Most functions carry a
  terse one-liner (e.g. `CC02_Gregorian.py` — "Convert Gregorian date
  to Rata Die (rd) fixed day number") but do **not** state error
  behaviour, side effects, or invariants.  The R&D page-cite
  comments (`# p 60 (2.17)`) are good and should stay.
* **American spelling (§ 3.7).**  One holdout: `behaviour` in
  `SPK_UniversalTimestamp/Moment_bPresent_Geological.py:1053`.
* **Diagnostic tags (§ 3.4).**  The codebase has essentially no
  diagnostic-print pattern today (one fallback `print()` in
  `Moment_bPresent_Geological.py:1358`).  This is fine — the library
  is a computational core, not an interactive tool — but the Handbook
  should document the "quiet by default" stance so future maintainers
  don't sprinkle prints.

### 3.4 — Testing (§ 4) — MEDIUM

* `Tests/conftest.py` contains a **stale test-order table**:

  | conftest reference | actual filename |
  |---|---|
  | `test_002_DecimalLibrary.py` | `test_010_DecimalLibrary.py` |
  | `test_100_Geological.py` | `test_130_Moment_bGeological.py` |
  | `test_200_UnivCalendars.py` | `test_160_Moment_bCalendars.py` |
  | `test_201_Gregorian.py` | `test_200_Moment_cGregorian.py` |
  | `test_202_Julian.py` | `test_201_Moment_cJulian.py` |
  | `test_203_Hebrew.py` | `test_203_Moment_cHebrew.py` |
  | `test_500_UnivFactory.py` | (no such file exists) |
  | `test_501_Sorting.py` | `test_501_Miscellaneous.py` |
  | `test_502_readme_examples.py` | `test_999_readme_examples.py` |

  Every test currently falls through to the `999` default — the map
  is silently a no-op.  Either sync it or delete it and rely on
  alphabetical order (the file-number scheme already gives us that
  for free).
* Same file splits on `\\` only — non-portable across Linux/macOS
  runners; use `os.sep` or `pathlib`.
* No temp-store fixture pattern in play (the library holds no user
  state, so § 4's "never touch real user data" rule is not violated —
  but the Handbook should record that the rule *applies vacuously
  today* so it isn't forgotten if persistence lands later).

### 3.5 — Repository / storage / GitHub rules (§ 8) — MEDIUM

* **`.gitignore` gaps:**
  * Ignores `Deprecated/` (capital D) but the real folder is
    `deprecated/` — pattern misses on case-sensitive filesystems.
  * No `/_*.py`, `/_*.txt`, `/_*.log` pattern for root-level scratch
    (§ 8.1 underscore convention).
  * Ignores `.vscode/` wholesale.  Standards § 8.1 calls for
    **allowlisting** `settings.json` and `extensions.json`.
  * Ignores `Resources/` — but that folder contains
    `CC19_Sexagesimal_Names.json`, `CC19_Table_19_1a.json`, and
    `geological-time-scale.json`, which are hand-curated seeds that
    § 8.1 says should be committed.
  * Ignores `Copilot/` — folder should not exist under this name
    (see 3.1); if `USAGE_GUIDE.md` survives, it belongs in the
    Handbook.
* **`deprecated/` is currently committed** (contains `UnivCalendars.py`,
  seven old `UnivXxx` implementations, and six `xxtest_…` files).
  Standards § 8.1 says `deprecated/` archives are **never** committed.
  Recommend: move to a local-only archive folder outside the project,
  OR keep in the tree but rename to something explicit like
  `_legacy_reference/` and add an ignore pattern.  See open question
  6.2.
* **`spk_universal_timestamp.egg-info/` is committed** (5 files).
  This is a build artifact; `.gitignore` already lists `*.egg-info/`
  so the committed copy is stale.  `git rm --cached` on next
  checkpoint.
* **`__pycache__/` at repo root** appears in the workspace listing —
  either a stray commit or noise from the editor.  Verify with
  `git ls-files`.
* **Data-sources policy (§ 8.3).**  The R&D and ISO PDFs in `docs/`
  are exactly the kind of upstream source material § 8.3 says lives
  in a `DATA-SOURCES\` folder outside the project.  See task 4.2.4.

### 3.6 — pyproject.toml — TRIVIAL

* Three `yourusername` placeholder URLs in `[project.urls]` (lines
  55-57).


## 4 — Work phases

Each phase is a natural checkpoint.  Tasks marked **[owner]** are
mine to do; tasks marked **[RM]** need the project owner's
decision or hand.

### 4.0 — Checkpoint protocol

A “CHECKPOINT” line inside a phase is a directive to **stop and run
the full test suite** before continuing:

```powershell
pytest --tb=short --no-header 2>&1 | Tee-Object -FilePath Output/PL-01_ck_<label>.txt
```

Each checkpoint yields a report saved as `Output/PL-01_ck_<label>.txt`
(e.g. `PL-01_ck_1A.txt`), compared against the baseline captured in
Phase 0.  The pass criterion at every checkpoint is:

> **No test that was green in Phase 0 is red now.**

Known-failing tests from Phase 0 (currently the Chinese-calendar
discrepancies flagged in § 5 S-8) are **allowed to stay red** — they
are the baseline’s pre-existing state and PL-01 is not chartered to
fix them.  Any *new* red or any previously-red test that starts to
pass in an unexpected way both stop the phase until diagnosed.

If a checkpoint fails:

1. Do not proceed to the next task.
2. Diff the checkpoint report against the immediately-prior report
   (`PL-01_baseline.txt` for the first checkpoint of a phase,
   otherwise the previous checkpoint).
3. The cause is the last edit — revert or fix in place.
4. Re-run the same checkpoint; only advance when green.

Checkpoint labels are `<phase><letter>` (e.g. `1A`, `2B`); the
“letter” resets per phase.

### Phase 0 — Baseline capture (do this first)

1. Run the full test suite exactly as it stands today:

   ```powershell
   pytest --tb=short --no-header 2>&1 | Tee-Object -FilePath Output/PL-01_baseline.txt
   ```

2. Record in this plan (in § 7 decision log or a new § 9 baseline
   snapshot) the summary line — total tests / passed / failed /
   skipped — and the **exact list of failing test IDs** (module
   `::` class `::` method).  This list is the “allowed red” set for
   every downstream checkpoint.
3. Also run `mypy SPK_UniversalTimestamp` and capture its output to
   `Output/PL-01_baseline_mypy.txt`.  Same rule: pre-existing mypy
   noise is the baseline; Phase 4 checkpoints must not add to it.
4. **No source edits happen in Phase 0.**  If baseline capture is
   dirty (uncommitted changes present in `git status`), stash first
   so the recorded results reflect the tip of `main`.

> **CHECKPOINT 0** — Baseline files exist in `Output/`, the failing
> test list is transcribed into this plan, and `git status` is
> clean.  Only then does Phase 1 start.

### Phase 1 — User's Manual, backlog, and preamble hygiene

Deliverables:

1. **`docs/USERS_MANUAL.md`** (display title *User's Manual*).
   Filename uses underscore (no apostrophe) to stay portable across
   filesystems and safe in URLs.  Structure mirrors `README.md` so
   the two can be maintained together and share the same testing
   pattern.  Proposed table of contents:

   * § 1 — What SPK_UniversalTimestamp is (paragraph pulled from
     `README.md`).
   * § 2 — Installation and imports.
   * § 3 — Core concepts.  One subsection each:
     * § 3.1 `UnivMoment` — Rata Die, precision levels, immutability.
     * § 3.2 `UnivDuration` — level quantum table, arithmetic rules,
       serialization.
     * § 3.3 `Calendar` — supported calendars and their status
       (mirror the `Calendar` enum in `Constants_aCommon.py`, with
       R&D chapter reference for each — see § 2.1).
     * § 3.4 Precision — how `UnivMomPrecision` and
       `UnivDuration.precision` interlock.
     * § 3.5 Formatting — the `ucal:` / `udur:` / `ugeo:` f-string
       prefix protocol.
   * § 4 — Task-oriented recipes.  One worked example per user
     scenario:
     * *Convert Gregorian ↔ Julian for a historical date*
       (Julian-to-Gregorian transition, 1582).
     * *Represent a Hebrew calendar holiday*
       (e.g. Pesach for a specified Gregorian year).
     * *Represent a Chinese calendar date* (with the note that
       precision is limited by known discrepancies — link to
       backlog item B-01, § 5 S-8).
     * *Express a geological interval* (e.g. Cretaceous-Paleogene
       boundary at 66 Ma).
     * *Compute the span between two moments* (`UnivMoment - UnivMoment
       → UnivDuration`).
     * *Sort a heterogeneous list of moments* across calendars and
       precisions.
     * *Round-trip through JSON* (`to_dict` / `from_dict`).
     * *Round-trip through a sortable key*
       (`to_StdLexicalKey` / `from_StdLexicalKey`).
   * § 5 — Reference tables.  `LEVEL_QUANTUM`, `LEVEL_ABBREV`,
     `PREC_LEVEL`, `Calendar` enum members, format-prefix table.
     These are extracted from source, not re-typed.
   * § 6 — Known limitations.  Explicit list including Chinese-
     calendar discrepancy, geological-scale precision floor, month
     precision not supported for `UnivMoment`, `float` used only at
     I/O boundaries.
   * § 7 — Where to look next.  `CHANGELOG.md`, `docs/plans/`,
     backlog, R&D book chapter map.
   * § 8 — Change log.

   **Rule for every code block in every section:** it is a
   self-contained runnable snippet with expected output shown as a
   `# →` comment on the print line, exactly like `README.md`
   already does.  Non-executable snippets (shell commands, PowerShell
   invocations) go in ` ```bash ` / ` ```powershell ` fences and are
   excluded from the test hook by language selector.

2. **`Tests/test_998_users_manual_examples.py`** — a near-clone of
   `Tests/test_999_readme_examples.py`:
   * Reads `docs/USERS_MANUAL.md`.
   * Regex-extracts every ` ```python ` block.
   * `exec`s each in a clean namespace under `redirect_stdout`.
   * Fails loudly with the block index and content on any exception.

   Numbering choice: `998` runs just before the README examples
   (`999`) so both markdown suites sit at the tail of the run.
   Both tests share zero fixtures; keeping them parallel makes it
   easy to lift shared machinery into `conftest.py` later if the
   pattern repeats a third time (e.g. a future R&D-worked-examples
   suite).

> **CHECKPOINT 1A** — After tasks 1 and 2 land.  Full suite must
> show *exactly one* new passing test file (`test_998_...`) and
> zero new failures.  If any ` ```python ` block in the manual
> fails, that’s a manual-content bug and blocks the phase.

3. **`docs/TODO_BACKLOG.md`** — seeded with the status preamble
   from Standards § 1.5, plus **B-01: Chinese-calendar discrepancy
   investigation** (see § 5 S-8) and any other deferred items that
   surface as the phases land.

4. **Retire `Copilot/USAGE_GUIDE.md` and the `Copilot/` folder.**
   Once `USERS_MANUAL.md` and its test are green, `Copilot/` is
   removed (see Phase 2 task 3 for the git mechanics — decision
   6.3 governs whether the removal is `git rm` or
   `git mv` to `deprecated/copilot/`).

   Pre-flight grep before removal:
   `grep -R "from Copilot\|import Copilot" SPK_UniversalTimestamp Tests`
   — must return zero matches, else something in the runtime
   depends on the folder and removal blocks.

> **CHECKPOINT 1B** — After task 4.  Full suite; delta from CK-1A
> is *nothing* (the retirement removes only a folder that nothing
> imports).  Any new failure means the pre-flight grep missed a
> dependency — revert.

5. **Reword the status preamble** at the top of
   `docs/Coding and Documenting Standards.md` to identify it as
   *portable / adopted 2026-07-18*, not *authored here*.  Trivial.
   No checkpoint (pure markdown edit outside the test path).

### Phase 2 — Repository hygiene

All tasks here are configuration or file-location changes.  Two
carry real risk of test breakage — un-ignoring `Resources/` (task
1) and moving `docs/*.pdf` (task 4) — because either can shift a
path that a test loads by relative reference.  Pre-flight greps
below catch those.

1. **`.gitignore` overhaul.**  Comment every non-obvious line
   (Standards § 8.4).  Fix:
   * `Deprecated/` → `deprecated/` (case).
   * Add `/_*.py`, `/_*.txt`, `/_*.log`.
   * Remove `Resources/` from the ignore list (seeds are committed
     per § 8.1).
   * Replace the wholesale `.vscode/` ignore with an allowlist:
     ```
     .vscode/*
     !.vscode/settings.json
     !.vscode/extensions.json
     ```
   * Add `spk_universal_timestamp.egg-info/` explicit line and
     `git rm --cached` the tracked copy.

   Pre-flight grep before un-ignoring `Resources/`:
   `grep -R "Resources/" SPK_UniversalTimestamp Tests` — note
   every relative reference; those become **committed** paths and
   must not change meaning.

> **CHECKPOINT 2A** — After task 1.  Full suite; delta from
> Phase 1 finish is zero.  `git status` must show only the intended
> ignore/untracked changes and the un-cached `egg-info/`.

2. **Deprecated/ decision.**  See open question 6.2.  When answered,
   either move the folder outside the repo, or rename + ignore it,
   in a single commit.

   Pre-flight grep:
   `grep -R "from deprecated\|import deprecated\|deprecated\.Univ" SPK_UniversalTimestamp Tests`
   — must return zero matches (the runtime already imports
   exclusively from `SPK_UniversalTimestamp.*`, so this should
   pass, but confirm).

> **CHECKPOINT 2B** — After task 2.  Full suite; zero new failures.

3. **`Copilot/` decision.**  See open question 6.3.  Content moves
   to `deprecated/copilot/` or is deleted; the folder is gone from
   the tree.  (Executed in Phase 1 task 4; task listed here so the
   ignore rule and the physical move stay grouped.)

4. **DATA-SOURCES relocation.**  Move `docs/*.pdf` (R&D chapters +
   ISO 19108) to a folder outside the project tree
   (e.g. `D:\DATA-SOURCES\Reingold_Dershowitz\` and
   `D:\DATA-SOURCES\ISO_19108\`).  Because there is no Handbook,
   the outside-project path is recorded in **§ 3.3 of the User's
   Manual** (the R&D chapter map under *Calendar*) so the citation
   trail from code → chapter → PDF survives the move.  Citations
   inside code (§ 2.1) are unaffected.

   Pre-flight grep:
   `grep -R "\.pdf" SPK_UniversalTimestamp Tests` — no test may
   load a PDF by relative path.  If any match surfaces, the move
   is blocked until the reference is updated.

> **CHECKPOINT 2C** — After task 4.  Full suite; zero new failures.

5. **`pyproject.toml` URLs.**  Replace `yourusername` with
   `RoswellMiller` in three `[project.urls]` entries.  No
   checkpoint (metadata only, not read by the test runtime).
6. Verify `__pycache__/` at repo root is not tracked
   (`git ls-files __pycache__` should be empty); if it is, remove.
   No checkpoint.
7. Add a `.gitkeep` to `Output/` and `Output/plots/` if downstream
   scripts expect the folders to exist.  No checkpoint.

> **CHECKPOINT 2D** — Final Phase 2 gate.  After tasks 5–7.  Full
> suite; zero delta from CK-2C.  This is the phase’s go/no-go for
> handing off to Phase 3.

### Phase 3 — Test-suite alignment

Higher-risk phase: every task edits `Tests/conftest.py` or test
docstrings, so a mistake shows up as either collection changes or
ordering changes.  Two checkpoints, one per code-touching task.

1. **`Tests/conftest.py` `pytest_collection_modifyitems`** — either
   delete the stale `file_order` map (recommended; the file-number
   scheme sorts alphabetically anyway) or update it to match today's
   filenames.

> **CHECKPOINT 3A** — After task 1.  Full suite; **same pass/fail
> set as Phase 0 baseline** and no test collection warnings.  If
> anything changed, an ordering assumption we didn’t know about
> was in play — investigate before proceeding.

2. Replace the `split('\\')` with `Path(...).name` so the collection
   hook works on non-Windows CI.

> **CHECKPOINT 3B** — After task 2.  Full suite; zero delta from
> CK-3A on Windows.  (Non-Windows verification is a future CI
> concern, not gate-blocking here.)

3. Add a **regression-story docstring** (§ 4 last bullet) to any
   test that pins down a specific defect.  Non-defect tests keep
   their current descriptive docstring.  No checkpoint (docstring
   edits do not change behaviour).

> **CHECKPOINT 3C** — Final Phase 3 gate.  After task 3.  Full
> suite; zero delta from CK-3B.

### Phase 4 — Coding-style pass

**Non-behavioural.**  No calendar math is touched.  Every task in
this phase respects § 2.1: R&D citations are never removed,
reordered, or paraphrased.  If a docstring rewrite touches a line
near a `# p N (X.Y)` comment, the citation stays exactly where it
is, adjacent to the equation it labels.

This is the phase where a slip most likely breaks something:
docstring rewrites, type-hint additions, and header blocks all
touch source files that participate in imports.  Checkpoint
aggressively — **one pytest run per module batch**.

1. **Type-hint fill-ins.**  Add missing type hints on
   `Astro_Space.py::psoEarth` dunders and
   `CC00_Decimal_library.py::to_roman_numeral`.  Run `mypy` to
   surface any others (`Makefile` target `type-check` already exists).

> **CHECKPOINT 4A** — After task 1.  Full suite + `mypy
> SPK_UniversalTimestamp`.  Test suite delta = zero from Phase 3
> finish.  mypy delta from `PL-01_baseline_mypy.txt` must not grow.

2. **Docstring contracts, batched by module** (§ 3.3): argument
   semantics, return, error behaviour, invariants.  Start with the
   public surface — everything re-exported from `__init__.py` — then
   descend.  **One checkpoint after each module batch lands.**  Order:

   | Batch | Module(s) | Checkpoint |
   |---|---|---|
   | 4.2.1 | `UnivMoment.py` | **CK-4B-1** |
   | 4.2.2 | `UnivDuration.py` | **CK-4B-2** |
   | 4.2.3 | `CC02_Gregorian.py` | **CK-4B-3** |
   | 4.2.4 | `CC03_Julian.py` | **CK-4B-4** |
   | 4.2.5 | `CC08_Hebrew.py` | **CK-4B-5** |
   | 4.2.6 | `CC19_Chinese_1645.py` — careful, this is the module whose tests carry known Phase-0 failures | **CK-4B-6** |
   | 4.2.7 | `CC14_Time_and_Astronomy.py` | **CK-4B-7** |
   | 4.2.8 | `CC01_Calendar_Basics.py` | **CK-4B-8** |
   | 4.2.9 | `CC00_Decimal_library.py` | **CK-4B-9** |
   | 4.2.10 | `Moment_bPresent_Calendars.py`, `Moment_bPresent_Geological.py` | **CK-4B-10** |
   | 4.2.11 | `Moment_cPresent_Gregorian.py`, `Moment_cPresent_Julian.py`, `Moment_cPresent_Hebrew.py`, `Moment_cPresent_Chinese.py` | **CK-4B-11** |
   | 4.2.12 | `Constants_aCommon.py`, `Constants_Gregorian.py`, `Constants_Julian.py`, `Constants_Hebrew.py`, `Constants_Chinese.py` | **CK-4B-12** |
   | 4.2.13 | `Astro_Space.py` | **CK-4B-13** |

   Each CK-4B-N is a full pytest run.  Pass criterion: **zero new
   failures vs Phase 0 baseline**.  Docstring-only edits should
   never break tests, so any red at CK-4B-N means an inadvertent
   code change slipped in — diff the module, revert the offending
   hunk, re-run.

3. **American-spelling sweep** — one edit: `behaviour` → `behavior`
   in `Moment_bPresent_Geological.py:1053`.

> **CHECKPOINT 4C** — After task 3.  Full suite; zero delta from
> CK-4B-13.  (Trivial change, but the discipline is cheap.)

4. **Module-header blocks.**  Add a header to every
   `SPK_UniversalTimestamp/*.py` file that lacks one, stating: what
   the module is, **which R&D chapter and page range it implements**
   (if any), and what it depends on.  Most already have this; the
   `Constants_*` files typically do not.  This header is the
   module-level anchor for the citation discipline in § 2.1.

> **CHECKPOINT 4D** — Final Phase 4 gate.  After task 4.  Full
> suite; zero delta from CK-4C.  mypy also re-run; delta from
> baseline must not grow.

### Phase 5 — Ratify and record

1. Landing sequence: because there is no Architecture doc and no
   Handbook here, the ratification loop is: each phase's outcome
   either updates `README.md`, `USERS_MANUAL.md`, `CHANGELOG.md`, or
   `docs/TODO_BACKLOG.md`.  No knowledge stays trapped in this plan.
2. When all five phases land, mark this document **RATIFIED** and
   add a `CHANGELOG.md` `[Unreleased]` entry summarising the
   initiative.
3. If any phase is deferred, it moves to `docs/TODO_BACKLOG.md`
   with a note pointing back here.
4. **Seed the backlog** with the follow-on plans surfaced during
   this audit — most notably **B-01: Chinese-calendar discrepancy
   investigation** (§ 5 S-8), which will graduate to `CM-01` when
   activated.

> **CHECKPOINT 5** — Final gate for the whole plan.  One last
> pytest run; the archived report `Output/PL-01_ck_final.txt`
> becomes evidence in the CHANGELOG entry.  Pass criterion is the
> same as every other checkpoint: no test that was green in
> Phase 0 is red now.


## 5 — Suggestions / modifications flagged for review

Where I disagreed with, or want to extend, the Standards document as
applied to this project:

* **S-1.  Adopt `PL-N` for project-wide plans** (this doc's
  numbering).  Alternative: reserve `PL-N` for pipeline/loader (as
  in the source project) and use `STD-N` here.  See open question
  6.1.
* **S-2.  R&D chapter PDFs — DATA-SOURCES rules are the right home,
  but the code cites page numbers heavily** (`# p 60 (2.17)`).  A
  Handbook table mapping each `CC*` module to its R&D chapter title
  plus its outside-project PDF path keeps the citation useful
  without pulling the PDFs back into the repo.
* **S-3.  `Copilot/USAGE_GUIDE.md` is renamed and rewritten, not
  merely deleted.**  The class name it teaches doesn't exist; the
  utility functions don't exist.  But the *shape* of the document —
  a task-oriented recipe collection keyed off the public API — is
  worth preserving.  Reincarnate it as `docs/USERS_MANUAL.md`
  (Phase 1), migrate any accurate content, delete the rest, then
  remove the `Copilot/` folder (Phase 2).
* **S-4.  `Tests/conftest.py`'s file-order table has already failed
  silently once (all entries now stale).**  This is a Standards §
  7 "make accidents explicit" case: rather than fixing the table,
  delete it and rely on alphabetical order, which is what has been
  actually running for months.  Add a comment saying so.
* **S-5.  The `.vscode/` allowlist** should include the workspace
  `tasks.json` if we want the "Run Python Script" task defined in
  this project's `.vscode/tasks.json` to be shared.  (Right now the
  workspace has that task; if we allowlist only `settings.json` and
  `extensions.json` we lose it.)  Suggest allowlisting
  `tasks.json` too.
* **S-6.  Standards § 3.4 diagnostic-tag rule** — the library core
  is quiet by design; the User's Manual § 6 *Known limitations /
  Conventions* records that the library does not emit progress
  prints so future contributors don't add bracketed-tag prints to
  hot paths.  (Originally proposed as a Handbook chapter, folded
  into the User's Manual now that the Handbook is deferred.)

* **S-7.  R&D citations are load-bearing** — promoted to a
  first-class project principle in § 2.1 above.  Every existing
  `# p N (X.Y)` and `# R&D X.Y` style comment stays in place across
  any Phase 4 docstring/hint rewrite.  Open question 6.6 asks
  where the rule itself lives durably.

* **S-8.  Chinese-calendar discrepancy investigation — future
  plan.**  The current test suite is broadly green but `CHANGELOG.md`
  ([1.0.0] entry) already documents that the Chinese calendar
  implementation has known problems with some astronomical
  calculations — its outputs diverge from values published in
  R&D's book.  A version 2 pinned to the JPL DE422 standard is
  anticipated.  This deserves its own plan (`CM-01`) but is **out
  of scope for PL-01**; it enters `docs/TODO_BACKLOG.md` as B-01
  in Phase 1.  The User's Manual § 3.3 and § 6 both flag the
  limitation so users are not surprised.


## 6 — Open questions

**6.1** — Plan-prefix scheme (§ 2 above).  `PL-N` for project-wide,
or a new prefix (`STD-N` / `GOV-N`), keeping `PL-N` reserved for
pipeline/loader when/if such work ever exists here?

**6.2** — `deprecated/` folder — three options:

* (a) **Delete + local archive.**  Move the folder to
  `%USERPROFILE%\PythonArchive\SPK_UniversalTimestamp\`.  Cleanest
  per Standards; loses git history for those files (but they are
  already superseded).
* (b) **Rename to `_legacy_reference/` + gitignore.**  Keeps the
  files locally, drops them from future commits, retains prior
  history.
* (c) **Do nothing.**  Explicit deviation from Standards § 8.1 —
  requires an entry in the Architecture change log naming the
  reason.

Recommendation: **(a)** unless the old code is being actively
compared against the new (in which case (b) for a few weeks, then
(a)).

**6.3** — `Copilot/` folder — delete after Handbook migration
(see S-3), or preserve as `deprecated/copilot/` per option 6.2(b)?

**6.4** — R&D PDFs — is `D:\DATA-SOURCES\Reingold_Dershowitz\` an
acceptable location, or is there an existing bibliography folder
elsewhere on your machine that these should join?

**6.5** — Ratification cadence — land each phase as its own commit
and mark this plan as `IN-PROGRESS` between phases, or hold a
single mega-commit at the end?  Standards § 1.2 step 4 favours
per-phase ratification.

**6.6** — Where does the R&D-citation-preservation rule (§ 2.1)
live durably?  See the options list at the end of § 2.1.
Recommendation: `docs/Project_Conventions.md`, a single-page
overlay doc.  This is *not* the Architecture doc you declined —
it's a delta on top of the portable Standards, holding rules that
are specific to this project (currently just the R&D rule; more
may accumulate).

**6.7** — User's Manual scope — does the proposed table of
contents in Phase 1 task 1 fit your intent?  In particular:

* Are the eight recipe scenarios in § 4 the right ones, or do you
  want additions (e.g. multilingual formatting for French/German/
  Italian) / removals?
* Should § 3.3 name the R&D chapter for each calendar (my
  preference — reinforces § 2.1) or stay purely user-facing and
  leave chapter references to code comments?
* Should the `# →` expected-output convention in code blocks be
  **asserted** by the test hook (parse the comment, compare to
  captured stdout) or merely displayed?  README currently only
  displays; strict-assert would catch more drift but takes more
  work to author.


## 7 — Decision log

Decisions marked *(assumed by agent)* were made using the plan's own
recommended default when the owner said "go" without answering the
open question; each may be reversed by editing the plan and re-running
the affected phase.

| Date | Question | Decision | Reasoning |
|---|---|---|---|
| 2026-07-18 | 6.1 Plan-prefix scheme | Adopt `PL-N` for project-wide plans; `CM-N` / `AS-N` / `API-N` / `T-N` for domain-specific *(assumed by agent)* | Recommended default in § 2; renaming after first plan lands is cheap. |
| 2026-07-18 | 6.3 `Copilot/` disposition | **Delete** (no local archive); files remain in git history if recovery is needed | S-3 recommendation; contents were factually wrong (`UnivTimestamp` / `Precision` names that never existed in the current API). |
| 2026-07-18 | 6.6 R&D-citation-rule home | Defer creation of `docs/Project_Conventions.md`; § 2.1 of this plan is the durable record until a second project-specific rule accumulates *(assumed by agent)* | Single rules do not warrant their own doc; \u00a7 2.1 is already citation-worthy. |
| 2026-07-18 | 6.7 User's Manual scope | Adopted the TOC and eight recipes as proposed in Phase 1 task 1; `# →` output shown but not strict-asserted (matches README pattern); § 3.3 names R&D chapters *(assumed by agent)* | Matches existing README test convention; strict-assert can be added later without breaking anything. |
| 2026-07-18 | 6.2 `deprecated/` disposition | **Keep locally, stop tracking.**  `.gitignore` now carries lowercase `deprecated/`; no rename.  Discovered during Phase 2 that the folder was never tracked (old `.gitignore` had `Deprecated/` which Windows treated as case-insensitive match) *(assumed by agent)* | Matches Standards § 1.1 wording ("kept locally for reference"); zero work needed beyond making the ignore case-safe for Linux/macOS. |
| 2026-07-18 | 6.4 DATA-SOURCES for PDFs | **Gitignore in place, physical move deferred to owner.**  `.gitignore` now excludes `Documentation/`, `docs/**/*.pdf`, `docs/**/*.PDF`.  R&D chapter files stay locally in `docs/` for reading convenience; when owner is ready to consolidate them under an out-of-tree DATA-SOURCES root, that is a filesystem move only — no code needs updating (Phase 2 grep confirmed zero code references any `.pdf` file) *(assumed by agent)* | Physical file relocation affects the owner's disk outside the repo and should be their explicit action; gitignore is the reversible half. |
| 2026-07-18 | 6.5 Ratification cadence | **Per-phase** (Standards default) *(assumed by agent)* | Matches Standards § 1.4; no reason to deviate for a first plan. |


## 8 — Baseline snapshot (Phase 0 result — 2026-07-18)

Captured at HEAD of `main` with the on-disk `Documentation/`→`docs/`
rename in progress (17 PDFs staged for delete from `Documentation/`,
`docs/` untracked).  None of those files participate in the test
runtime, so the baseline reflects the same code that any downstream
checkpoint will exercise.

### 8.1 — pytest baseline

* File: [`Output/PL-01_baseline.txt`](../../Output/PL-01_baseline.txt)
* Summary: **68 passed, 2 failed** in **52.30 s**.
* **Allowed-red set** (must stay red — not new regressions):

  | Test ID | Nature |
  |---|---|
  | `Tests/test_400_Moment_cPresent_Chinese.py::Test_Moment_Chinese::test_appendix_c_Construction` | R&D Appendix C reproduction — Chinese calendar constructor returns dates that disagree with R&D published values (month/day slip by 1–3 units; one row also disagrees on leap-month flag). |
  | `Tests/test_400_Moment_cPresent_Chinese.py::Test_Moment_Chinese::test_appendix_c_Presentation` | Same root cause, verified through the presentation path. |

  These are the exact discrepancies flagged in `CHANGELOG.md` under
  **[1.0.0]** ("known problems with some of the astronomical
  calculations… A version 2 is planned which will be consistent with
  the JPL DE422 standard") and are seeded as backlog item **B-01**
  (§ 5 S-8) for a future `CM-01` plan.  PL-01 does **not** fix them.

* Pass criterion at every downstream checkpoint: **the set of red
  tests is exactly `{test_appendix_c_Construction,
  test_appendix_c_Presentation}` — nothing more, nothing fewer**.
  (A previously-red test flipping green is also suspicious and
  requires diagnosis before proceeding.)

### 8.2 — mypy baseline

* File: [`Output/PL-01_baseline_mypy.txt`](../../Output/PL-01_baseline_mypy.txt)
* Summary: **293 errors in 17 of 22 files.**
* Per-file histogram (used to plan Phase 4 batch order — heavy files
  first buys us the most signal per checkpoint):

  | Errors | File |
  |---|---|
  | 82 | `SPK_UniversalTimestamp/UnivMoment.py` |
  | 45 | `SPK_UniversalTimestamp/CC14_Time_and_Astronomy.py` |
  | 37 | `SPK_UniversalTimestamp/CC19_Chinese_1645.py` |
  | 31 | `SPK_UniversalTimestamp/Moment_bPresent_Calendars.py` |
  | 29 | `SPK_UniversalTimestamp/Moment_bPresent_Geological.py` |
  | 18 | `SPK_UniversalTimestamp/CC00_Decimal_library.py` |
  | 17 | `SPK_UniversalTimestamp/CC08_Hebrew.py` |
  | 10 | `SPK_UniversalTimestamp/Astro_Space.py` |
  | 10 | `SPK_UniversalTimestamp/CC02_Gregorian.py` |
  | 7 | `SPK_UniversalTimestamp/UnivDuration.py` |
  | 7 | `SPK_UniversalTimestamp/Moment_cPresent_Chinese.py` |
  | 4 | `SPK_UniversalTimestamp/CC01_Calendar_Basics.py` |
  | 4 | `SPK_UniversalTimestamp/Moment_cPresent_Gregorian.py` |
  | 4 | `SPK_UniversalTimestamp/Constants_Chinese.py` |
  | 3 | `SPK_UniversalTimestamp/Moment_cPresent_Hebrew.py` |
  | 3 | `SPK_UniversalTimestamp/CC03_Julian.py` |
  | 2 | `SPK_UniversalTimestamp/Moment_cPresent_Julian.py` |

  Files with **zero** baseline errors (must stay clean through
  Phase 4): `__init__.py`, `Constants_aCommon.py`,
  `Constants_Gregorian.py`, `Constants_Julian.py`,
  `Constants_Hebrew.py`.

* Pass criterion at CK-4A and CK-4D: **total error count does not
  grow above 293**, and no file with a zero baseline gains any error.

### 8.3 — Incidentals surfaced during Phase 0

Three small findings worth folding into later phases without their
own open questions:

1. **`pyproject.toml` mypy overrides table targets `tests.*`** but
   this project's test folder is `Tests/`.  mypy reports the section
   as unused.  Fix during Phase 4 task 4 (module-header pass touches
   config-adjacent conventions) — change to `Tests.*`.
2. **`Tests/conftest.py` prints "Collected: <file> :: <test>" for
   every test** during collection (roughly 70 lines of noise before
   the run starts).  Not a failure; already flagged in § 3.4 as part
   of the stale `file_order` map.  Phase 3 task 1 removes it.
3. **`Tests/PlotManager.py:15` uses lowercase `output/plots`** while
   `.gitignore` (post-Phase-2) and docs use `Output/`.  Windows
   case-insensitive FS folds them; Linux/macOS would create two
   distinct folders.  Surfaced during Phase 2's `.gitignore`
   overhaul; fix during Phase 3 alongside the `conftest.py`
   platform-path cleanup.

### 8.4 — Git state at capture

`git status --short` at capture time showed:

* 17 files in `Documentation/*.pdf` staged for delete.
* `docs/` untracked (contains the same PDFs, the Standards doc, and
  `docs/plans/PL-01_...md`).

This is an on-disk folder rename (`Documentation` → `docs`) that
predates PL-01.  It does not affect any pytest or mypy result.  It
does, however, mean Phase 2 task 4 (DATA-SOURCES relocation) should
either fold in the git-side rename or explicitly leave the deletion
staged for the same commit.


## 9 — Change log

**2026-07-18 (rev 7)** — Phase 3 landed.  (a) `Tests/conftest.py`
`pytest_collection_modifyitems` deleted — the stale `file_order` map
referenced retired filenames and had been a silent no-op for months;
the numeric-prefix naming already sorts alphabetically in the intended
order.  Removal also eliminates ~70 lines of "Collected:" noise per
test run.  The `plot_manager` session fixture is preserved.  Deletion
subsumes the original task 2 (Windows-only `split('\\')`) — no code
remains that references a path separator.  (b) `Tests/PlotManager.py:15`
lowercase `output/plots` → `Output/plots` for case-sensitive-FS
consistency (fixes § 8.3 incidental #3).  (c) `Tests/test_400_Moment_cPresent_Chinese.py`
module docstring rewritten as a regression story per Standards § 4
last bullet: symptom, root cause, backlog pointer, allowed-red status.

Gates: **CK-3A** (69 passed, 2 failed in 19.15 s — allowed-red set
unchanged; runtime back to normal after collection-print removal),
**CK-3B** (69/2 in 18.31 s — zero delta), **CK-3C** (69/2 in 17.89 s
— final Phase 3 gate).

**2026-07-18 (rev 6)** — Phase 2 landed.  (a) `.gitignore` overhauled
per Standards § 8.4: every rule commented for intent, `Resources/`
un-ignored (hand-curated seeds per § 8.1), `Copilot/` line dropped
(folder removed in Phase 1), case-safe `deprecated/`, `.vscode/`
allowlist for `settings.json`/`extensions.json`/`tasks.json`, new
`/_*.py`/`/_*.txt`/`/_*.log` scratch pattern (§ 8.1), explicit
`spk_universal_timestamp.egg-info/` line, and DATA-SOURCES coverage
via `Documentation/` + `docs/**/*.pdf`.  (b) `deprecated/` git-untrack
turned out to be a no-op — the old `Deprecated/` line already covered
it on Windows case-insensitive FS.  (c) `pyproject.toml` — `yourusername`
replaced with `RoswellMiller` in three `[project.urls]` entries.
(d) `spk_universal_timestamp.egg-info/` and `__pycache__/` verified
not tracked (`git ls-files` returned empty).  (e) `Output/.gitkeep`
unnecessary — `Tests/PlotManager.py` creates its output dir on demand.
§ 7 decision log filled for open questions 6.2, 6.4, 6.5.

Gates: **CK-2A** (69 passed, 2 failed — same allowed-red set),
**CK-2B**/**CK-2C** collapsed into CK-2A (no source changes between
them), **CK-2D** (69 passed, 2 failed — zero delta from CK-1B, phase
cleanly closed).

One new incidental for Phase 3: `Tests/PlotManager.py:15` uses
lowercase `output/plots` while `.gitignore` and docs use `Output/`.
Windows folds them; Linux/macOS would create two folders.  Small
fix, logged for Phase 3 alongside the `conftest.py` cleanup.

**2026-07-18 (rev 5)** — Phase 1 landed.  (a) `docs/USERS_MANUAL.md`
authored (8-section TOC, self-contained runnable examples, § 3.3
carries R&D chapter references per calendar).  (b) Companion test
`Tests/test_998_users_manual_examples.py` created, mirroring
`test_999_readme_examples.py`.  (c) `docs/TODO_BACKLOG.md` seeded
with **B-01** (Chinese-calendar Appendix-C discrepancy, future
`CM-01`).  (d) `Copilot/` folder retired (five files, none imported
by runtime; content documented an API that no longer exists).
(e) Standards preamble reworded to identify the doc as *portable,
adopted 2026-07-18*.  (f) § 7 decision log filled in with the four
open questions resolved via the plan's own defaults after the owner
said "go".  Gates passed: **CK-1A** (69 passed, 2 failed — one new
passing test, same allowed-red set), **CK-1B** (69 passed, 2 failed —
zero delta from CK-1A after `Copilot/` removal).

**2026-07-18 (rev 4)** — Phase 0 executed.  Baseline pytest and mypy
captured; § 8 added with the allowed-red test set (two Chinese-calendar
Appendix-C tests) and the 293-error mypy histogram used to size
Phase 4 batches.  Two incidentals surfaced (§ 8.3): `pyproject.toml`
mypy override mis-cased (`tests.*` vs `Tests/`), and the stale
`conftest.py` file-order map is spraying 70 lines of "Collected:"
noise per run.  Phase 4 and Phase 3 already cover both.

**2026-07-18 (rev 3)** — Phase 0 baseline-capture step added; new
§ 4.0 defines the checkpoint protocol (label scheme, pass
criterion “no green-in-baseline test is red now”, what to do on
failure).  CHECKPOINT markers now interleaved through Phases 1–5:
1A/1B (docs + Copilot retirement), 2A/2B/2C/2D (per repo-hygiene
task), 3A/3B/3C (per test-suite edit), 4A + 4B-1..13 per docstring
batch + 4C + 4D, and a final CK-5.  Each phase gains explicit
pre-flight greps where a file move or ignore-rule change could
shift a path that a test loads.  A `§ 9 baseline snapshot` will
be created at Phase 0 execution to hold the allowed-red test list.

**2026-07-18 (rev 2)** — Owner feedback folded in.  (a) Architecture
doc and Developer's Handbook removed from Phase 1 deliverables
(deferred indefinitely per owner).  (b) Phase 1 replaced with the
`docs/USERS_MANUAL.md` rename+rewrite of `Copilot/USAGE_GUIDE.md`,
mirroring `README.md` structure and testing pattern; new companion
test `Tests/test_998_users_manual_examples.py` proposed.  (c) New
§ 2.1 promotes R&D citation preservation to a first-class project
principle; suggestion S-7 records it; open question 6.6 asks where
it lives durably.  (d) New suggestion S-8 seeds
`docs/TODO_BACKLOG.md` with B-01, the Chinese-calendar discrepancy
investigation (candidate `CM-01`).  (e) Prefix table in § 2 gains a
"first candidate" column pointing at the new backlog items.  (f)
New open question 6.7 covers User's Manual scope.

**2026-07-18 (rev 1)** — Initial draft.  Audit of the project
against `Coding and Documenting Standards.md` produced the
five-phase plan.  Open questions 6.1–6.5 gate Phase 1.
