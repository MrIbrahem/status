# Configuration Update: Dynamic Year Calculation

## Change Summary

Updated `src/config.py` to calculate `LAST_YEAR` and `CURRENT_YEAR` dynamically using Python's standard `datetime` module instead of hardcoding values.

## Before (Hardcoded)

```python
# Years
LAST_YEAR: str = "2024"
CURRENT_YEAR: str = "2025"
```

**Problems:**
- ❌ Requires manual update every year
- ❌ Easy to forget to update
- ❌ Can cause stale data if not maintained

## After (Dynamic)

```python
from datetime import datetime

# Years (dynamically calculated)
CURRENT_YEAR: str = str(datetime.now().year)
LAST_YEAR: str = str(datetime.now().year - 1)
```

**Benefits:**
- ✅ Automatically updates with system date
- ✅ No manual maintenance required
- ✅ Always uses correct years
- ✅ Uses Python standard library (no dependencies)

## Full Updated config.py

```python
"""
Application configuration.

All configuration constants for the Wikipedia Medicine project.
"""
from datetime import datetime
from typing import Dict, Any

# Years (dynamically calculated from current date)
CURRENT_YEAR: str = str(datetime.now().year)
LAST_YEAR: str = str(datetime.now().year - 1)

# Processing
BATCH_SIZE: int = 100
MAX_CONNECTIONS: int = 5
QUERY_TIMEOUT: int = 60
MAX_RETRIES: int = 3

# Database
CREDENTIAL_FILE: str = "~/replica.my.cnf"
DATABASE_PORT: int = 3306
DATABASE_CHARSET: str = "utf8mb4"

# Output directories
OUTPUT_DIRS: Dict[str, str] = {
    "languages": "languages",
    "editors": "editors",
    "reports": "reports"
}

# Logging
LOG_LEVEL: str = "INFO"
LOG_FILE: str = None
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# Database connection parameters
DATABASE_CONFIG: Dict[str, Any] = {
    "port": DATABASE_PORT,
    "charset": DATABASE_CHARSET,
    "connect_timeout": 30,
    "read_timeout": QUERY_TIMEOUT,
    "autocommit": True,
}
```

## Usage Examples

```python
from src.config import LAST_YEAR, CURRENT_YEAR

# In queries
query = f"WHERE rev_timestamp LIKE '{LAST_YEAR}%'"

# In logging
logger.info("Processing year: %s", LAST_YEAR)

# When run in 2026
# CURRENT_YEAR will be "2026"
# LAST_YEAR will be "2025"
```

## Testing Considerations

### Test for Dynamic Calculation

```python
"""Test configuration module."""
import pytest
from datetime import datetime
from src import config


@pytest.mark.unit
def test_years_are_dynamic():
    """Test that years are calculated from current date."""
    current_year = datetime.now().year
    
    assert config.CURRENT_YEAR == str(current_year)
    assert config.LAST_YEAR == str(current_year - 1)


@pytest.mark.unit
def test_years_are_strings():
    """Test that years are string type for SQL queries."""
    assert isinstance(config.CURRENT_YEAR, str)
    assert isinstance(config.LAST_YEAR, str)


@pytest.mark.unit
def test_year_format():
    """Test year format is 4 digits."""
    assert len(config.CURRENT_YEAR) == 4
    assert len(config.LAST_YEAR) == 4
    assert config.CURRENT_YEAR.isdigit()
    assert config.LAST_YEAR.isdigit()
```

### Mocking for Specific Year Testing

If you need to test with a specific year:

```python
from unittest.mock import patch
from datetime import datetime

@pytest.mark.unit
@patch('src.config.datetime')
def test_with_specific_year(mock_datetime):
    """Test behavior with a specific year."""
    # Mock datetime.now() to return 2024
    mock_datetime.now.return_value = datetime(2024, 6, 15)
    mock_datetime.now().year = 2024
    
    # Re-import to get mocked values
    import importlib
    import src.config
    importlib.reload(src.config)
    
    assert src.config.CURRENT_YEAR == "2024"
    assert src.config.LAST_YEAR == "2023"
```

## CLI Override (Optional Enhancement)

For flexibility, you could allow CLI override:

```python
# In main.py
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        default=LAST_YEAR,
        help=f"Year to analyze (default: {LAST_YEAR})"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    year = args.year  # Use CLI year if provided
    
    logger.info("Analyzing year: %s", year)
```

## Alternative: Using relativedelta

For more complex date calculations:

```python
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Last year
LAST_YEAR: str = str((datetime.now() - relativedelta(years=1)).year)

# Last month (if needed)
LAST_MONTH: str = (datetime.now() - relativedelta(months=1)).strftime("%Y%m")
```

## Documentation Updates

### README.md

Update the usage section:

```markdown
## Configuration

The application automatically uses the previous year for analysis.
For example, when run in 2025, it analyzes 2024 data.

To analyze a different year:
```bash
python -m src.main --year 2023
```
```

### .claude/context/conventions.md

Add to the Constants section:

```markdown
### Dynamic Constants

Constants that depend on runtime state should use Python's standard library:

```python
# ✓ Good - Dynamic calculation
from datetime import datetime
CURRENT_YEAR = str(datetime.now().year)

# ✗ Bad - Hardcoded value requiring updates
CURRENT_YEAR = "2025"
```
```

## Migration Checklist

If updating existing code:

- [ ] Update `src/config.py` with dynamic calculation
- [ ] Update tests in `tests/unit/test_config.py`
- [ ] Update documentation references to year values
- [ ] Update `.claude/context/conventions.md`
- [ ] Update `copilot_prompt.md`
- [ ] Test in development environment
- [ ] Verify SQL queries use correct year format
- [ ] Update README.md with dynamic year explanation

## Benefits Recap

1. **Maintenance**: Zero manual updates needed
2. **Accuracy**: Always uses correct year
3. **Simple**: Uses Python standard library
4. **Testable**: Easy to mock for testing
5. **Flexible**: Can still override via CLI if needed

---

*This improvement ensures the application stays current without manual intervention.*
