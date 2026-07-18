# SPK Universal Timestamp — User's Manual

> **Job of this document.**  Task-oriented guide to `SPK_UniversalTimestamp`
> for people using the library.  Every Python code block in this manual is
> a self-contained runnable snippet; each one is executed by
> [`Tests/test_998_users_manual_examples.py`](../Tests/test_998_users_manual_examples.py)
> on every test run, so an out-of-date example is a test failure, not a
> documentation bug.
>
> **Companion documents.**  [`README.md`](../README.md) covers the same
> ground more compactly for browsers of the GitHub page.
> [`CHANGELOG.md`](../CHANGELOG.md) records version-to-version differences.
> [`docs/plans/`](plans/) holds active work plans.
>
> **What lives elsewhere.**  R&D algorithm references, page numbers, and
> equation numbers live as `# p N (X.Y)` comments **in the source**
> (`SPK_UniversalTimestamp/CC*.py`).  Those citations are load-bearing
> and are the authoritative record of what maps to which R&D theorem.

Last revised: 2026-07-18.

---

## 1 — What SPK_UniversalTimestamp is

A comprehensive multi-scale timestamp system that handles time from
geological epochs (billions of years) to attosecond precision, with
cultural-calendar support (Gregorian, Julian, Hebrew, Chinese) and
astronomical reference (Julian Day Number).  It is built on the
Rata Die (RD) framework of Reingold & Dershowitz, *Calendrical
Calculations: The Ultimate Edition*.

The library exposes two core value types:

* **`UnivMoment`** — a single point in time.  Immutable, orderable,
  representable across every supported calendar.
* **`UnivDuration`** — a time span (positive or negative) expressed as
  a `Decimal` number of seconds plus an integer precision level.

Both are frozen dataclasses; arithmetic on them is value-semantic.


## 2 — Installation and imports

Install from PyPI:

```bash
pip install spk-universal-timestamp
```

Or install from source:

```bash
git clone https://github.com/RoswellMiller/spk-universal-timestamp.git
cd spk-universal-timestamp
pip install -e .
```

Standard imports used throughout this manual:

```python
from decimal import Decimal

from SPK_UniversalTimestamp import (
    UnivMoment,
    UnivDuration,
    UnivMomPrecision,
    Calendar,
)

# Sanity check — nothing else in this block.
assert UnivMoment is not None
assert UnivDuration is not None
```


## 3 — Core concepts

### 3.1 — `UnivMoment`

A `UnivMoment` represents a single instant in time as a pair
`(rd_day, rd_time)` where `rd_day` is the Reingold–Dershowitz Rata
Die day number and `rd_time` is the `(hour, minute, second)` tuple
within that day.  Every calendar-specific constructor converts to
this canonical form.

```python
from decimal import Decimal
from SPK_UniversalTimestamp import UnivMoment, UnivMomPrecision, Calendar

# Construct from a Gregorian date (top-down positional args).
moment = UnivMoment.from_gregorian(2025, 9, 8, 12, 30)
print(moment.format_signature())     # calendar-agnostic signature

# The precision defaults to the finest component you supplied.
# Here MINUTE, because we passed hour and minute but not seconds.
assert moment.precision is UnivMomPrecision.MINUTE

# Present the same moment in each supported calendar.
print(moment.present(Calendar.GREGORIAN, "%Y-%m-%d %H:%M"))
print(moment.present(Calendar.JULIAN,    "%Y-%m-%d %H:%M"))
print(moment.present(Calendar.HEBREW,    "%A %d %B, %Y"))
```

Immutability guarantees that a `UnivMoment` created once is safe to
share across data structures — arithmetic never mutates operands.

### 3.2 — `UnivDuration`

A `UnivDuration` is a time span with an explicit precision level.
Precision is an integer on the same scale used by `UnivMomPrecision`:
`0` = seconds, positive values coarser (days, years, k-years, …),
negative values finer (ms, µs, ns, …).

