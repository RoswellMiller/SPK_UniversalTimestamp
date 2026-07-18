"""
UnivDuration — immutable, multi-scale time span with automatic
precision snapping.

**Purpose.**  Represent "how long" independently of any calendar,
from attoseconds (10⁻¹⁸ s) to gigayears (10⁹ years).  Every
instance carries a raw duration in seconds (as `Decimal`) plus a
coarseness level derived from the input magnitude via
`_auto_precision`.  Arithmetic between two `UnivDuration` values
promotes to the coarser of the two levels so that a millisecond +
a gigayear rounds to a gigayear rather than pretending to preserve
millisecond precision.

**Public surface (star-exported via `__init__.py`).**
    `UnivDuration` — dataclass with constructor helpers
    (`from_dict`, `from_StdLexicalKey`, `from_string`), display
    formatters (`to_dict`, `to_StdLexicalKey`, `format_for_display`,
    `__str__`, `__repr__`, `__format__`), full comparison protocol
    (`__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__hash__`),
    and arithmetic (`__add__`, `__sub__`).

**Module-private helpers.**  `_dur_level`, `_level_quantum`,
`_abbrev`, `_auto_precision` — support functions used by the
formatters and arithmetic; not part of the public API.

**Precision level convention.**
    Positive levels 1–7: named units (seconds up through gigayears)
    stored in `UnivDuration.LEVEL_QUANTUM` / `LEVEL_ABBREV`.
    Zero:              seconds.
    Negative levels:   powers of ten below the second (−3 = ms,
        −6 = µs, −9 = ns, −12 = ps, −15 = fs, −18 = as).

**Not in scope.**  Anything anchored to a specific instant in time
(that's `UnivMoment`), calendar-specific durations like "1 month"
(months are not universal quanta — see `UnivMomPrecision`).

**Change history.**  See `CHANGELOG.md`.
"""

import re

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_EVEN
from types import MappingProxyType
from typing import ClassVar



def _dur_level(dur: "UnivDuration") -> int:
    """Numeric coarseness level: negative for sub-second, 0+ for whole-second precisions."""
    return dur.precision


def _level_quantum(level: int) -> Decimal:
    """Seconds per quantum for the given coarseness level."""
    if level < 0:
        return Decimal(10) ** level
    return UnivDuration.LEVEL_QUANTUM[level]


def _abbrev(level: int, count: int) -> str:
    """Abbreviation for *level*, singular (no trailing 's') when count == 1."""
    label = UnivDuration.LEVEL_ABBREV.get(level, f"10^{level}s")
    if count == 1 and 1 <= level <= 7:   # only named units carry a plural 's'
        label = label.rstrip("s")
    return label


def _auto_precision(seconds: Decimal) -> int:
    """Return the coarsest level whose quantum is <= abs(seconds).

    Scans from the coarsest unit (level 7, G-years) down to the finest
    (level -18, attoseconds) and returns the first level whose quantum
    does not exceed the magnitude.  Returns 0 (seconds) for a zero value.
    """
    abs_s = abs(seconds)
    if abs_s == 0:
        return 0
    for level in range(7, -1, -1):
        if abs_s >= UnivDuration.LEVEL_QUANTUM[level]:
            return level
    for level in range(-1, -19, -1):
        if abs_s >= Decimal(10) ** level:
            return level
    return -18


