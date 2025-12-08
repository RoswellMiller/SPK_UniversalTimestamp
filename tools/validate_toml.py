import tomllib  # built-in in Python 3.11+
from pathlib import Path

def validate_toml(path: str):
    file = Path(path)
    try:
        with file.open("rb") as f:
            data = tomllib.load(f)
        print("✅ TOML parsed successfully!")
        return data
    except Exception as e:
        print("❌ Error parsing TOML:")
        print(e)

# Example usage
validate_toml("pyproject.toml")