```python
from decimal import Decimal
from SPK_UniversalTimestamp import UnivDuration

# 90 061 seconds at second precision (level 0).
dur = UnivDuration(90061)
print(dur.format_for_display())          # → "1 day 1 hr 1 min 1 s"

# Same magnitude, but rounded to day precision (level 3).
day_dur = UnivDuration(Decimal("90061"), precision=3)
print(day_dur.format_for_display())      # → "1 day"

# Sub-second: 5.123 seconds at millisecond precision (level -3).
ms_dur = UnivDuration(Decimal("5.123"), precision=-3)
print(ms_dur.format_for_display())       # → "5.123 s"

# Arithmetic — coarser precision wins.
a = UnivDuration(Decimal("86400"), precision=3)   # 1 day, day precision
b = UnivDuration(Decimal("3600"),  precision=0)   # 1 hour, second precision
combined = a + b
print(combined.precision, combined.format_for_display())
```

### 3.3 — `Calendar` — supported systems and their R&D references

| `Calendar` enum member | Status  | R&D chapter |
|:---|:---|:---|
| `GEOLOGICAL` | Done | (project extension — not in R&D) |
| `GREGORIAN`  | Done | 2 (§ 14.1) |
| `JULIAN`     | Done | 3 (§ 14.2) |
| `HEBREW`     | Done | 8 (§ 14.7) |
| `CHINESE`    | Done, with known R&D Appendix-C discrepancies — see § 6 | 19 (§ 15.6) |
| others (`COPTIC`, `ISLAMIC`, `PERSIAN`, …) | Enum entries reserved; not yet implemented | — |

Each implementation lives in a `CC*.py` file whose header names its
R&D chapter and page range.  Individual functions carry
`# p N (X.Y)` comments pointing at the equation they implement.

### 3.4 — Precision

`UnivMoment.PREC_LEVEL` and `UnivDuration.precision` share one
integer scale.  Higher values are coarser; more-negative values are
finer.  `MONTH` is intentionally absent because month length varies
by calendar and therefore cannot express a universal quantum.

```python
from SPK_UniversalTimestamp import UnivMoment, UnivMomPrecision

# Look up a few levels.
assert UnivMoment.PREC_LEVEL[UnivMomPrecision.SECOND]        == 0
assert UnivMoment.PREC_LEVEL[UnivMomPrecision.DAY]           == 3
assert UnivMoment.PREC_LEVEL[UnivMomPrecision.MILLION_YEARS] == 6
assert UnivMoment.PREC_LEVEL[UnivMomPrecision.MICROSECOND]   == -6

# Round-trip: level -> precision -> level.
level = UnivMoment.PREC_LEVEL[UnivMomPrecision.NANOSECOND]
back  = UnivMoment.LEVEL_PREC[level]
assert back is UnivMomPrecision.NANOSECOND
```

See the full table in § 5.1.

### 3.5 — Formatting

Both `UnivMoment` and `UnivDuration` implement Python's `__format__`
protocol, so you can embed them in f-strings with calendar-aware
specifications.

* `f"{moment}"` or `f"{moment:umom}"` — default signature.
* `f"{moment:ucal:<cal>:<fmt>}"` — non-geological calendar output.
* `f"{moment:ugeo:<fmt>}"` — geological output.
* `f"{dur}"` or `f"{dur:udur}"` — default `format_for_display`.
* `f"{dur:udur:<abbrev>}"` — coarsen the duration to the named unit.

```python
from decimal import Decimal
from SPK_UniversalTimestamp import UnivMoment, UnivDuration, UnivMomPrecision

moment = UnivMoment.from_gregorian(2025, 9, 8)
print(f"{moment:ucal:greg:%Y-%m-%d}")           # → "2025-09-08"
print(f"{moment:ucal:gregorian:%A, %B %d, %Y}")
print(f"{moment:ucal:jul:%d/%m/%Y}")            # Julian calendar
print(f"{moment:ucal:heb:%d %B %Y}")            # Hebrew calendar

dur = UnivDuration(90061, precision=0)          # 1 day 1 hr 1 min 1 s
print(f"{dur}")
print(f"{dur:udur:days}")                       # coarsen to day precision
print(f"{dur:udur:mins}")                       # coarsen to minute precision
```

