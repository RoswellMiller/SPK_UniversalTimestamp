# SPK Universal Timestamp — TODO Backlog

> **Job of this document.**  Durable open items that do not yet have
> a plan document in [`docs/plans/`](plans/).  When a backlog item is
> activated, it graduates to a plan (prefix per PL-01 § 2: `PL-N`,
> `CM-N`, `AS-N`, `API-N`, or `T-N`) and its `B-N` id is retired here
> with a pointer to the plan.
>
> **Companion documents.**  [`docs/plans/`](plans/) — active plans.
> [`CHANGELOG.md`](../CHANGELOG.md) — landed changes.
>
> **What does not belong here.**  Session-scoped todos (those live in
> the agent/editor todo tracker only) and questions whose answer is
> "this will not be done" (those belong in the change log of the
> document that first proposed them).

Last revised: 2026-07-18.


## Open items

### B-01 — Chinese-calendar Appendix-C discrepancy investigation

**Status**: open, awaiting activation as plan `CM-01`.
**Priority**: medium — the discrepancy is documented in `CHANGELOG.md`
[1.0.0] and reproduced by two failing tests, but the library ships
usable Chinese-calendar output for the vast majority of dates.
**Symptom.**  The following two tests fail against R&D Appendix C
reference values:

* `Tests/test_400_Moment_cPresent_Chinese.py::Test_Moment_Chinese::test_appendix_c_Construction`
* `Tests/test_400_Moment_cPresent_Chinese.py::Test_Moment_Chinese::test_appendix_c_Presentation`

The failures are month/day slips (typically 1–3 units) and, on one
row, a leap-month flag disagreement.

**Suspected root cause.**  The astronomical routines used by
`CC19_Chinese_1645.py` — solar longitude, lunar new moon, sexagesimal
term boundaries — depend on ephemeris quality that the current
pure-Python R&D implementation does not achieve.

**Recommended plan.**  A `CM-01` plan that:

1. Reproduces every R&D Appendix C row as an isolated test case with
   the intermediate astronomical quantities (solar longitude at
   winter solstice, new-moon RDs before/after key markers) exposed.
2. Diffs each intermediate against R&D published values.
3. Decides between (a) tightening the existing R&D pure-Python
   routines to close the gap, or (b) replacing them with a JPL
   DE422 ephemeris interface as anticipated in `CHANGELOG.md` [1.0.0].
4. If (b) is chosen, factors the astronomical layer behind a
   dependency-injection seam so pure-R&D and DE422-backed
   implementations can be swapped for verification.

**Referenced by.**  PL-01 § 5 S-8 and § 8; `USERS_MANUAL.md` § 6;
`CHANGELOG.md` [1.0.0].


### B-02 — `psoEarth.__ne__` returns wrong value for equal points

**Status**: open, needs a small fix + regression test.
**Priority**: low — `psoEarth` is a geometry helper on `Astro_Space.py`;
no current test exercises `!=` on two equal instances so the bug is
latent.

**Symptom.**  Given two `psoEarth` objects `a == b`, `a != b`
currently evaluates to `True` instead of `False`.

**Root cause.**  `Astro_Space.py::psoEarth.__ne__` calls
`self.__eq__(other.point)` — passing the underlying `shapely.Point`
into `__eq__`, which expects a `psoEarth`.  `__eq__` returns `False`
for the non-`psoEarth` argument, so `__ne__` returns `not False =
True` regardless of actual equality.  Should be `self.__eq__(other)`.

**Discovered.**  PL-01 Phase 4 Task 1 (2026-07-18) — surfaced when
adding type hints on the dunders.  Preserved with `# type: ignore`
+ this backlog reference because PL-01 Phase 4 is charter-limited
to non-behavioural changes.

**Recommended plan.**  A small `API-01` (or `T-01`) that:

1. Adds a regression test for `!=` on two identical `psoEarth`
   instances and on `!=` between a `psoEarth` and a non-`psoEarth`.
2. Changes `other.point` → `other` in `Astro_Space.py::psoEarth.__ne__`.
3. Removes the `# type: ignore[attr-defined]` comment left by
   PL-01.


## Retired items

_(none yet — items move here with a pointer to the plan that
absorbed them.)_
