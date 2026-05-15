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


@dataclass(frozen=True)
class UnivDuration:
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
         7: "B-years",
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

        Raises ValueError if no valid (number, unit) pairs are found.
        """
        # Build reverse map: abbreviation -> level.
        # Include both the stored plural form and the singular (strip trailing 's')
        # for named units at levels 1-7 so that format_for_display output round-trips.
        abbrev_to_level: dict[str, int] = {}
        for level, abbrev in cls.LEVEL_ABBREV.items():
            abbrev_to_level[abbrev] = level
            if 1 <= level <= 7 and abbrev.endswith("s"):
                abbrev_to_level[abbrev[:-1]] = level   # e.g. "days" -> "day"

        # Sort longest-first so the regex won't match "s" inside "days", etc.
        sorted_abbrevs = sorted(abbrev_to_level, key=len, reverse=True)
        abbrev_pat = "|".join(re.escape(a) for a in sorted_abbrevs)

        pair_re = re.compile(rf"(\d+(?:\.\d+)?)\s+({abbrev_pat})")
        pairs = pair_re.findall(text.strip())
        if not pairs:
            raise ValueError(f"No valid (number, unit) pairs found in: {text!r}")

        total_seconds = Decimal(0)
        finest_prec   = 7   # will be reduced toward the finest (most negative) level seen

        for num_str, abbrev in pairs:
            level   = abbrev_to_level[abbrev]
            quantum = cls.LEVEL_QUANTUM[level] if level >= 0 else Decimal(10) ** level
            total_seconds += Decimal(num_str) * quantum

            dec_places     = len(num_str.split(".")[1]) if "." in num_str else 0
            effective_prec = level - dec_places
            if effective_prec < finest_prec:
                finest_prec = effective_prec

        finest_prec = max(-18, min(7, finest_prec))
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

    def format_for_display(self) -> str:
        """
        Decompose the duration into a human-readable compound string scaled to
        the stored precision level, e.g.:

            UnivDuration(31557600000000, M_YEAR)  → "1 M-year"
            UnivDuration(90061, SECOND)           → "1 day 1 hr 1 min 1 s"
            UnivDuration(3661,  MINUTE)           → "1 hr 1 min"
            UnivDuration(Decimal('5.123'), -3)    → "5 s 123 ms"
            UnivDuration(Decimal('0.001'), -3)    → "1 ms"
        """
        sign      = "-" if self.seconds < 0 else ""
        remaining = abs(self.seconds)
        parts: list[str] = []
        bottom    = _dur_level(self)    # finest level: negative=sub-second, 0..7=coarse
        floor     = max(0, bottom)      # highest index we loop down to

        # Decompose whole units from level 7 down to floor
        for level in range(7, floor - 1, -1):
            q     = UnivDuration.LEVEL_QUANTUM[level]
            count = int(remaining / q)
            if count > 0:
                parts.append(f"{count} {_abbrev(level, count)}")
                remaining -= count * q

        # Sub-second residual
        if bottom < 0:
            frac_q = Decimal(10) ** bottom
            frac_n = int((remaining / frac_q).to_integral_value(ROUND_HALF_EVEN))
            label  = UnivDuration.LEVEL_ABBREV.get(bottom, f"10^{bottom}s")
            if frac_n > 0 or not parts:
                parts.append(f"{frac_n} {label}")

        if not parts:
            label = _abbrev(bottom, 0)
            parts.append(f"0 {label}")

        return sign + " ".join(parts)

    def __str__(self) -> str:
        if self.precision < 0:
            return f"UnivDuration({self.seconds}, {self.precision})"
        return f"UnivDuration({self.seconds})"
    
    def __repr__(self) -> str:
        return f"UnivDuration(seconds={self.seconds}, precision={self.precision})"