The full format-spec grammar and the exhaustive code table live in
[`README.md`](../README.md#format-spec-reference).


## 4 — Task-oriented recipes

Every recipe below is a self-contained code block runnable in a
fresh interpreter.  Copy, paste, run.

### 4.1 — Convert Gregorian ↔ Julian for a historical date

The Gregorian reform (October 1582) is the canonical worked example:
the 10-day gap where Julian dates and Gregorian dates disagree.

```python
from SPK_UniversalTimestamp import UnivMoment, Calendar

# The day Pope Gregory XIII decreed as "Friday 15 October 1582"
# (Gregorian) was formerly "Friday 5 October 1582" (Julian).
first_gregorian_day = UnivMoment.from_gregorian(1582, 10, 15)
print(first_gregorian_day.present(Calendar.GREGORIAN, "%Y-%m-%d"))
print(first_gregorian_day.present(Calendar.JULIAN,    "%Y-%m-%d"))

# Same moment, constructed from the Julian side, must yield the same RD.
same_moment_from_julian = UnivMoment.from_julian(1582, 10, 5)
assert first_gregorian_day.rd_moment() == same_moment_from_julian.rd_moment()
```

### 4.2 — Represent a Hebrew calendar date

```python
from SPK_UniversalTimestamp import UnivMoment, Calendar

# First day of Passover — 15 Nisan 5785 in the Hebrew calendar.
# Nisan is month 1 in the ecclesiastical count; the R&D convention
# uses month 1 for Nisan (see CC08_Hebrew.py header).
pesach = UnivMoment.from_hebrew(5785, 1, 15)
print(pesach.present(Calendar.HEBREW,    "%d %B %Y"))
print(pesach.present(Calendar.GREGORIAN, "%A, %Y-%m-%d"))
```

### 4.3 — Represent a Chinese calendar date

The Chinese-calendar constructor takes the **sexagenary cycle number**
first, then the year within the cycle (1–60), then month, then day.
Cycle 78 year 42 is Gregorian 2025.

```python
from SPK_UniversalTimestamp import UnivMoment, Calendar

# Cycle 78 year 42, month 8, day 15 — the mid-autumn (moon) festival
# roughly corresponds to this civil date range.  The exact Gregorian
# projection may differ from R&D published values; see § 6.
mid_autumn = UnivMoment.from_chinese(78, 42, 8, 15)
print(mid_autumn.present(Calendar.CHINESE,   "%d/%m/%Y (%C)"))
print(mid_autumn.present(Calendar.GREGORIAN, "%Y-%m-%d"))
```

> **Known limitation.**  The Chinese-calendar implementation
> currently differs from R&D Appendix C on several astronomical
> quantities.  See § 6 and backlog item `B-01` in
> [`docs/TODO_BACKLOG.md`](TODO_BACKLOG.md).

### 4.4 — Express a geological interval

```python
from SPK_UniversalTimestamp import UnivMoment, UnivMomPrecision, Calendar

# Cretaceous–Paleogene (K–Pg) boundary: ~66 Ma.
kpg = UnivMoment.from_geological(66, precision=UnivMomPrecision.MILLION_YEARS)
print(f"{kpg:ugeo:%y %O}")     # e.g. "-66.00 M-yr Phanerozoic"

# The Big Bang, represented as the beginning of time.
big_bang = UnivMoment.beginning_of_time()
print(big_bang.format_signature())
```

### 4.5 — Compute the span between two moments

Subtracting two `UnivMoment`s yields a `UnivDuration`.  Adding a
`UnivDuration` to a `UnivMoment` yields a new `UnivMoment`.

```python
from decimal import Decimal
from SPK_UniversalTimestamp import UnivMoment, UnivDuration, Calendar

t0 = UnivMoment.from_gregorian(2025, 1, 1)
t1 = UnivMoment.from_gregorian(2025, 12, 31)

span = t1 - t0                       # UnivDuration
print(span.format_for_display())     # → "364 days"  (2025 is not a leap year)

# Add a duration back.
one_week = UnivDuration(Decimal("604800"), precision=3)   # 7 days
next_week = t0 + one_week
print(next_week.present(Calendar.GREGORIAN, "%Y-%m-%d"))
```

### 4.6 — Sort a heterogeneous list of moments

`UnivMoment` implements all six comparison operators, so plain
`sorted()` works across calendars and precisions.  Ordering is by
Rata Die: geological moments (deep negative RD) come before AD
moments; sub-second precision preserves order down to attoseconds.

```python
from SPK_UniversalTimestamp import UnivMoment, UnivMomPrecision, Calendar

moments = [
    UnivMoment.from_gregorian(2025, 9, 8),
    UnivMoment.from_geological(66, precision=UnivMomPrecision.MILLION_YEARS),
    UnivMoment.from_julian(1582, 10, 5),
    UnivMoment.from_hebrew(5785, 1, 15),
    UnivMoment.beginning_of_time(),
]

for m in sorted(moments):
    print(m.format_signature())
```

### 4.7 — Round-trip through JSON

`to_dict()` returns a JSON-safe dictionary; `from_dict()` reconstructs
the same `UnivMoment` (or `UnivDuration`).

```python
import json
from SPK_UniversalTimestamp import UnivMoment

original = UnivMoment.from_gregorian(2025, 9, 8, 12, 30)

payload = json.dumps(original.to_dict())
recovered = UnivMoment.from_dict(json.loads(payload))

assert recovered == original
print("round-trip ok:", original == recovered)
```

### 4.8 — Round-trip through a sortable lexical key

For storage systems that only sort strings (e.g. some KV stores),
`to_StdLexicalKey()` produces a string that sorts identically to the
underlying `UnivMoment` order.

```python
from SPK_UniversalTimestamp import UnivMoment

original = UnivMoment.from_gregorian(2025, 9, 8, 12, 30)

key = original.to_StdLexicalKey()
recovered = UnivMoment.from_StdLexicalKey(key)

assert recovered == original
print("lexical key:", key)
```


## 5 — Reference tables

### 5.1 — Precision levels

The full table appears in
[`README.md`](../README.md#precision-level-reference); a summary:

| Level | `UnivMomPrecision`   | Quantum          |
|------:|:---------------------|:-----------------|
|     7 | `BILLION_YEARS`      | 10⁹ Julian years |
|     6 | `MILLION_YEARS`      | 10⁶ Julian years |
|     5 | `THOUSAND_YEARS`     | 10³ Julian years |
|     4 | `YEAR`               | 1 Julian year    |
|     3 | `DAY`                | 86 400 s         |
|     2 | `HOUR`               | 3 600 s          |
|     1 | `MINUTE`             | 60 s             |
|     0 | `SECOND`             | 1 s              |
|    −3 | `MILLISECOND`        | 10⁻³ s           |
|    −6 | `MICROSECOND`        | 10⁻⁶ s           |
|    −9 | `NANOSECOND`         | 10⁻⁹ s           |
|   −12 | `PICOSECOND`         | 10⁻¹² s          |
|   −15 | `FEMTOSECOND`        | 10⁻¹⁵ s          |
|   −18 | `ATTOSECOND`         | 10⁻¹⁸ s          |

Programmatic access:

```python
from SPK_UniversalTimestamp import UnivMoment, UnivMomPrecision

# All four class-level mappings are frozen (MappingProxyType).
prec = UnivMomPrecision.MILLISECOND
print(UnivMoment.PREC_LEVEL[prec])    # → -3
print(UnivMoment.PREC_ABBREV[prec])   # → "ms"

# LEVEL_PREC is the reverse of PREC_LEVEL.
assert UnivMoment.LEVEL_PREC[-6] is UnivMomPrecision.MICROSECOND
```

### 5.2 — Format-spec prefixes

| Prefix   | Target             | Grammar                              |
|:---------|:-------------------|:-------------------------------------|
| `umom`   | `UnivMoment`       | `f"{m:umom}"` — signature default    |
| `ucal:`  | `UnivMoment`       | `ucal:<cal>:<fmt>`                   |
| `ugeo:`  | `UnivMoment`       | `ugeo:<fmt>` — geological calendar   |
| `udur`   | `UnivDuration`     | `f"{d:udur}"` — display default      |
| `udur:`  | `UnivDuration`     | `udur:<abbrev>` — coarsen to abbrev  |

Calendar abbreviations for `ucal:` (case-insensitive):
`gregorian`/`greg`, `julian`/`jul`/`jc`, `hebrew`/`heb`/`am`,
`chinese`/`chin`/`cc`.  Full code tables appear in `README.md`.


## 6 — Known limitations

* **Chinese calendar — R&D Appendix C discrepancies.**  Several
  moments constructed via `UnivMoment.from_chinese(...)` disagree
  with the reference values printed in R&D Appendix C, typically by
  one to three days on the month/day fields, occasionally on the
  leap-month flag.  The two tests
  `Tests/test_400_Moment_cPresent_Chinese.py::test_appendix_c_*` pin
  the divergence.  Root cause is astronomical: the R&D solar-longitude
  and lunar-position computations require a level of ephemeris
  accuracy that the current pure-Python implementation does not
  reach.  A version 2 tied to the JPL DE422 standard is anticipated;
  it is seeded as backlog item **B-01**
  (see [`docs/TODO_BACKLOG.md`](TODO_BACKLOG.md)) for a future
  `CM-01` plan.
* **Month precision is not a supported `UnivMomPrecision`.**  Month
  length varies by calendar (Hebrew leap year has 13 months, Chinese
  ditto with a different rule); "one month" cannot express a
  universal quantum.  Use `DAY` for day-level precision and format
  as month/day pairs when a month view is needed.
* **`float` is used only at I/O boundaries.**  All internal math uses
  `Decimal` at 50-digit precision (`UnivMoment`) or 30-digit
  (`CC00_Decimal_library`).  Passing `float` values into
  constructors that expect `Decimal` may silently lose precision at
  the sub-second scale.
* **Time zones are not first-class on `UnivMoment`.**  The library
  treats the RD as UTC-anchored; local-time conversion is available
  through `CC14_Time_and_Astronomy` helpers when astronomical
  computations require it.
* **The library emits no progress or diagnostic output.**  It is a
  computational core; callers write their own logging.


## 7 — Where to look next

* [`README.md`](../README.md) — quick-start and the exhaustive
  format-spec / calendar-code reference tables.
* [`CHANGELOG.md`](../CHANGELOG.md) — version-to-version diffs and
  post-mortems for landed defects.
* [`docs/Coding and Documenting Standards.md`](Coding%20and%20Documenting%20Standards.md)
  — the portable coding conventions this project follows.
* [`docs/plans/`](plans/) — active work plans, including the plan
  that produced this manual (`PL-01`).
* [`docs/TODO_BACKLOG.md`](TODO_BACKLOG.md) — durable open items not
  yet activated into plans.
* The R&D book — the authoritative source for every algorithm in
  `SPK_UniversalTimestamp/CC*.py`.  Each `CC*` module names the
  chapter and page range it implements; individual functions carry
  page/equation citations.


## 8 — Change log

**2026-07-18** — Initial issue, replacing the retired
`Copilot/USAGE_GUIDE.md`.  Structure mirrors `README.md`; every
` ```python ` block executes under
`Tests/test_998_users_manual_examples.py`.  Landed as part of
`docs/plans/PL-01_C_and_D_Standards_Update.md` Phase 1.