@dataclass(frozen=True)
class UnivDuration:
    """
    Immutable, multi-scale time span.

    Instances carry `seconds` (`Decimal`) and a `precision` level
    integer (0 = seconds, positive = coarser named units up through
    G-years, negative = powers of ten below the second down to
    attoseconds).  Arithmetic promotes to the coarser precision of
    two operands; construction from a magnitude auto-selects the
    coarsest level whose quantum does not exceed `abs(seconds)`.

    Class-level tables:
        `LEVEL_QUANTUM`        — level → seconds-per-quantum.
        `LEVEL_ABBREV`         — level → short abbreviation.
        `ABBREV_LEVEL`         — reverse map for string parsing;
            includes both plural and singular forms for named units.
        `MAX_FINE_FOR_COARSE`  — span constraint per coarsest level
            (a G-year compound may be no finer than year; a year
            compound may go to microseconds; etc.).
    """
    # CONSTANTS ##################################################################################################
    @staticmethod
    def __version__():
        return "2.0.3"

    @staticmethod
    def __file__():
        return "SPK_UniversalTimestamp\\UnivDuration.py"

    # --- Class-level read-only lookup tables ---
    LEVEL_QUANTUM: ClassVar[MappingProxyType] = MappingProxyType({
        0: Decimal("1"),
        1: Decimal("60"),
        2: Decimal("3600"),
        3: Decimal("86400"),
        4: Decimal("31557600"),
        5: Decimal("31557600000"),
        6: Decimal("31557600000000"),
        7: Decimal("31557600000000000"),
    })

    LEVEL_ABBREV: ClassVar[MappingProxyType] = MappingProxyType({
        # Coarse / whole-second units
         7: "G-years",
         6: "M-years",
         5: "k-years",
         4: "years",
         3: "days",
         2: "hrs",
         1: "mins",
         0: "s",
        # Sub-second units (10^N seconds)
        -1:  "ds",
        -2:  "cs",
        -3:  "ms",
        -4:  "100µs",
        -5:  "10µs",
        -6:  "µs",
        -7:  "100ns",
        -8:  "10ns",
        -9:  "ns",
        -10: "100ps",
        -11: "10ps",
        -12: "ps",
        -13: "100fs",
        -14: "10fs",
        -15: "fs",
        -16: "100as",
        -17: "10as",
        -18: "as",
    })

    # Build reverse map: abbreviation -> level.
    # Include both the stored plural form and the singular (strip trailing 's')
    # for named units at levels 1-7 so that format_for_display output round-trips.
    # Also include non-SI allowed abbreviations: 'd' (day) and 'h' (hour).
    ABBREV_LEVEL: ClassVar[MappingProxyType] = MappingProxyType({
        **{abbrev: level for level, abbrev in LEVEL_ABBREV.items()},
        **{abbrev[:-1]: level for level, abbrev in LEVEL_ABBREV.items()
            if 1 <= level <= 7 and abbrev.endswith("s")},  # e.g. "days" -> "day"
        'd': 3,   # day    SI allowed non-SI unit abbreviation
        'h': 2,   # hour   SI allowed non-SI unit abbreviation
        #'m': 1,   # minute (compact abbreviation) not allowed in SI (m is meter)
    })

    # Finest precision level allowed for each coarsest unit level.  Checked by from_string().
    # Keys are coarsest-unit levels 0-7; values are the most-negative (finest) level allowed.
    # E.g. a G-year compound may be no finer than year (level 4).
    # Adjust the values here to tighten or loosen the span constraints.
    MAX_FINE_FOR_COARSE: ClassVar[MappingProxyType] = MappingProxyType({
        7:  4,   # G-years  → years finest         (span  3)
        6:  2,   # M-years  → hours finest          (span  4)
        5:  0,   # k-years  → seconds finest        (span  5)
        4: -6,   # years    → microseconds finest   (span 10)
        3: -6,   # days     → microseconds finest   (span  9)
        2: -9,   # hours    → nanoseconds finest    (span 11)
        1: -12,  # minutes  → picoseconds finest    (span 13)
        0: -18,  # seconds  → attoseconds finest    (span 18, no restriction)
    })

    seconds   : Decimal     # Total duration in seconds; may be negative (duration in the past)
    precision : int = 0     # Coarseness level: 0=second, positive=coarser, negative=sub-second
                            # Matches MomPrecLevel values: e.g. 3=day, 7=billion-year, -3=ms

    def __post_init__(self):
        if isinstance(self.seconds, Decimal):
            pass
        elif isinstance(self.seconds, int):
            object.__setattr__(self, "seconds", Decimal(self.seconds))
        else:
            raise TypeError("seconds must be a Decimal or int")
        if not isinstance(self.precision, int):
            raise TypeError("precision must be an int (e.g. 0=second, 3=day, -3=millisecond)")
        if not (-18 <= self.precision <= 7):
            raise ValueError(f"precision {self.precision} is out of range [-18, 7]")

    # Support for JSON serialization
    def to_dict(self) -> dict:
        """
        Convert the UnivDuration to a dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the UnivDuration
        """
        data = {
            "seconds":   str(self.seconds),
            "precision": str(self.precision),   # always a plain int string, e.g. "0", "3", "-3"
        }
        return data
    @staticmethod
    def from_dict(data: dict) -> "UnivDuration":
        """
        Create a UnivDuration from a dictionary.

        Args:
            data (dict): Dictionary representation of the UnivDuration
        Returns:
            UnivDuration: Created UnivDuration object
        """
        seconds   = Decimal(data["seconds"])
        precision = int(data["precision"])    # always stored as a plain int string
        return UnivDuration(seconds, precision)
    # Support for sorting and comparison lexically
    def to_StdLexicalKey(self) -> str:
        """
        Convert the UnivMoment to a standardized lexical key for sorting and comparison.

        Returns:
            str: Standardized lexical key representing the UnivMoment
        """
        abs_secs   = abs(self.seconds)
        int_part   = int(abs_secs)
        frac_part  = abs_secs - Decimal(int_part)
        frac_digits = int(frac_part * Decimal("1" + "0" * 18))

        if self.precision < 0:
            prec_code = 18 + self.precision   # e.g. -3 → 15
            type_char = "L"
        else:
            prec_code = self.precision        # 0=second, 3=day, 7=billion-year
            type_char = "P"

        return f"univDU{int_part:018d}.{frac_digits:018d}.{prec_code:02d}{type_char}"
    @staticmethod
    def from_StdLexicalKey(lex_key: str) -> "UnivDuration":
        """
        Create a UnivMoment from a standardized lexical key.

        Args:
            lex_key (str): Standardized lexical key representing the UnivMoment
        """
        pattern = r"^univDU(?P<mantissa>\d{18})\.(?P<fraction>\d{18})\.(?P<prec>\d{2})(?P<type>[LP])$"
        match = re.match(pattern, lex_key)
        if not match:
            raise ValueError("Invalid lexical key format for UnivDuration")

        int_part  = int(match.group("mantissa"))
        frac_str  = match.group("fraction")
        prec_code = int(match.group("prec"))
        type_char = match.group("type")

        seconds = Decimal(f"{int_part}.{frac_str}")

        if type_char == "L":
            precision = prec_code - 18    # e.g. 15 → -3 (milliseconds)
        else:
            precision = prec_code         # 0=second, 3=day, 7=billion-year

        return UnivDuration(seconds, precision)

    @classmethod
    def from_string(cls, text: str) -> "UnivDuration":
        """
        Construct a UnivDuration from a human-readable compound string.

        Each ``<number> <unit>`` pair contributes to the total seconds.  The
        unit must be one of the abbreviations in LEVEL_ABBREV; both singular
        and plural forms of named units (levels 1-7) are accepted.

        Precision is determined by the finest effective level across all pairs,
        where decimal places on a value subdivide its unit one level per digit:

            '10.001 s'      → precision -3  (milliseconds)
            '10.5 M-years'  → precision  5  (k-years)
            '1 day 2 hrs'   → precision  2  (hours)
            '1 day 2.5 hrs' → precision  1  (minutes)

        Raises ValueError if no valid (number, unit) pairs are found, or if
        the span between the coarsest and finest level exceeds the limit defined
        in MAX_FINE_FOR_COARSE.
        """
        # Build reverse map: abbreviation -> level.
        # Include both the stored plural form and the singular (strip trailing 's')
        # for named units at levels 1-7 so that format_for_display output round-trips.
        # abbrev_to_level: dict[str, int] = {}
        # for level, abbrev in cls.LEVEL_ABBREV.items():
        #     abbrev_to_level[abbrev] = level
        #     if 1 <= level <= 7 and abbrev.endswith("s"):
        #         abbrev_to_level[abbrev[:-1]] = level   # e.g. "days" -> "day"

        # Sort longest-first so the regex won't match "s" inside "days", etc.
        sorted_abbrevs = sorted(cls.ABBREV_LEVEL, key=len, reverse=True)
        abbrev_pat = "|".join(re.escape(a) for a in sorted_abbrevs)

        # Strip a single leading '-' — it negates the whole duration, not individual components.
        stripped = text.strip()
        if stripped.startswith("-"):
            negative = True
            stripped = stripped[1:].lstrip()
        else:
            negative = False

        pair_re = re.compile(rf"(\d+(?:\.\d+)?)\s*({abbrev_pat})")
        pairs = pair_re.findall(stripped)
        if not pairs:
            raise ValueError(f"No valid (number, unit) pairs found in: {text!r}")

        total_seconds  = Decimal(0)
        finest_prec    = 7   # reduced toward the finest (most negative) level seen
        coarsest_prec  = -18 # raised toward the coarsest (most positive) level seen

        for num_str, abbrev in pairs:
            level   = cls.ABBREV_LEVEL[abbrev]
            quantum = cls.LEVEL_QUANTUM[level] if level >= 0 else Decimal(10) ** level
            total_seconds += Decimal(num_str) * quantum

            dec_places     = len(num_str.split(".")[1]) if "." in num_str else 0
            effective_prec = level - dec_places
            if effective_prec < finest_prec:
                finest_prec = effective_prec
            if level > coarsest_prec:
                coarsest_prec = level

        if negative:
            total_seconds = -total_seconds

        finest_prec = max(-18, min(7, finest_prec))

        # Validate precision span against MAX_FINE_FOR_COARSE
        allowed_finest = cls.MAX_FINE_FOR_COARSE.get(coarsest_prec)
        if allowed_finest is not None and finest_prec < allowed_finest:
            coarsest_abbrev = cls.LEVEL_ABBREV.get(coarsest_prec, f"10^{coarsest_prec}s")
            finest_abbrev   = cls.LEVEL_ABBREV.get(finest_prec,   f"10^{finest_prec}s")
            allowed_abbrev  = cls.LEVEL_ABBREV.get(allowed_finest, f"10^{allowed_finest}s")
            raise ValueError(
                f"Precision span too large: coarsest unit {coarsest_abbrev!r} (level "
                f"{coarsest_prec}) cannot be combined with precision {finest_abbrev!r} "
                f"(level {finest_prec}). Finest allowed for {coarsest_abbrev!r} is "
                f"{allowed_abbrev!r} (level {allowed_finest}). "
                f"See UnivDuration.MAX_FINE_FOR_COARSE."
            )

        return cls(total_seconds, finest_prec)

    # --- Comparison operators (ordered by total seconds) ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self.seconds == other.seconds

    def __hash__(self) -> int:
        return hash(self.seconds)

    def __lt__(self, other: "UnivDuration") -> bool:
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self.seconds < other.seconds

    def __le__(self, other: "UnivDuration") -> bool:
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self.seconds <= other.seconds

    def __gt__(self, other: "UnivDuration") -> bool:
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self.seconds > other.seconds

    def __ge__(self, other: "UnivDuration") -> bool:
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self.seconds >= other.seconds

    # --- Arithmetic operators ---

    def _combine(self, raw_seconds: Decimal, other: "UnivDuration") -> "UnivDuration":
        """Round raw_seconds to the coarser of self/other (half-even), return new UnivDuration."""
        coarse_level = max(self.precision, other.precision)
        q = _level_quantum(coarse_level)
        rounded = (raw_seconds / q).to_integral_value(rounding=ROUND_HALF_EVEN) * q
        return UnivDuration(rounded, coarse_level)

    def __add__(self, other: "UnivDuration") -> "UnivDuration":
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self._combine(self.seconds + other.seconds, other)

    def __sub__(self, other: "UnivDuration") -> "UnivDuration":
        if not isinstance(other, UnivDuration):
            return NotImplemented
        return self._combine(self.seconds - other.seconds, other)

    def format_for_display(self, format: str | None = None) -> str:
        """
        Decompose the duration into a human-readable compound string scaled to
        the stored precision level (or *format* when supplied).

        For precisions coarser than or equal to seconds the value is decomposed
        into whole-unit pairs (e.g. "1 day 1 hr 1 min 1 s").  For sub-second
        precisions the decomposition stops at minutes and the remaining seconds
        are expressed as a single decimal number with exactly ``abs(precision)``
        digits after the point.

        For year-scale precisions (years, k-years, M-years, B-years) the value
        is shown as a single decimal number at the coarsest fitting unit with
        four decimal places, e.g. "17.7000 M-years".

        Decompose mode (``format`` prefixed with ``>``):
            Decompose from the coarsest containing unit down to the specified
            level.  All levels above the target are shown as integers; the
            target (finest) level uses four decimal places when year-scale or
            ``abs(precision)`` decimal places when sub-second.

            Example:
                UnivDuration(1.75 * Q[7], precision=7).format_for_display(">M-years")
                    → "1 B-year 750 M-years"
                UnivDuration(1.7321 * Q[6], precision=6).format_for_display(">k-years")
                    → "1 M-year 732.1000 k-years"

        Docstring examples (single-unit mode):
            UnivDuration(31557600000000, M_YEAR)     → "1 M-year"
            UnivDuration(90061, SECOND)              → "1 day 1 hr 1 min 1 s"
            UnivDuration(3661,  MINUTE)              → "1 hr 1 min"
            UnivDuration(Decimal('90061.123'), -3)   → "1 day 1 hr 1 min 1.123 s"
            UnivDuration(Decimal('5.123'), -3)       → "5.123 s"
            UnivDuration(Decimal('0.001'), -3)       → "0.001 s"
            UnivDuration(Decimal('0.000000001'), -9) → "0.000000001 s"
        """
        # --- Detect decompose mode (leading ">") ---
        decompose = False
        if format is not None:
            if format.startswith(">"):
                decompose = True
                format    = format[1:]
            if format not in UnivDuration.ABBREV_LEVEL:
                raise ValueError(
                    f"Unknown duration precision abbreviation {format!r}. "
                    f"Valid abbreviations: {sorted(UnivDuration.ABBREV_LEVEL.keys())}."
                )
            bottom = UnivDuration.ABBREV_LEVEL[format]
        else:
            if self.precision >= 4:
                # For year-scale precisions, coarsen to the largest unit that fits
                # the magnitude (e.g. 10.5 M-years at k-year precision → M-year level).
                bottom = max(_auto_precision(self.seconds), self.precision)
            else:
                bottom = self.precision

        sign     = "-" if self.seconds < 0 else ""
        abs_secs = abs(self.seconds)

        # ------------------------------------------------------------------
        # Single-unit year-scale path (default / no ">")
        # Show the entire value as one decimal number at the target level.
        # ------------------------------------------------------------------
        if not decompose and bottom >= 4:
            q       = UnivDuration.LEVEL_QUANTUM[bottom]
            value   = abs_secs / q
            int_val = int(value)
            if value != int_val:
                display = f"{value:.4f} {_abbrev(bottom, 2)}"   # always plural
            else:
                display = f"{int_val} {_abbrev(bottom, int_val)}"
            # Suppress sign only for true negative-zero (all displayed digits are 0).
            if sign and not any(c in '123456789' for c in display):
                return display
            return sign + display

        # ------------------------------------------------------------------
        # Decomposition path (time units OR decompose mode with ">")
        # ------------------------------------------------------------------
        loop_floor = 1 if bottom < 0 else bottom
        remaining  = abs_secs
        parts: list[str] = []

        for level in range(7, loop_floor - 1, -1):
            q = UnivDuration.LEVEL_QUANTUM[level]
            if level == loop_floor and decompose and bottom >= 4:
                # Final year-scale level in decompose mode: 4 decimal places.
                value   = remaining / q
                int_val = int(value)
                if value != int_val:
                    if value > 0 or not parts:
                        parts.append(f"{value:.4f} {_abbrev(level, 2)}")
                else:
                    if int_val > 0 or not parts:
                        parts.append(f"{int_val} {_abbrev(level, int_val)}")
            else:
                count = int(remaining / q)
                if count > 0:
                    parts.append(f"{count} {_abbrev(level, count)}")
                    remaining -= count * q

        if bottom < 0:
            # Express remaining seconds as a decimal to abs(bottom) decimal places.
            decimal_places = abs(bottom)
            quantum        = Decimal(10) ** bottom
            quantized      = remaining.quantize(quantum, rounding=ROUND_HALF_EVEN)
            if quantized > 0 or not parts:
                parts.append(f"{quantized:.{decimal_places}f} s")

        if not parts:
            label = _abbrev(bottom, 0)
            parts.append(f"0 {label}")

        display = " ".join(parts)
        # Suppress the minus sign only when the formatted output is true negative-zero
        # (i.e. every displayed digit is 0; a value like -0.0035 M-years keeps its sign).
        if sign and not any(c in '123456789' for c in display):
            return display
        return sign + display

    def __format__(self, spec: str) -> str:
        """
        Format the duration using a format spec.

        Format spec grammar::

            spec   ::= "" | "udur" | "udur:" [">" ] abbrev
            abbrev ::= one of the LEVEL_ABBREV values (e.g. "s", "ms", "days", "µs")

        A leading ``>`` before the abbreviation enables decompose mode: the value
        is broken into integer counts at each unit above the target, with decimal
        places only at the target (finest) level.

        Examples::

            f"{dur}"              →  auto-detect coarsest unit whose quantum <= abs(seconds)
            f"{dur:udur}"         →  format_for_display() at stored precision
            f"{dur:udur:ms}"      →  single-unit display at millisecond precision
            f"{dur:udur:days}"    →  single-unit display at day precision
            f"{dur:udur:>M-years}"→  decompose down to M-years (integer B-years above)
        """
        if spec == "":
            auto_level  = _auto_precision(self.seconds)
            auto_abbrev = UnivDuration.LEVEL_ABBREV.get(auto_level, f"10^{auto_level}s")
            return self.format_for_display(format=auto_abbrev)
        if spec == "udur":
            return self.format_for_display()
        if spec.startswith("udur:"):
            return self.format_for_display(format=spec[5:])
        raise ValueError(f"Unsupported UnivDuration format spec {spec!r}")

    def __str__(self) -> str:
        if self.precision < 0:
            return f"UnivDuration({self.seconds}, {self.precision})"
        return f"UnivDuration({self.seconds})"
    
    def __repr__(self) -> str:
        return f"UnivDuration(seconds={self.seconds}, precision={self.precision})"